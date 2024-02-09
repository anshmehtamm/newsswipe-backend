from gnews import GNews
import newspaper
from newsarticle import NewsArticle
def top_latest_news():

    google_news = GNews()
    top_news = google_news.get_top_news()
    errorCount = 0
    data = []
    for news in top_news:
        try:
            article = newspaper.Article(url="%s" % news['url'], language='en')
            article.download()
            article.parse()
        except Exception as error:
            # TODO: logging to cloudwatch
            errorCount += 1
            continue
        article.nlp()
        article_data = NewsArticle(title=article.title,
                                   summary=article.summary,
                                   url=article.url,
                                   image_url=article.top_image,
                                   published_datetime=news['published date'],
                                   region="us",
                                   article_type="news")
        data.append(article_data)
    return data


if __name__ == '__main__':
    top_latest_news()
