import feedparser
from jinja2 import Template
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

NEWS = [
    "https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja",
    "https://rss.cnn.com/rss/edition.rss",
    "https://feeds.bbci.co.uk/news/rss.xml"
]

summarizer = LsaSummarizer()

articles = []

for url in NEWS:
    feed = feedparser.parse(url)

    for e in feed.entries[:5]:
        text = e.get("summary", "")

        if len(text) > 100:
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            sentences = summarizer(parser.document, 2)
            summary = " ".join(str(s) for s in sentences)
        else:
            summary = text

        articles.append({
            "title": e.title,
            "link": e.link,
            "summary": summary
        })

# 重複削除
unique = {}
for a in articles:
    unique[a["title"]] = a
articles = list(unique.values())[:15]

html_template = open("index_template.html", encoding="utf-8").read()
template = Template(html_template)

output = template.render(news=articles)

open("index.html","w",encoding="utf-8").write(output)

print("index.html生成完了")
