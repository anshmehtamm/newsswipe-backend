import boto3


def fetch_news_for_user(user, last_news_time):


    # connect to the database (AwsDynamoDB - url)
    dynamodb = boto3.resource('dynamodb')
    # url and key

    # get the table
    table = dynamodb.Table('news')


    # get the news for the user
    # return the news
