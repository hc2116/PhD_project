# Description of the Python source files

All files in this director are written in Python 3, with the exception of the files found in the python2 directory.

## Generic files

### [utils](utils.py)

Generic functions; e.g. to find all netflow files in directory.

## CTU files

### [ctu_botnet_actions](ctu_botnet_actions.py)

Parse/extract actions and generate FSA/MC from the CTU dataset. Examples of how to do this that can easily be generalised.

### [aggreate_CTU](aggreate_CTU.py)

Aggregates data obtained from create_dataset_CTU.py, adding markov chaing features and dfsa features

### [create_dataset_CTU](create_dataset_CTU.py)

Parse and extract data from the CTU dataset. The result is a DataFrame with Normal and Infected traffic


### [one_class_svm_CTU](one_class_svm_CTU.py)

One-class svm on aggregated features. One-class svm is traine on Normal traffic studying structure of combinations of SrcAddr+session

### [rnn](rnn.py)

RNN training and prediction of normaly traffic. 

## Sherlock files

### [sherlock_initial_exploration](sherlock_initial_exploration.py)

### [sherlock_actions](sherlock_actions.py)

Functionality to parse and extract actions from Sherlock set. This can then be used to extract FSA and MChain
**TODO: create a simple interface [probably excl parsing] to integrate with Marc's stuff**

### [sherlock_sessions](sherlock_session.py)

Contains two classes to connect readings (for a given user at a given time) with a session in the Moriarty app.

### [sherlock_utils](sherlock_utils.py)

General things to read dataframe and work with sherlock_sessions. Should probably be removed at some point as I suspect it duplicates things (or will be duplicated) in order files.


## models directory

This directory contains files related to the formal models and learning of formal models. Note that there was an implementation of learning association rules using the Apriori algorithm

### [mchain](models/mchain.py)

Simple Markov Chain implementation where there is one node for each action, and we store the probability of consequtive action simply by counting. Properties to generate MC and to compute probabilities for a sequence of action, given a MC.

### [dfsa](models/dfsa.py)

Contains Deterministic FSA representation (class FSA) and Pretex Tree Acceptor (PTA). FSA class is not used (the Non-Deterministic version is used), but PTA is used to generate the initial automata from the logs.

## [ndfsa](models/ndfsa.py)

Non-deterministic FSA implementation, including a "coloured" extension implementing the Blue-Fringe algorithm for state merging (FSA learning). 

### [graphviz](models/graphviz.py)

Contains all the files to visualise automata/Markov chain using Graphviz (Note: separated to separate due to installation issue with graphbiz libarry on Python 3 for Windows). This file has
not been tested (in Python 3; the Python 2 versions work [when included within the corresponding classes])

## python2 directory

This directory contains the original Python 2 files that has now been ported to Python 3. This directory should be ignored. Some of these are no longer used (but kept just in case)

## rnn_models directory

Contains the learnt RNN models. 

## fsa_models directory

**TODO: create a directory with learnt FSA (json)**

## test_data directory

Some files used for testing during development; can be deleted.
