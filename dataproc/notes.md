# Dataproc

## Hadoop and Spark

### What is it

**Hadoop** is an open-source big data processing software that leverages a cluster of computers by distributing work and completing tasks in parallel.

Consists of

  * HDFS - hadoop distributed file system
  * YARN - facilitating software for managing master/worker nodes
  * MapReduce - the paradigm for how data is processed.

__Spark__ is a big data engine that can consume and process large amounts of data for various analytical workloads

Why Spark?

* It runs on top of Hadoop, easier to use than Hadoop and supports various programming languages (Java, Python, Scala, R, SQL)
* Spark comes with other libraries for supporting use cases requiring machine learning, streaming, SQL and machine learning

### On-Premise

On-premise clusters have challenges where compute resources have to be adjusted for different sized workloads. It's hard to scale fast and there are capacity limits. Also, compute and storage are not seperated, thus if the cluster isn't on data cannot be accessed.

## Dataproc

A managed Hadoop/Spark cluster service in the cloud that can use various compute resources to meet different needs. It's low-cost (charges at vCPU/hr), fast to provision (~90 seconds), and includes many familiar Hadoop/Spark ecosystem libraries already installed including Hadoop, Spark, Pig, Hive, Flink, etc. This means developers can focus on their work rather than configuring and tuning cluster settings for different workloads. Dataproc can also connect with other GCP products including Google Cloud Storage, BigQuery, BigTable, Logging and Monitoring.

[To see more information on dataproc image versions and the libraries they include](https://cloud.google.com/dataproc/docs/concepts/versioning/overview)

### Architecture

In a dataproc cluster the Master and Worker nodes use compute engine VMs (can set secondary workers to be preemptible for cost savings). Clusters can use a persistent disk for HDFS or they can access data stored in Google Cloud Storage. The latter is optimal as it's cheaper, faster, seperates compute and storage, requires less maintenance, and can interact with other GCP products. Google's network is very fast so there's no need to have data located close to the compute. 

Reminder
**Colossus** is Google's massively distributed storage layer on Google's servers in their data centers.
**Jupiter** is google's 1Petabit/sec bandwith network.

[Cool demonstration describing the steps data follows when travelling in and out of Google's network!](https://cloud.withgoogle.com/infrastructure/)

To use GCS instead of HDFS in most cases just change the URL from `hdfs://` to `gs://`

### Cluster Designs

#### Cluster Types

1. __Single node cluster__ - primarily for proof of concept work; cannot be autoscaled
2. __Standard/Default Cluster__ - 1 master, 2+ worker nodes. 
3. __High Availability Cluster__ - 3 master, 2+ worker nodes. Ideal for workloads where it _cannot_ be impacted by failures at all. Ensures YARN and HDFS operations are uninteruppted, even if there are single-node failures or reboots.

It's possible to use preemptible workers as "secondary" workers, but they will not store any data, so they're useful for high compute jobs. If you require more storage then use non-preemptible secondary workers.

#### Job Type
**Batch/Ephemeral Job Workloads** - Clusters are provisioned for specific jobs, then they're deleted once the job is complete. 

**Long standing clusters** - Deploy a small cluster where users can submit jobs. The cluster can scale up and down depending on the workload size. This approach is for when there is frequent demand to run Dataproc jobs, otherwise follow the Batch Job model and delete the cluster. Clusters take no more than a couple minutes to provision and resizing takes a similar amount of time as deleting/creating.

##### Autoscaling 

Yes use:
* clusters that store data in external sources (eg. GCS or BQ)
* clusters that process many jobs
* to scale up single-job clusters


Not recommended for:
* High availability clusters
* HDFS
* YARN Node Labels
* Spark Streaming
* Idle Clusters


Note from Datarpoc Autoscaling Documentation
> Use Dataproc Workflows to schedule a set of jobs on a dedicated cluster, and then delete the cluster when the jobs are finished. For more advanced orchestration, use Cloud Composer, which is based on Apache Airflow. 
> 
> For clusters that process ad-hoc queries or externally scheduled workloads, use Cluster Scheduled Deletion to delete the cluster after a specified idle period or duration, or at a specific time.

### When to use Dataproc and When Not to

Generally speaking if someone is already using a Hadoop cluster or their workloads use Spark or any other related library, then Dataproc makes sense. However, if someone only needs to do data processing and isn't tied down to a library yet, then __Dataflow__ is the recommended product. For people who don't know how to code __Data Fusion__ is a good GUI, drag and drop based data processing tool.

For ML/AI tasks if there is flexibility then it's recommended to explore Google ML APIs or AutoML, AI Platform and TensorFlow, or BQ ML.


### Other Useful Things to Know (WIP)
* If you need other packages or libraries not available in the Dataproc images, you can build and use your own custom image
* Use `DistCp` to copy on-premise data to Google Cloud
  * Push: On-premise cluster runs `distcp` jobs on data in the cluster, then pushes files directly to GCS
  * Pull:  An ephemeral cluster runs `distcp` jobs on its data nodes, pulls data from source cluster then copies it to storage. May require Cloud Interconnect to communicate between on-premise and cloud.
* Take advantage of __Workflow Templates__ to create reuseable workflow configurations for automating repetitive tasks.
* Stackdriver logs can view job driver output, HDFS, YARN, job metrics and operational metrics
* There are cluster detail graphs that show CPU utilization, disk bytes, disk operations, network bytes and packets


### Links and Resources
* [10 tips for building long running clusters](https://cloud.google.com/blog/products/data-analytics/10-tips-for-building-long-running-clusters-using-cloud-dataproc)
* [7 tips for dataproc in production](https://cloud.google.com/blog/products/data-analytics/7-best-practices-for-running-cloud-dataproc-in-production)

