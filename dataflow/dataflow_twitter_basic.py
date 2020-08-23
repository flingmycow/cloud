import string
import logging
import argparse
# import emoji
import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.pipeline import PipelineOptions, StandardOptions, SetupOptions
from apache_beam.options.pipeline_options import GoogleCloudOptions

settings = {
    'gcp': {
        'project': 'red-velvet-98765',
        'bucket': 'somebuckethere',
        'region': 'eur4',
        'zone': 'eur4' 
    },
    'job': {
        'name' : 'cats-tweet-processing',
        'input': 'cats_tweets_small.txt',
        'output_words': 'gs://somebuckethere/stuff/cats_cleaned_tweets.txt',
        'output_emojis': 'gs://somebuckethere/stuff/cats_tweets_emojis.txt'
    }
}

# by default logging doesnt do INFO level
def update_logging_levels(level='INFO'):
    if level == 'INFO':
        logging.getLogger().setLevel(logging.INFO)

def strip_extra(text,chars=None):
    return text.strip(chars)

class ExtractWordFromTweets(beam.DoFn):
    def process(self, element):
        return element.split(" ")      

def run():
    pipeline_options = PipelineOptions()
    google_cloud_options = pipeline_options.view_as(GoogleCloudOptions)
    google_cloud_options.project = settings['gcp']['project']
    google_cloud_options.job_name = settings['job']['name']
    google_cloud_options.staging_location = f"gs://{settings['gcp']['bucket']}/staging"
    google_cloud_options.temp_location = f"gs://{settings['gcp']['bucket']}/temp"
    pipeline_options.view_as(StandardOptions).runner = 'DataflowRunner'
    pipeline_options.view_as(SetupOptions).save_main_session = True

    with beam.Pipeline(options=pipeline_options) as pipe:

        text = pipe | 'Read from text file' >> beam.io.ReadFromText(f"gs://twitter_data_etl/stuff/{settings['job']['input']}")

        tokens = ( 
        text 
        | 'Remove RT from text' >> beam.Map(strip_extra, chars='RT') 
        | 'Remove twitter handles' >> beam.Regex.replace_all(r'@[a-zA-Z0-9_]+', "")
        | 'Remove all url links' >> beam.Regex.replace_all(r'http[s]*://[a-zA-Z0-9_\.\/]+', '')
        | 'Remove punctuation' >> beam.Map(lambda text : text.translate(str.maketrans("","", string.punctuation)))
        | 'Remove all tabs' >> beam.Map(lambda text: text.replace("\t", ""))
        | 'Remove periods (not removed in punctuation step?)' >> beam.Map(lambda text: text.replace(".", ""))
        | 'Make all lowercase' >> beam.Map(lambda text: text.lower())
        | 'Split tweets into words' >> beam.ParDo(ExtractWordFromTweets())
        )

        words = (tokens 
        | 'Prepare word tuples' >> beam.Map(lambda word: (word, 1))
        | 'Group and sum the words to get counts' >> beam.CombinePerKey(sum)
        | 'Save to file' >> beam.io.WriteToText(settings['job']['output_words'])
        )

        # This worked locally ... was having issues with getting the worker package installation in dataflow
        # emojis = (tokens | 'Filter to keep emojis only' >> beam.Filter(lambda token: token if token in emoji.UNICODE_EMOJI else False)
        # | 'Prepare emoji tuples' >> beam.Map(lambda emoji: (emoji, 1)) 
        # | 'Group and sum the emojis to get counts' >> beam.CombinePerKey(sum)
        # | 'Save emojis to text' >> beam.io.WriteToText(settings['job']['output_emojis']) 
        # )
        
    result = pipe.run()
    result.wait_until_finish()

if __name__ == '__main__':
    update_logging_levels()
    run()