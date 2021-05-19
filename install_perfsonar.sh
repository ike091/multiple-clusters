#! /bin/bash

# Installs perfSONAR on a CentOS7 box

sudo yum install epel-release

sudo yum install http://software.internet2.edu/rpms/el7/x86_64/latest/packages/perfSONAR-repo-0.10-1.noarch.rpm

sudo yum clean all

sudo yum install perfsonar-toolkit -y

