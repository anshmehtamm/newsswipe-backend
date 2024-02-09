from boto3 import resource
from boto3.dynamodb.conditions import Key
from flask import jsonify, make_response
import config
import uuid
import time
AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
AWS_REGION = config.AWS_REGION

resource = resource('dynamodb',
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    region_name=AWS_REGION
                    )


def read_news_for_user(user_id):

    # check if user exists
    user_table = resource.Table('users')
    response = user_table.get_item(
        Key={
            'user_id': user_id
        }
    )
    if 'Item' not in response:
        return make_response(jsonify('User not found'), 404)

    news_table = resource.Table('news_articles')
    user_views_table = resource.Table('user_views')

    response = user_views_table.query(
        IndexName='user_id-index',  # Assuming GSI on user_id if user_id is not the PK
        KeyConditionExpression=Key('user_id').eq(user_id)
    )

    viewed_article_ids = [item['article_id'] for item in response['Items']]
    #response = news_table.query(IndexName='published_datetime-index', Limit=20, ScanIndexForward=False)
    response = news_table.scan()

    # Filter articles not in viewed_article_ids and sort by Publish_datetime
    articles = [item for item in response['Items'] if item['article_id'] not in viewed_article_ids]

    news_articles = []
    for item in articles:
        article = {
            'article_id': item['article_id'],
            'published_datetime': item['published_datetime'],
            'title': item['title'],
            'summary': item['summary'],
            'url': item['url'],
            'image_url': item['image_url'],
            'region': item['region'],
            'article_type': item['article_type']
        }
        news_articles.append(article)
    return make_response(jsonify(news_articles), 200)


def write_news_to_db(data):
    print('writing to db: total=%s' % len(data))
    table = resource.Table('news_articles')
    for article in data:
        response = table.put_item(
            Item={
                'article_id': str(article.article_id),
                'published_datetime': str(article.published_datetime),
                'title': article.article_title,
                'summary': article.article_summary,
                'url': article.url,
                'image_url': article.image_url,
                'region': article.article_region,
                'article_type': article.article_type
            }
        )
    return


def viewed_news(user, article_id):
    # check if user exists
    user_table = resource.Table('users')
    response = user_table.get_item(
        Key={
            'user_id': user
        }
    )
    if 'Item' not in response:
        return make_response(jsonify('User not found'), 404)

    table = resource.Table('user_views')
    response = table.put_item(
        Item={
            'view_id': str(uuid.uuid4()),  # Generate a unique view_id
            'user_id': user,
            'article_id': article_id,
            'viewed_datetime': str(int(time.time()))
        }
    )
    return make_response(jsonify('success'), 200)


def create_user(user_name):
    table = resource.Table('users')
    idd = str(uuid.uuid4())
    response = table.put_item(
        Item={
            'user_id': idd,  # Generate a unique user_id
            'user_name': user_name,
        }
    )
    return make_response(jsonify(idd), 200)