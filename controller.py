from boto3 import resource
import config


AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
AWS_REGION = config.AWS_REGION


resource = resource('dynamodb',
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    region_name=AWS_REGION
                    )

def read_news_for_user(user):
    table = resource.Table('news_articles')
    response = table.get_item(
        Key={
            'article_id': user, 'published_datetime': 'test'
        }
    )
    return response