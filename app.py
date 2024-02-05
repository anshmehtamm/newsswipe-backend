from flask import Flask
from flask import request
from news_fetch import fetch_news_for_user
from client_error import ClientError

app = Flask(__name__)


@app.route('/news/<string:user>', methods=['GET'])
def news_for_user(user):
    if request.method == 'GET':
        last_news_time = request.form.get('last_news')
        # get the news for the user
        return fetch_news_for_user(user, last_news_time)
    return ClientError('Invalid request method', 405)


if __name__ == '__main__':
    app.run()
