#!/bin/bash

name=$1
if [[ -z "$name" ]]; then
    echo "USAGE:"
    echo "$0 <KOPS_NAME>"
    echo
    echo "Will destroy the roles, policies, and instance_profiles kops leaks"
    exit
fi

which aws >/dev/null 2>&a
if [[ "$?" != "0" ]]; then
    echo "$0 requires the aws cli tools be installed"
    exit
fi

for pre in masters nodes ; do
    aws iam remove-role-from-instance-profile --instance-profile-name ${pre}.${name} --role-name ${pre}.${name}
    aws iam delete-instance-profile --instance-profile-name ${pre}.${name}
    aws iam delete-role-policy --role-name ${pre}.${name} --policy-name ${pre}.${name}
    aws iam delete-role --role-name ${pre}.${name}
done
