#TODO: Create database connection or instanciation rule
test_rss: database sampleRSSFeeds.txt rssItemCollector.py
	cat sampleRSSFeeds.txt | python3 rssItemCollector.py