#TODO: Create database connection or instanciation rule

BCC=browserContentCollector

test_rss: sampleRSSFeeds.txt rssItemCollector.py
	cat sampleRSSFeeds.txt | python3 rssItemCollector.py

test_content: sampleURLs.txt $(BCC)/$(BCC).js
	cat sampleURLs.txt | node $(BCC)/$(BCC).js

clean:
	rm -rf *.png