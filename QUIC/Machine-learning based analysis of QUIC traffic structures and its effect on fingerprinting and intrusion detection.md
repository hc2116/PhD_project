## Machine-learning based analysis of QUIC traffic structures and its effect on fingerprinting and intrusion detection



#### Background:
QUIC traffic emulates TCP-like behaviour via UDP, which contains less information in the visible metadata. It furthermore significantly extends parallel multiplexing of transfers in one connection, which decreases the amount of opened connections by a browser to retrieve a webpage. Additionally, compression is used both on the HTTP3 layer as well as directly in QUIC (called QPACK). These three characteristics suggest that QUIC reveals less information about the transferred content and make traffic appear more uniformly across the breadth of QUIC traffic.

On the other side, QUIC implementations are done in user space, allowing for differences across a broad spectrum of applications (Chrome vs Firefox, openssl vs boringssl, different versions of the same application) that could potentially be visible in the traffic structures and allow for device fingerprinting etc. 

Lastly, the usage of QUIC could make intrusion detection based on traffic metadata such as via attack fingerprints more difficult if traffic appears more uniformly.



#### Goals:
1. Analyse how structured the space of QUIC traffic is in comparison to TCP/HTTP2 and TCP/HTTP1.1. Provide some metrics to back up the statements.
- Examine whether fingerprinting websites is made more difficult, potentially via Onion-routing or VPNs. 
- Test wether fingerprinting of individual implementations is easier than for TCP/HTTP. Relate this to the different set-up of QUIC in the user-space 
- Compare information leakage about specific tasks routed via HTTP. 
- Potentially make statements about mining signatures of HTTP/SQL attacks. 

#### Data:

Collect QUIC data and TCP/HTTP data using detgen paradigm into several datasets.

1. First dataset, use client container to crawl a decent number of webpages, both for QUIC and for TCP/HTTP2 and TCP/HTTP1.1. Do this for multiple clients using different implementations. This 
- Second dataset, put a small number of webpages on multiple webservers that are based on different QUIC implementations. Retrieve webpages from them using the implemented clients. This dataset should highlight implementation differences visible in the data
- Third dataset is concerned with different operations performed, such as file posting, SQL information retrieval, or error messages. To minimise work, we can do this on just one server implementation, potentially with different clients. 
- The fourth dataset: effect on attack signatures and intrusion detection, to be more specified

#### Methodology:

Here, we can rely on two approaches. Using an encoder for structure analysis, and training a classifier to test fingerprinting.

######Structure analysis

We can use the already existing LSTM-autoencoder implementation to analyse the overall structure of the traffic. This should be done by training on a dataset mixed between QUIC and TCP/HTTP traffic to avoid differences in model convergence. 
Since decoder has to recreate the original sequence from the created embeddings, they act as an encoding for different structures. By comparing the divergence of the embeddingsof different tasks/websites/implementations between QUIC and TCP/HTTP, we can provide a metric where and how much more or less structure is present. This gives us a measure of how individual actions manifest in traffic structures, and how well separated the structures for different implementations are.

The overall uniformity of the traffic, i.e. how similar the traffic for different tasks is, can be quantified through the reconstruction error. A higher reconstruction error means the traffic contains less visible structure.

###### Fingerprinting

We can then go ahead and see if we can actually fingerprint webpages (primarily, but also) server and client implementations. 
This is done by training an LSTM-classifier following a similar architecture as the encoder.

###### Website fingerprinting

The most common application and threat through for website fingerprinting is to privacy-enhancing measures such as VPNs or Onion-routing. The set-up of a VPN should be relatively simple in DetGen, however there also already exist applications of QUIC to Tor ("Empirical Performance Evaluation of QUIC Protocol for Tor Anonymity Network", "The case for Tor-over-QUIC"), which could be more interesting. I am planning to e-mail the authors about implementations and data.
We also need to ensure that our model is comparable to the latest standard in fingerprinting ("Website Fingerprinting at Internet Scale" for Tor" at NDSS 16)

Finally, we also need to ensure that this is tested against a sufficient background of data to be representable. 

###### Server/Client fingerprinting/Activity information leakage

The dataset for client or server fingerprinting is from our perspective more simple to implement, however we might have to consider that there are less implementations for QUIC than for TCP/HTP, meaning that our background data might be less representable. Itmight also be not a big problem since the majority of TCP/HTTP traffic comes from a small set of browsers (Chrome, Firefox, etc.) and server implementations (NGINX, Apache, IIS). 

Model-wise, fingerprinting is slightly more complex as multiple connections are used by state-of-the-art ("Host Fingerprinting and Tracking on the Web: Privacy and Security Implications", 2018, "Fast and Reliable Browser Identiﬁcation with JavaScript Engine Fingerprinting" 2018), but again the existing LSTM-encoder can be used and potentially repeated for multiple connections.

###### Effect on intrusion detection signatures

For this, we could potentially analyse the effect of QUIC on the performance of signature creation and detection. The signatures obviously need to be in the metadata as opposed to packet loads. The goal here is to see if attacks that have highly visible signatures in TCP/HTTP become less visible in QUIC.
I need to research a bit more on ML-based signature creation to see if the concepts transfer well to QUIC. 

 