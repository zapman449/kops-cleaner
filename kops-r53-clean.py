#!/usr/bin/env python

"""
Clean up left over route53 entries left over from kops
"""

from __future__ import print_function, division, absolute_import, unicode_literals

import sys
import time

import boto
# from boto.route53.record import ResourceRecordSets
# import boto.exception


def usage():
    sys.exit("""
USAGE:
{0} <KOPS_NAME>

Will find and delete all route53 names under KOPS_NAME""")


def derive_potential_zones(name):
    potential_zones = []
    words = name.split('.')
    idx = 0
    while idx < len(words) - 1:
        # -2 allows to ignore the empty string, and the .com TLD
        # using -1 on the off chance someone is running their own TLD
        idx += 1
        potential_zones.append('.'.join(words[idx:]) + '.')
    return potential_zones


def find_zone(name, conn):
    potential_zones = derive_potential_zones(name)
    # print(potential_zones)
    all_hosted_zones = conn.get_all_hosted_zones()
    # TODO: If you have more than 100 hosted zones, this will have to be
    # recalled with a start marker.
    hosted_zones = all_hosted_zones['ListHostedZonesResponse']['HostedZones']
    for zone_record in hosted_zones:
        if zone_record['Name'] in potential_zones:
            paux_id = zone_record['Id']
            zone_id = paux_id.split('/')[2]
            return zone_record['Name'], zone_id
    print("unable to find a matching zone")
    print("looked for these potential zone names based off {}:".format(name))
    for pz in potential_zones:
        print("    {}".format(pz))
    print("Found these zones in route53:")
    for zone_record in hosted_zones:
        print("    {}".format(zone_record['Name']))
    sys.exit("Exiting.")


def find_entries(name, zone, conn):
    records = zone.get_records()
    entries = []
    for record in records:
        if name in record.name:
            entries.append(record)
    if len(entries) == 0:
        sys.exit("Found no entries which matched name {}".format(name))
    return entries


def verify_delete(entries):
    print("I will delete the following DNS entries from route53:")
    for entry in entries:
        # if entry.startswith("api.") or entry.startswith("etcd-"):
        for r in entry.resource_records:
            print("    {0} {1} {2}".format(entry.type, entry.name, r))
    response = raw_input("Type 'yes' to continue: ")
    if response != 'yes':
        sys.exit("Exiting")
    return None


def delete_entries(entries, zone):
    statuses = []
    for entry in entries:
        statuses.append(zone.delete_a(entry.name))
    print("Submitted deletes. Waiting on Status updates.")
    while True:
        counter = 0
        for status in statuses:
            if status.status == 'INSYNC':
                counter += 1
                continue
            x = status.update()
            if x == 'INSYNC':
                counter += 1
        if counter == len(statuses):
            break
        print(".", end="")
        # print("{}".format(counter), end="")
        sys.stdout.flush()
        time.sleep(2)


def main():
    if len(sys.argv) == 1:
        usage()
    conn = boto.connect_route53()
    name = sys.argv[1]
    zone_name, zone_id = find_zone(name, conn)
    zone = conn.get_zone(zone_name)
    entries = find_entries(name, zone, conn)
    verify_delete(entries)
    delete_entries(entries, zone)


if __name__ == "__main__":
    main()
