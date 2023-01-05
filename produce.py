#!/usr/bin/env python3
import argparse
import csv
from ipaddress import IPv4Network, IPv6Network
import math

parser = argparse.ArgumentParser(description='Generate non-China routes for BIRD.')
parser.add_argument('--next', default="wg0", metavar = "INTERFACE OR IP",
                    help='next hop for where non-China IP address, this is usually the tunnel interface')

args = parser.parse_args()

class Node:
    def __init__(self, cidr, parent=None):
        self.cidr = cidr
        self.parent = parent

    def __repr__(self):
        return "<Node %s>" % self.cidr

def dump_tree(lst, ident=0):
    for n in lst:
        print("+" * ident + str(n))
        dump_tree(n.child, ident + 1)

def dump_bird(lst, f):
    for n in lst:
       f.write(n)


def subtract_cidr(sub_from, sub_by):
    for cidr_to_sub in sub_by:
        for n in sub_from:
            if n.cidr == cidr_to_sub:
                n.dead = True
                break

            if n.cidr.supernet_of(cidr_to_sub):
                if len(n.child) > 0:
                    subtract_cidr(n.child, sub_by)

                else:
                    n.child = [Node(b, n) for b in n.cidr.address_exclude(cidr_to_sub) ]

                break

root = []

with open("chnroutes.txt", newline='') as f:
    f.readline() # skip the title
    f.readline()
    for line in f:
        line = line.strip('\n')
        root.append('route %s via "%s";\n' % (line, args.next))

with open("routes4.conf", "w") as f:
    dump_bird(root, f)

