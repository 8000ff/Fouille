#TODO: Create database connection or instanciation rule

p=python3

RssIC=rssItemCollector.py
BCC=browserContentCollector/browserContentCollector.js

sampleRssItem:
	mongoexport --db rss --collection rss_item --out sampleRssItem

sampleRssFeed:
	mongoexport --db rss --collection rss_feed --out sampleRssFeed

sampleRssItemId: sampleRssItem
	cat sampleRssItem | jq '._id' | jq '.[]' | tr -d '"' > sampleRssItemId

sampleRssFeedId: sampleRssFeed
	cat sampleRssFeed | jq '._id' | jq '.[]' | tr -d '"' > sampleRssFeedId


sampleHash: sampleRssItem
	cat sampleRssItem | jq '.hash' | tr -d '"' > sampleHash

sampleUrl: sampleRssItem
	cat sampleRssItem | jq '.link' > sampleUrl

add_feed: feed addFeeds.py
	$(p) addFeeds.py < feed

test_rss: sampleRssFeedId $(RssIC)
	$(p) $(RssIC) < sampleRssFeedId
test_content: sampleHash $(BCC)
	head -n 1 sampleHash | node $(BCC)

clean:
	rm -rf sampleRssItem sampleHash sampleUrl sampleRssItemId sampleRssFeed sampleRssFeedId