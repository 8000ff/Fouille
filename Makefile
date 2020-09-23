#TODO: Create database connection or instanciation rule

RssIC=rssItemCollector.py
BCC=browserContentCollector/browserContentCollector.js

sampleRssItem:
	mongoexport --db rss --collection rss_item --out sampleRssItem

sampleRssItemId: sampleRssItem
	cat sampleRssItem | jq '._id' | jq '.[]' | tr -d '"' > sampleRssItemId

sampleHash: sampleRssItem
	cat sampleRssItem | jq '.hash' | tr -d '"' > sampleHash

sampleUrl: sampleRssItem
	cat sampleRssItem | jq '.link' > sampleUrl

test_rss: feed $(RssIC)
	python3 $(RssIC) < feed

test_content: sampleHash $(BCC)
	head -n 1 sampleHash | node $(BCC)

clean:
	rm -rf sampleRssItem sampleHash sampleUrl sampleRssItemId