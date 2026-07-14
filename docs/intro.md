
Alpha60 is a long-term study of media on the distributed internet, focusing on streaming film and television, but also including examples of other media including 3d gun files and hacks/leaks from the transparency collective Distributed Denial of Secrets.

This fall, we will start with groupings of streaming tv, and depending on the progress we make with those data sets, we will be widening the scope to include the UKR-RUS cyberwar leaks.

About our technical background and scope.

There are three parts to alpha60 compute infrastructure:

1. Samplers: cluster of 9 leased bare metal alma 9/10 linux machines in europe that run a custom C++ p2p swarm sample application 24/7. This cluster is administered in python with ansible,  reads a github data repository for input, and is scheduled via chron.  Standard operating practice is to do super-saturated sampling of the p2p swarm every 3 minutes, for 10, 15, or 26 weeks. Each sample (aka every 3 minutes) writes a json output file. These files are archived and compressed, and transferred to offline storage.  
2. Caching: this is a cluster of workstation hardware in SF that aggregates individual samples into aggregates in durations of hour, day, week, and cumulative.  
3. Analysis: another cluster of hardware that takes aggregates, does IP-\>geolocation, and writes out an anonymized json file stripped of ip addresses but augmented with geolocation and network characteristics using specialized ip to geolocation software from [Ipinfo.io](http://Ipinfo.io).  In fact, alpha60 has research access to all Ipinfo [data API](https://ipinfo.io/developers/libraries)s  at the highest resolution in unlimited quantities (with attribution). This group will primarily be working on this part of the infrastructure.

Our scope:

Year	a60 download	netflix subscribers  
2018 	63M 		139M  
2019 	154M 		167M  
2020 	206M 		204M  
2021 	594M 		222M  
2022 	353M 		231M  
2023 	743M 		260M   
2024 	1.99B

We are going to be developing new techniques for data analysis of this information. This is new territory, and we will be trying to correlate to existing media metrics from film (box office) and streaming tv (Nielsen, and look at some of the other metrics on a per-platform basis.) We will be trying to estimate the growth of piracy vis-a-vis growth of the internet and growth of commercial streaming platforms Disney+, Amazon Prime, Netflix, Apple TV+

