import uuid
import datetime
import time



class NewsArticle:
    article_id = None
    article_title = None
    article_summary = None
    url = None
    image_url = None
    published_datetime = None
    article_region = None
    article_type = None

    def __init__(self, title=None,
                 summary=None,
                 url=None,
                 image_url=None,
                 published_datetime=None,
                 region=None,
                 article_type=None, article_id=None):
        if article_id is not None:
            self.article_id = article_id
        else:
            self.article_id = uuid.uuid5(uuid.NAMESPACE_URL, url)
        self.article_title = title
        self.article_summary = summary
        self.url = url
        self.image_url = image_url
        # convert datetime to epoch
        if published_datetime is not None:
            # format 'Tue, 06 Feb 2024 18:17:27 GMT'
            try:
                published_datetime = int(time.mktime(datetime.datetime.strptime(published_datetime,
                                                                                "%a, %d %b %Y %H:%M:%S %Z")
                                                     .timetuple()))
                self.published_datetime = published_datetime
            except ValueError:
                self.published_datetime = published_datetime
        self.article_region = region
        self.article_type = article_type

    def __str__(self):
        return f"{self.article_title}\n"
