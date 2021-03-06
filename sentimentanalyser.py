pip install --upgrade "ibm-watson>=4.4.0"
pip install aylien-news-api

from __future__ import print_function
import aylien_news_api
from aylien_news_api.rest import ApiException
from pprint import pprint
configuration = aylien_news_api.Configuration()

# Configure API key authorization: app_id
configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = '75a3c792'

# Configure API key authorization: app_key
configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = '14646d1168ada4e30e7f288ebe6dcd0f'
configuration.host = "https://api.aylien.com/news"

# Create an instance of the API class
api_instance = aylien_news_api.DefaultApi(aylien_news_api.ApiClient(configuration))

def fetch_new_stories(params={}):
  fetched_stories = []
  stories = None

  while stories is None or len(stories) > 0:
    try:
      response = api_instance.list_stories(**params)
    except ApiException as e:
      if ( e.status == 429 ):
        print('Usage limits are exceeded. Waiting for 60 seconds...')
        time.sleep(60)
        continue

    stories = response.stories
    params['cursor'] = response.next_page_cursor

    fetched_stories += stories
    print("Fetched %d stories. Total story count so far: %d" %
      (len(stories), len(fetched_stories)))

  return fetched_stories

params = {
  'language': ['en'],
  'title': 'Politics',
  'published_at_start': 'NOW-5DAYS',
  'published_at_end': 'NOW',
  'cursor': '*',
  'sort_by': 'published_at'
}

stories = fetch_new_stories(params)

print('************')
print("Fetched %d stories mentioning 'politics' in the title, are in English, and were published between %s and %s" %
(len(stories), params['published_at_start'], params['published_at_end']))from __future__ import print_function
import aylien_news_api
from aylien_news_api.rest import ApiException
from pprint import pprint
configuration = aylien_news_api.Configuration()

# Configure API key authorization: app_id
configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = '75a3c792'

# Configure API key authorization: app_key
configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = '14646d1168ada4e30e7f288ebe6dcd0f'
configuration.host = "https://api.aylien.com/news"

# Create an instance of the API class
api_instance = aylien_news_api.DefaultApi(aylien_news_api.ApiClient(configuration))

def fetch_new_stories(params={}):
  fetched_stories = []
  stories = None

  while stories is None or len(stories) > 0:
    try:
      response = api_instance.list_stories(**params)
    except ApiException as e:
      if ( e.status == 429 ):
        print('Usage limits are exceeded. Waiting for 60 seconds...')
        time.sleep(60)
        continue

    stories = response.stories
    params['cursor'] = response.next_page_cursor

    fetched_stories += stories
    print("Fetched %d stories. Total story count so far: %d" %
      (len(stories), len(fetched_stories)))

  return fetched_stories

params = {
  'language': ['en'],
  'title': 'Politics',
  'published_at_start': 'NOW-5DAYS',
  'published_at_end': 'NOW',
  'cursor': '*',
  'sort_by': 'published_at'
}

stories = fetch_new_stories(params)

print('************')
print("Fetched %d stories mentioning 'politics' in the title, are in English, and were published between %s and %s" %
(len(stories), params['published_at_start'], params['published_at_end']))


import json
from newsapi.newsapi_client import NewsApiClient
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions,ConceptsOptions,EntitiesOptions,SentimentOptions

authenticator = IAMAuthenticator('4HecLEQUBw03WbfyI1FFubQIoH7TbPtl8TU0RMwGcFMl')
natural_language_understanding = NaturalLanguageUnderstandingV1(version='2019-07-12',authenticator=authenticator)


natural_language_understanding.set_service_url('https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/775e9661-0eec-420c-a526-ee3be3d3d5e6')

newsapi=NewsApiClient(api_key="13626ce152a348e890604da34423ecdf")
news=newsapi.get_everything(q='Politics',language='en')

for i in news['articles']:
    response=natural_language_understanding.analyze(
        url=i['url'],features=Features(entities=EntitiesOptions(sentiment=True,limit=1),concepts=ConceptsOptions(limit=3),categories=CategoriesOptions(limit=3))).get_result()
    
    print(json.dumps(response, indent=4))