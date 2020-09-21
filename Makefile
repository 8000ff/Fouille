#TODO: Create database connection or instanciation rule

BCC=browserContentCollector

feed_db : sampleRSSItems
	mongoimport --db rss --colleciton rss_item sampleRSSItems

sampleRSSItems:
	mongoexport --db rss --collection rss_item --out sampleRSSItems

test_rss: sampleRSSFeeds.txt rssItemCollector.py
	python3 rssItemCollector.py < sampleRSSFeeds.txt

test_content: sampleHash.txt $(BCC)/$(BCC).js
	node $(BCC)/$(BCC).js < sampleHash.txt

clean:
	rm -rf *.png