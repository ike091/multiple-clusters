# CloudLab Cluster Notes

## Setup

* Used dual-homed bare-metal machines, and set up Kubernetes on experimental plane.
* Used control plane for ssh and `kubectl` access.


## Experiments

* Ran Nginx instances on each cluster and accessed from other cluster
* Ran `iperf` both ways - around TODO


### perfSONAR

* Used `/etc/hosts` to simulate DNS records
* Ran `perfsonar-testpoint` on one cluster, and `perfsonar-checker` on the other
* Repeated the other way around
* See `multiple-clusters/logs` for results


