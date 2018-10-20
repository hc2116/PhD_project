'''
   Representation of session and readings (for a given session) for Sherlock data. Mainly in order to get suitable 
   readings from sensors/application/T4 etc.
'''

class Session(object):
    '''
        Contains details of all the sessions per user. Assume they are registered in an ordered way
        and keeps an ordered representation.

        A Ssession object is predominently an auxiliary object used by one or more Reading objects.
    '''
    def __init__(self):
        # uid -> (sessionid,version) -> (starttime,endtime)
        self.interval = {}
        # uid -> startime -> (endtime,sessionid,version)
        # ordered index of session
        self.o_current = {}
        self.o_sid = {} # this is the crucial field that contains sessions and used by reading.
    
    def update_session_time(self,uid,time,version,sid):
        '''
            This function will be called from each line from Moriarty probe. It assumes that 
            each call is in order w.r.t time/session etc, and will generate new session (per user)
            if required. By mapping this over each line of the Morarirty probe a complete Session 
            object is created.
        '''
        if not(uid in self.interval):
            self.interval[uid] = {}
            self.o_sid[uid] = {} 
            self.o_current[uid] = -1
        if not((sid,version) in self.interval[uid]):
            self.interval[uid][(sid,version)] = (time,time)
            # new session
            self.o_current[uid] = self.o_current[uid] + 1
            self.o_sid[uid][self.o_current[uid]] = {'start' : time, 'end' : time, 'version' : version, 'sid' : sid}
        # assume ordered    
        self.interval[uid][(sid,version)] = (self.interval[uid][(sid,version)][0],time)
        self.o_sid[uid][self.o_current[uid]]['end'] = time


    
    def get_session(self,uid,time):
        '''
            Returns the corresponding session (if any) given the time and userid.
            Note: this function is never really used.abs
        '''
        for i in self.o_sid[uid]:
            r = self.o_sid[uid][i]
            # there is an option here to compare with the previous next if between session
            # and include readings that are "close"
            # OR: we have multiple iterations to store just before and just after?
            if time > r.end:
                return None
            if time > r.start and time < r.end:
                return (r.sid,r.version)

class Reading(object):
    '''
        Keeps track of particular readings (e.g. T4 or application) with respect to a session,
        i.e. first/last reading and last/first reading after session for particular information 
        as well as number of readings. Functionality to compute relative weight for a particular 
        reading and connect it to a session (for a user).
    '''
    def __init__(self,session):
        self.session = session
        self.reading_time = {}
        self.reading_current = {}
        self.reading_session = {}
        self.wcount = {}

    def reset_reading_time(self):
        '''
            needs to be called before starting to registerer readings
        '''
        self.reading_time = {}
        self.reading_current = {}
        self.reading_session = {}

    def set_reading_time(self,uid,time):
        '''
            1 extra iteration in dataframe: will set border readings for each sensor
            (last_before,first,last,last_after):
                TODO: could be extended to include all the actual readings?
        '''
        if not(uid in self.reading_time):
            self.reading_time[uid] = {}
            self.reading_current[uid] = 0
            self.reading_session[uid] = 0
            self.reading_time[uid][0] = {'session_idx' : 0, 'count' : 0}
        
        if uid in self.session.o_sid and self.reading_session[uid] in self.session.o_sid[uid]:
            curr = self.session.o_sid[uid][self.reading_session[uid]]
        else:
            return # not session exists for this 

        # TODO: what about 0th session? and 0th reading?

        if time > curr['end']: # new session
            self.reading_time[uid][self.reading_session[uid]]['post'] = time
            # post is still a valid reading so increase count
            self.reading_time[uid][self.reading_session[uid]]['count'] = \
              self.reading_time[uid][self.reading_session[uid]]['count'] + 1
            self.reading_session[uid] = self.reading_session[uid] + 1
            if not(self.reading_session[uid] in self.session.o_sid[uid]): # no more sessions for uid
                return
            curr = self.session.o_sid[uid][self.reading_session[uid]] # next session
            cread = {'session_idx' : self.reading_session[uid], 'count' : 0}
            if time >= curr['start']:
                cread['start'] = time
                cread['end'] = time
                cread['count'] = 1
                if 'end' in self.reading_time[uid][self.reading_session[uid]-1]:
                    cread['pre'] = self.reading_time[uid][self.reading_session[uid]-1]['end']
                # if 
            else:
                cread['pre'] = time
            self.reading_time[uid][self.reading_session[uid]] = cread

        if time < curr['start']:
            self.reading_time[uid][self.reading_session[uid]]['pre'] = time
            # not count as a reading so count not increased

        if time >= curr['start']: # update
            # first reading within session
            if not('start' in self.reading_time[uid][self.reading_session[uid]]):
                self.reading_time[uid][self.reading_session[uid]]['start'] = time
            self.reading_time[uid][self.reading_session[uid]]['end'] = time
            self.reading_time[uid][self.reading_session[uid]]['count'] = \
              self.reading_time[uid][self.reading_session[uid]]['count'] + 1
    
    def reset_weigh(self):
        '''
            must be called before starting to compute weights
        '''
        self.wcount = {}

    def compute_weight(self,uid,time):
        '''
            Computes the relative weight of a reading, w.r.t. proportion within a session
            Returns:
              weigh + corresponding session
            Assumptions:
              - uid/time belongs to single session:
              - this is applied top-to-bottom of chain
              - self.wcount is {} to start with

        '''
        if not(uid in self.wcount):
            self.wcount[uid] = 0
    
        # TODO: pre and post may not be defined: how should this be handled?
        #  no pre: first reading was within session
        #  no post: no more readings afterwards - what should we do then?

        # find the suitable session: first has to be above pre
        while (self.wcount[uid] in self.reading_time[uid]) and  \
          (('pre' in self.reading_time[uid][self.wcount[uid]] and \
           time < self.reading_time[uid][self.wcount[uid]]['pre']) or \
          ((not('pre' in self.reading_time[uid][self.wcount[uid]]) and \
           time < self.reading_time[uid][self.wcount[uid]]['start']))):
            self.wcount[uid] = self.wcount[uid] + 1
        # may have skipped sessions so has to be less than post
        while self.wcount[uid] in self.reading_time[uid] and \
          (('post' in self.reading_time[uid][self.wcount[uid]] and \
           time > self.reading_time[uid][self.wcount[uid]]['post']) or \
          (not('post' in self.reading_time[uid][self.wcount[uid]]) and \
           time > self.reading_time[uid][self.wcount[uid]]['end'])):
            self.wcount[uid] = self.wcount[uid] + 1

        # passed last session
        if ('post' in self.reading_time[uid][self.wcount[uid]]) and \
         (time > self.reading_time[uid][self.wcount[uid]]['post']):
            return (0.0,None) 

        # passed last session (and no post) - should never happen
        if not('post' in self.reading_time[uid][self.wcount[uid]]) and  \
          time > self.reading_time[uid][self.wcount[uid]]['end']:
            return (0.0,None) 

        # no suitable sessions so end
        if not(self.wcount[uid] in self.reading_time[uid]):
            return (0.0,None)

        # session haven't started yet (but passed pre) 
        # [this is only used for first reading where partial data is used]
        if time < self.reading_time[uid][self.wcount[uid]]['start']:
            return (0.0,None)
        
        # part of reading is within session
        if time == self.reading_time[uid][self.wcount[uid]]['start']:
            if 'pre' in self.reading_time[uid][self.wcount[uid]]:
                last_read = self.reading_time[uid][self.wcount[uid]]['pre']
                sess_st = self.session.o_sid[uid][self.wcount[uid]]['start']
                # percentage within session
                w = float(time - sess_st) / (time - last_read)
                return (w,self.reading_time[uid][self.wcount[uid]])
            else: 
                # TODO: is this correct if we don't have pre??
                return (1.0,self.reading_time[uid][self.wcount[uid]]) 

        # normal reading within session
        if time > self.reading_time[uid][self.wcount[uid]]['start'] and \
         time <= self.reading_time[uid][self.wcount[uid]]['end']:
            return (1.0,self.reading_time[uid][self.wcount[uid]])

        # Should never happen: if there is no post then there should not be 
        # a reading after end...
        if not('post' in self.reading_time[uid][self.wcount[uid]]):
            return (0.0,None) # TODO: correct? possible?
    
        # part of reading beyond session (i.e. equal post)
        if time > self.reading_time[uid][self.wcount[uid]]['end'] and \
         time <= self.reading_time[uid][self.wcount[uid]]['post']:
            last_read = self.reading_time[uid][self.wcount[uid]]['end']
            sess_end = self.session.o_sid[uid][self.wcount[uid]]['end']
            # percentage within session
            w = float(time - sess_end) / (time - last_read)
            return (w,self.reading_time[uid][self.wcount[uid]])

        return (0.0,None) # don't actually think this can ever happen...
    
    def compute_total_val(self,uid,time,val):
        '''
            Given reading data from a dataframe (user id, time of reading and the particular value read)
            this function will adjust the reading according to weight. It will give 0.0 if the reading does 
            not belong to a session.
        '''
        res = self.compute_weight(uid,time)
        if res[1] == None: # no session
            return (0.0,None)
        else:
            w = res[0]
            sid = res[1]['session_idx']
            sess = self.session.o_sid[uid][sid]
            ret = (uid,sess['sid'],sess['version'])
            return (w * val,ret)

    def compute_total_val_list(self,uid,time,vals):
        '''
            Variant of compute_total_val but given list of val (readings)
        '''
        res = self.compute_weight(uid,time)
        if res[1] == None: # no session
            return ([],None)
        else:
            w = res[0]
            sid = res[1]['session_idx']
            sess = self.session.o_sid[uid][sid]
            ret = (uid,sess['sid'],sess['version'])
            return ([w * val for val in vals],ret)

    def compute_avg_val(self,uid,time,val):
        '''
            Similar to compute total but used if average value is needed. Meaning we should not use average from Panda
            aggreate features but total with this function (as it also adjust according to weight [meaning how much of the 
            reading is actually inside the session.])
        '''
        res = self.compute_weight(uid,time)
        if res[1] == None: # no session
            return (0.0,None)
        else:
            w = res[0]
            sid = res[1]['session_idx']
            sess = self.session.o_sid[uid][sid]
            ret = (uid,sess['sid'],sess['version'])
            c = res[1]['count']
            if c > 0:
                return (w * val / c,ret)
            else: # should not happen
                return (0.0,None) 

    def compute_avg_val_list(self,uid,time,vals):
        '''
            Variant of compute_avg_val but for list of values
        '''
        res = self.compute_weight(uid,time)
        if res[1] == None: # no session
            return (0.0,None)
        else:
            w = res[0]
            sid = res[1]['session_idx']
            sess = self.session.o_sid[uid][sid]
            ret = (uid,sess['sid'],sess['version'])
            c = res[1]['count']
            if c > 0:
                return ([w * val / c for val in vals],ret)
            else: # should not happen
                return ([],None) 

def simple_test():
    '''
        Simple test of sessions
    '''
    sess = Session()
    #sess.update_session_time(uid,time,version,sid)
    sess.update_session_time(0,1,0.0,1)
    sess.update_session_time(0,2,0.0,1)
    sess.update_session_time(0,4,0.0,1)
    sess.update_session_time(0,5,0.0,1)
    sess.update_session_time(0,7,0.0,2)
    sess.update_session_time(0,9,0.0,2)
    sess.update_session_time(0,10,0.0,2)
    sess.update_session_time(0,20,0.0,3)
    sess.update_session_time(0,30,0.0,3)
    print(sess.o_sid)   
    reading = Reading(sess)
    reading.set_reading_time(0,1)
    reading.set_reading_time(0,2)
    reading.set_reading_time(0,8)
    reading.set_reading_time(0,10)
    reading.set_reading_time(0,14)
    reading.set_reading_time(0,18)
    reading.set_reading_time(0,22)
    reading.set_reading_time(0,35)

    print (reading.compute_weight(0,1))
    print (reading.compute_weight(0,22))
    print (reading.compute_weight(0,35))   

    print (reading.compute_avg_val(0,22,5))
    print (reading.compute_total_val(0,22,5))

    print (reading.compute_avg_val_list(0,22,[3,4,5]))
    print (reading.compute_total_val_list(0,22,[3,4,5]))

## testing
if __name__ == "__main__":
    simple_test()

