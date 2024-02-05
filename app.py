from flask import Flask
from flask import request
import controller as db
from errors import client_error

app = Flask(__name__)


@app.route('/news/<string:user>', methods=['GET'])
def news_for_user(user):
    if request.method == 'GET':
        try:
            #last_news_time = request.form.get('last_news')
            return db.read_news_for_user(user)
        except Exception as e:
            return client_error.ClientError(str(e), 500).message
    return client_error.ClientError('Invalid request method', 405).message


if __name__ == '__main__':
    app.run()
