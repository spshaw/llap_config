#!/usr/bin/env python3

import math


class AmbariSpecs:
    def __init__(self):  # When someone calls AS = AmbariSpecs() This will run
        self.ambari_domain = input("Ambari Domain: ")
        self.ambari_port = input("Ambari Port/(8080): ")
        self.ambari_user_id = input("Ambari Username?/(admin): ")
        self.ambari_pw = input("Ambari Password?/(admin): ")
        self.rm_domain = input("Resource Manager Domain: ")
        self.rm_port = input("Resource Manager Port/(8088): ")
        self.cluster_name = input("Cluster Name? ")
        # return AmbariSpecs(ambari_domain, ambari_port, ambari_user_id,
        #                    ambari_pw, rm_domain, rm_port, cluster_name);


def getLLAPHeapSize(container_size, cores, nodes, num_variable):
    llap_heap_size = container_size * cores * num_variable
    heap_check = llap_heap_size / cores
    if heap_check < 4:
        print("Warning: Heap size divided by cores should be greater than 4 GB")
        return llap_heap_size
    else:
        return llap_heap_size


def getMemoryPerDaemonPerNode(nodes, queries, ram):
    total_available_memory = nodes * ram
    total_concurrent_memory = queries * 2
    memory_per_deamon_per_node = (total_available_memory - total_concurrent_memory)/nodes
    return memory_per_deamon_per_node


def getCacheSize(memory_per_deamon_per_node, headroom, llap_heap_size):
    cache_size = round(llap_heap_size - memory_per_deamon_per_node - headroom, 0)
    return cache_size


class main:
    ambari = input("Do you wish to have the script automatically show current configs? y/n:").lower()
    if ambari == 'y':
        ambariconfig = AmbariSpecs()
        # Code goes here to access data from Ambari Specs
    elif ambari == 'n':
        container_size = int(input("What is the value of hive.tez.container.size/(GB)?: "))
        cores = int(input("Number of cores per node?: "))
        ram = int(input("How much RAM per node?/(GB): "))
        nodes = int(input("Number of nodes dedicated to LLAP?: "))
        queries = int(input("Number of concurrent queries?: "))
        headroom = int(input("Headroom?/(GB): "))
    else:
        print("Enter either y/n")
    # With python Methods don't need to have associated objects.
    #   Also, Global Variables in pyton can be messy so I just saved the outcomes needed for other functions
    #   Some of the variable neames didn't match what was needed in the headers so I defaulted to the headers

    if ram < 128:
        num_variable = .8
    else:
        num_variable = .95

    heapsize = getLLAPHeapSize(container_size, cores, nodes, num_variable)
    print("LLAP Heap Size = " + str(heapsize) + "GB")

    nodememory = getMemoryPerDaemonPerNode(nodes, queries, ram)
    print("Memory Per Deamon Per Node = " + str(nodememory) + "GB")

    cachesize = getCacheSize(nodememory, headroom, heapsize)
    print ("Total Cache Size = " + str(cachesize) + "GB")
