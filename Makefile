#TODO: Create database connection or instanciation rule


p=python3


RssIC=rssItemCollector.py
BCC=browserContentCollector/browserContentCollector.js

n=10


export MONGO_URI=mongodb://localhost:27017

sampleRssItem:
	mongoexport --db rss --collection rss_item --out sampleRssItem

sampleRssFeed:
	mongoexport --db rss --collection rss_feed --out sampleRssFeed

sampleRssItemId: sampleRssItem
	head -n $(n) sampleRssItem | jq '._id' | jq '.[]' | tr -d '"' > sampleRssItemId

sampleRssFeedId: sampleRssFeed
	head -n $(n) sampleRssFeed | jq '._id' | jq '.[]' | tr -d '"' > sampleRssFeedId


sampleHash: sampleRssItem
	head -n $(n) sampleRssItem | jq '.hash' | tr -d '"' > sampleHash

sampleUrl: sampleRssItem
	head -n $(n) sampleRssItem | jq '.link' > sampleUrl

add_feed: feed addFeeds.py
	head -n $(n) feed | $(p) addFeeds.py

test_rss: sampleRssFeedId $(RssIC)
	head -n $(n) sampleRssFeedId | $(p) $(RssIC) 
test_content: sampleRssItemId $(BCC)
	head -n $(n) sampleRssItemId | node $(BCC)

clean:
	rm -rf sampleRssItem sampleHash sampleUrl sampleRssItemId sampleRssFeed sampleRssFeedId