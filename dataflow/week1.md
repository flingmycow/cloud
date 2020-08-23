# Week 1 

## Introduction

So Google Cloud Platform has various certifications available including Cloud Architect, Cloud Security Engineer, Cloud Developer, and Data Engineer. For my first certification I'll be taking the Data Engineer exam, but there are a few areas of the certification that I need to develop. Thus I spent my first week developing a streaming data pipeline in Dataflow, which is something I have little experience with. I decided to use Twitter data along with one of the most common data architectures in GCP - using PubSub together with Dataflow.

## Prerequisite

If someone wants to use dataflow for a common use case, such as extracting data from PubSub directly into BigQuery, there are templates available that only require parameters to run. This is a good introduction to Dataflow to understand at a high-level how it operates, the user interface and how to interpret the information generated at each stage. 

If you want to develop your own custom pipelines you'll need to know Python or Java as well as _some_ familarity with Google Cloud Platform. Also, if you want to use data from source systems or other products such as PubSub it's ideal to have experience with those too.

If you're a total beginner I recommend doing some Qwiklabs or Pluralsight (you can get a free trial account) and following along exercises/tutorials. I have also seen some good medium posts and videos on Youtube, too.

### A Couple Recommendations

* [5 Minute video explaining what Dataflow is!](https://www.youtube.com/watch?v=KalJ0VuEM7s)
* [Someone has a medium article they update frequently of codes or access to free Qwiklabs!](https://medium.com/@sathishvj/qwiklabs-free-codes-gcp-and-aws-e40f3855ffdb)
* [Architecting Serverless Solutions on Dataflow on PluralSight](https://www.pluralsight.com/courses/google-dataflow-architecting-serverless-big-data-solutions)
* [Tutorials on Google Cloud's documentation](https://cloud.google.com/dataflow/docs/samples)
* [Code examples of dataflow in Python](https://github.com/apache/beam/tree/master/sdks/python/apache_beam/examples)

## Use Case

My _specific_ use case isn't particularly useful, but rather a fun exercise. I wanted to extract data from Twitter and process it with Dataflow with both batch and streaming data. I simply calculated the word and emoji counts as I picked a relatively hard data source in terms of cleaning. The overall process can be applied to other problems that require the processing of data and uploading it to the cloud.

### About Dataflow & Apache Beam

Dataflow allows users to create data processing pipelines for both batch and streaming jobs using a single library - Apache Beam.

#### Benefits of Dataflow

* single model for both batch and streaming data
* no vendor lock-in as it uses Apache Beam. You can run Apache Beam jobs locally or with other services that are not GCP
* dataflow is serverless so it scales up and down to meet the demands of your workloads - simple!
* dataflow has monitoring, log collection, and metrics included in the product so pipeline performance data is readily available for users to view

If you aren't tied to a specific data processing library/tool (eg. Hadoop, Spark, Airflow, etc) then this is a great choice.

### How it Works (high-level)

Dataflow uses Apache Beam to create pipelines. A Pipeline is a series of data transformation steps with the goal of producing data in a certain format. More specifically these operations in apache beam are:
1. PTransform - processing to be done on the data (eg. Filter, Map, Combine, GroupByKey, etc)
2. PCollection - a collection of data and is the output from a PTransform

Pipelines are developed following this format:

```
[final result] = (pipeline | [1st transform] 
                           | [2nd transform] 
                           | [3rd transform, etc])
```