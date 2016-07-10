# kops cleanup scripts

## kops-r53-clean.py

Cleans up route 53 entries left behind by kops.

### USAGE:

```
$ kops-r53-clean.py
USAGE:
./kops-r53-clean.py <KOPS_NAME>

Will find and delete all route53 names under KOPS_NAME
```

Takes one argument: The domain name given to kops:

```
./kops-r53-clean.py kopsdemo.domain.com
I will delete the following DNS entries from route53:
    A api.kopsdemo.domain.com. 54.11.22.33
    A api.internal.kopsdemo.domain.com. 172.20.71.157
    A etcd-events-us-west-2b.internal.kopsdemo.domain.com. 172.20.71.157
    A etcd-us-west-2b.internal.kopsdemo.domain.com. 172.20.71.157
Type 'yes' to continue: yes
Submitted deletes. Waiting on Status updates.
..........
complete
```

## kops-iam-clean.sh

Cleans up the IAM instance_profiles, roles and policies left behind by kops

NOTE: This script has less 'mercy' than the python version

### USAGE:

```
$ kops-iam-clean.sh
USAGE:
./kops-iam-clean.sh <KOPS_NAME>

Will destroy the roles, policies, and instance_profiles kops leaks
```
