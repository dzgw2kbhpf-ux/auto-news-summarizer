import feedparser
from transformers import pipeline
from jinja2 import Template

NEWS = [
    "https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja",
    "https://rss.cnn.com/rss/edition.rss",
    "https://feeds.bbci.co.uk/news/rss.xml"
]

print("モデル読み込み...")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

articles = []

for url in NEWS:
    feed = feedparser.parse(url)
    for e in feed.entries[:5]:
        text = e.get("summary","")
        if len(text) > 100:
            try:
                s = summarizer(text[:1000], max_length=120, min_length=30, do_sample=False)[0]["summary_text"]
            except:
                s = text[:200]
        else:
            s = text

        articles.append({
            "title": e.title,
            "link": e.link,
            "summary": s
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
