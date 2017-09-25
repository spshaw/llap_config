# llap_config

For the initial version only select "n".  Automatic config gathering from Ambari will be included in a future version.

The script needs the following information:
 * Value of hive.tez.container.size in GB
 * Number of cores per node.
 * How much RAM per node in GB
 * Number of nodes dedicated to LLAP
 * Number of concurrent queries.
 * Headroom in GB (This should be around 6 GB)
        
        
       
        
       

This script allows you to determine memory settings prior to enabling LLAP or to predict what memory changes will occur based on inputs.
