import snscrape.modules.twitter as sntwitter
import pandas as pd

query = "New York Mets"
tweets_list = []
num = 0
for tweet in sntwitter.TwitterSearchScraper(query).get_items():
  num+=1
  tweets_list.append(tweet.rawContent)
  print(tweet.rawContent)
