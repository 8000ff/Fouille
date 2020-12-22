#TODO: Create database connection or instanciation rule

p=python3

RssIC=rssItemCollector.py
BCC=browserContentCollector/browserContentCollector.js
svm=svmClassifier.py

CC=contentCleaner/contentCleaner.py
E=exporter/exporter.py

n=10

#export MONGO_URI=mongodb://localhost:27017
#export ELASTIC_URI=http://localhost:9200/

sampleRssItem:
	mongoexport $(MONGO_URI) --db rss --collection rss_item --out sampleRssItem

sampleRssFeed:
	mongoexport $(MONGO_URI) --db rss --collection rss_feed --out sampleRssFeed

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

test_svm:
	$(p) $(svm)
test_content_cleaner: sampleRssItemId $(CC)
	head -n $(n) sampleRssItemId | $(p) $(CC)
test_exporter: sampleRssItemId $(E)
	head -n $(n) sampleRssItemId | $(p) $(E)

daemon:
	python3 daemon.py

# save:
# 	mongoexport $(MONGO_URI) --db rss --collection rss_task --out rss_task
# 	mongoexport $(MONGO_URI) --db rss --collection config --out config

load:
	# mongoimport $(MONGO_URI) --db rss --collection config --file config.json
	mongoimport $(MONGO_URI) --db rss --collection rss_task --file rss_task.json

clean:
	rm -rf sampleRssItem sampleHash sampleUrl sampleRssItemId sampleRssFeed sampleRssFeedId