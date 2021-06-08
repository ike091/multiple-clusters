# CloudLab Cluster Notes

## Setup

* Used dual-homed bare-metal machines, and set up Kubernetes on experimental plane.
* Used control plane for ssh and `kubectl` access.


## Experiments

* Ran Nginx instances on each cluster and accessed from other cluster
* Ran `iperf` both ways - 105 to 106 megabits per second


### perfSONAR
* Used `/etc/hosts` to simulate DNS records
* Ran `perfsonar-testpoint` on one cluster, and `perfsonar-checker` on the other
* Repeated both ways

No added latency:
* See `multiple-clusters/logs/perfsonar-output-1.log`, and `multiple-clusters/logs/perfsonar-output-2.log`

50ms added latency:
* See `multiple-clusters/logs/perfsonar-50ms-1.log`, and `multiple-clusters/logs/perfsonar-50ms-2.log`

