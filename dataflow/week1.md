# Week 1 

## Introduction

So Google Cloud Platform has various certifications available including Cloud Architect, Cloud Security Engineer, Cloud Developer, and Data Engineer. For my first certification I'll be taking the Data Engineer exam, but there are a few areas of the certification that I need to develop. Thus I spent my first week developing a streaming data pipeline in Dataflow, which is something I have little experience with. I decided to use Twitter data along with one of the most common data architectures in GCP - using PubSub together with Dataflow.

_Note_: I'm still a beginner when it comes to Dataflow. When I learn more I'll add more information to this markdown file and include other files in my github repository. Please let me know if anything is incorrect or is outdated. This isn't a comprehensive explanation of *everything*, but serves as a concise explanation of dataflow, which can help with preparing for the data engineering certification.

## Prerequisite

If someone wants to use dataflow for a common use case, such as extracting data from PubSub directly into BigQuery, there are templates available that only require parameters to run. This is a good introduction to Dataflow to understand at a high-level how it operates, the user interface and how to interpret the information generated at each stage. 

[Google provided templates](https://cloud.google.com/dataflow/docs/guides/templates/provided-templates)

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

### Introduction to Dataflow & Apache Beam

Dataflow allows users to create data processing pipelines for both batch and streaming jobs using a single library - Apache Beam.

#### Benefits of Dataflow

* single model for both batch and streaming data
* no vendor lock-in as it uses Apache Beam. You can run Apache Beam jobs locally or with other services that are not GCP
* dataflow is serverless so it scales up and down to meet the demands of your workloads - simple!
* dataflow has monitoring, log collection, and metrics included in the product so pipeline performance data is readily available for users to view
* integrates well with other GCP products such as PubSub, BigQuery, Storage, BigTable, Spanner, and Datastore!

If you aren't tied to a specific data processing library/tool (eg. Hadoop, Spark, Airflow, etc) then this is a great choice.

#### How it Works (high-level)

Dataflow uses Apache Beam to create pipelines. A Pipeline is a series of data transformation steps with the goal of producing data in a certain format. More specifically these operations in apache beam are:
1. PTransform - processing to be done on the data (eg. Filter, Map, Combine, GroupByKey, etc)
2. PCollection - a collection of data and is the output from a PTransform

Pipelines are developed following this format:

```
[final result] = (pipeline | [1st transform] 
                           | [2nd transform] 
                           | [3rd transform, etc])
```

A pipeline may start like this:

```python
pipeline = beam.Pipeline(options=options)
text = pipe | 'Read from text file' >> beam.io.ReadFromText("tweet_data.txt")
cleaned = (text | 'Remove RT from text' >> beam.Map(strip_extra, chars='RT'))
```

So each step is joined with a `|` then followed with an (optional but recommended) definition of the step, and lastly the PTransform after the `>>`. After each PTransform a PCollection is produced containing the results from the transform. 
* Note: The PCollection produces an unorderd collection of data

It's also possible to create a PCollection using the PTransform `create()`

```python
# This example creates a PCollection containing tuples of random data
total_pets = 393.3

with beam.Pipeline() as pipeline:
  fruits = (pipeline | 'Popular pets' >> beam.Create([
    (1, 'Cat', 'Mammal', 94.2, round(94.2/total_pets, 3), '🐈'),
    (2, 'Dog', 'Mammal', 89.7, round(89.7/total_pets, 3), '🐕'),
    (3, 'Fish', 'Vertebrate', 139.3, round(139.3/total_pets, 3), '🐟'),
    (4, 'Bird', 'Vertebrate', 20.3, round(20.3/total_pets, 3), '🐦')]) 
    | beam.Map(print)
  )
```

#### PTransforms

Generally speaking there are two types of PTransforms - **Element-wise** and __Aggregation__

1. Element-Wise: Operates on each element (eg. Map, Filter, Keys, ParDo, FlatMap, etc)
2. Aggregation: Calculates a single value based on multiple values (eg. Count, CombineGlobally, CombinePerKey, Max, Mean, etc)

**Brief Explanations**
* Map: 1-1 mapping over each element 
* FlatMap: for 1-* mapping over each element in the collection
* **ParDo**: parallel do; for running user defined functions that process over each element
* CombineGlobally: combine all elements
* CombinePerKey: combine all elements for each key

[To see all the available transforms for Python](https://beam.apache.org/documentation/transforms/python/overview/)

##### ParDo

If you want to run a custom element-wise transformation on your PCollection then you use a ParDo.
Simply inherit `beam.DoFn` and create a custom class then write the logic in the `process()` method.

```python
class ExtractWordFromTweets(beam.DoFn):
    def process(self, element):
        return element.split(" ")
```

##### Map vs. FlatMap?

Yes, I didn't understand the difference either until I saw a particular example.

```python
# result = [1, 'yes', 2, 'yes', 3, 'yes']
with beam.Pipeline() as pipeline:
  example = (pipeline | 'Test data' >> beam.Create([1,2,3])
                      | beam.FlatMap(lambda x: [x, 'yes'])
                      | beam.Map(print)
  )

# result = [[1, 'yes'], [2, 'yes'], [3, 'yes']]
with beam.Pipeline() as pipeline:
  example = (pipeline | 'Test data' >> beam.Create([1,2,3])
                      | beam.Map(lambda x: [x, 'yes'])
                      | beam.Map(print)
  )
```

#### Inputs and Outputs

I only used the TextIO and PubSubIO connectors, but there are plenty oters available. They vary depending on the SDK you're using.

[Built in I/O connectors](https://beam.apache.org/documentation/io/built-in/)

#### Pipeline Options

When you create your pipeline object you need to provide it configuration parameters. There are a few ways of doing this. The most common way I've seen examples is to configure an argparser and pass in arguments when running the pipeline via command line.

Personally in my pipelines I configured them by adjusting attributes of the Pipeline object.

```python
pipeline_options = PipelineOptions()
google_cloud_options = pipeline_options.view_as(GoogleCloudOptions)
google_cloud_options.project = settings['gcp']['project']
google_cloud_options.job_name = settings['job']['name']
google_cloud_options.staging_location = f"gs://{settings['gcp']['bucket']}/staging"
google_cloud_options.temp_location = f"gs://{settings['gcp']['bucket']}/temp"
pipeline_options.view_as(StandardOptions).runner = 'DataflowRunner'
pipeline_options.view_as(SetupOptions).save_main_session = True
```

The runner tells apache beam which environment to execute the pipeline. In the code above I've told it to use the DataflowRunner. If you don't specify anything, it'll default to DirectRunner which runs the pipeline locally.

[More information about configurations and other things you should be aware of when using the Dataflow runner](https://beam.apache.org/documentation/runners/dataflow/)

### Intro to Streaming

When creating pipeline for streaming data you can use the same model as before. You only need to provide one configuration change to the pipeline options and you're ready to go!

`pipeline_options.view_as(StandardOptions).streaming = True`

#### Windows

In order to perform calculations and aggregations on unbounded data, we need to specify timeframes to split the data so that we can process them in a similar way to batch data. Windows is used to achieve this!

**Main Types of Windows**

These three types are the most common windows to use

1. Fixed - time based chunks that are non-overlapping
2. Sliding - time based chunks that are overlapping
3. Sessions - defined by a minimum gap duration and they are trigged by another element

By default PCollections are assigned to a single, global window so all late data is discarded. Ensure to specify the desired window type along with duration and gap times.

If you want to account for lags of data, as in data that was due to arrive at a particular time but experiened greater latency than usual, then you can also include a **Watermark**. This will include late-coming data.

[More on windowing](https://beam.apache.org/documentation/programming-guide/#windowing)

### Issues / Problems I faced and Tips (WIP)

* Run things with the DirectRunner whilst you're developing to get used to things. Deploying pipelines to Dataflow always takes a minute or so to prepare everything.
* You can provide a requirements.txt file to download packages not already available on workers
  * [More information on including python pipeline dependencies](https://beam.apache.org/documentation/sdks/python-pipeline-dependencies/)
  * [Packages the workers have](https://cloud.google.com/dataflow/docs/concepts/sdk-worker-dependencies)


### Other Info (WIP)

**Dataflow Setup Process**
1. This is the graph construction time phase - Dataflow creates an execution graph from your code
2. Beam validates the pipeline doesn't have errors or invalid operations. If it's fine it'll create a dataflow job.
3. Creates an execution graph of your pipeline; it may optimise it using fusion optimisation
4. Starts the workers and executes each PTransform

**PCollection**
* Stands for Parallel Collection and they're arranged in such a way that data within a PCollection can be distributed to multiple workers at the same time, thus speeding up the data processing process
* They are immutable
* Bounded for batch (fixed size) and Unbounded for streaming data (non-fixed size)