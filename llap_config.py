import math

class AmbariSpecs:
    def getAmbariSpecs(self):
        # gather Ambari connection information
        ambari_domain = input("Ambari Domain: ")
        ambari_port = input("Ambari Port/(8080): ")
        ambari_user_id = input("Ambari Username?/(admin): ")
        ambari_pw = input("Ambari Password?/(admin): ")
        rm_domain = input("Resource Manager Domain: ")
        rm_port = input("Resource Manager Port/(8088): ")
        cluster_name = input("Cluster Name? ")
        return AmbariSpecs(ambari_domain, ambari_port, ambari_user_id, ambari_pw, rm_domain, rm_port, cluster_name);


class LLAPHeapSize:
    def getLLAPHeapSize(self, container_size, cores, nodes):
        global llap_heap_size;
        total_cores = cores * nodes
        llap_heap_size = math.ceil((container_size * total_cores * .95))
        heap_check = llap_heap_size / cores
        if heap_check < 4:
            print("Heap size divided by cores must be greater than 4 GB")
        else:
            return llap_heap_size


class MemoryPerDaemonPerNode:
    def getMemoryPerDaemonPerNode(self, nodes, queries, ram):
        total_available_memory = nodes * ram
        global total_concurrent_memory;
        total_concurrent_memory = queries * 2
        global memory_per_deamon_per_node;
        memory_per_deamon_per_node = (total_available_memory - total_concurrent_memory)/nodes
        return memory_per_deamon_per_node, total_concurrent_memory

class CacheSize:
    def getCacheSize(self, total_concurrent_memory, headroom, container_size):
        global cache_size;
        cache_size = memory_per_deamon_per_node - headroom - llap_heap_size
        return cache_size

class main:
    ambari = input("Do you wish to have the script automatically show current configs? y/n:")
    if ambari == 'y':
        ambariconfig = AmbariSpecs()
        ambariconfig.getAmbariSpecs()
    elif ambari == 'n':
        container_size = int(input("What is the value of hive.tez.container.size/(GB)?: "))
        cores = int(input("Number of cores per node?: "))
        ram = int(input("How much RAM per node?/(GB): "))
        nodes = int(input("Number of nodes dedicated to LLAP?: "))
        queries = int(input("Number of concurrent queries?: "))
        headroom = int(input("Headroom?/(GB): "))
    else:
        print("Enter either y/n")

    heapsize = LLAPHeapSize()
    heapsize.getLLAPHeapSize(container_size, cores, nodes)
    print("LLAP Heap Size = " + str(llap_heap_size) + "GB")

    nodememory = MemoryPerDaemonPerNode()
    nodememory.getMemoryPerDaemonPerNode(nodes, queries, ram)
    print("Memory Per Deamon Per Node = " + str(memory_per_deamon_per_node) + "GB")

    cachesize = CacheSize()
    cachesize.getCacheSize(total_concurrent_memory, headroom, container_size)
    print ("Total Cache Size = " + str(cache_size) + "GB")




