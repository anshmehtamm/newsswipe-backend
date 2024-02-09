from flask import Flask
from flask import request
import controller as db
import client_error
from flask_apscheduler import APScheduler
from schedule_job_config import JobConfig


def configure_scheduler():
    global scheduler
    app.config.from_object(JobConfig())
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()


app = Flask(__name__)
configure_scheduler()

#
# @scheduler.task('interval', id='do_job_1', seconds=60, misfire_grace_time=900)
# def job1():
#     data = top_latest_news()
#     db.write_news_to_db(data)


@app.route('/news/<string:user>', methods=['GET'])
def news_for_user(user):
    if request.method == 'GET':
        try:
            # last_news_time = request.form.get('last_news')
            return db.read_news_for_user(user)
        except Exception as e:
            return client_error.ClientError(str(e), 500).message
    return client_error.ClientError('Invalid request method', 405).message

#
@app.route('/news/viewed/<string:user>/<string:article_id>', methods=['GET'])
def viewed_news(user, article_id):
    if request.method == 'GET':
        return db.viewed_news(user, article_id)
    return client_error.ClientError('Invalid request method', 405).message

@app.route('/news/create/<string:user_name>', methods=['GET'])
def create_user(user_name):
    if request.method == 'GET':
        if len(user_name) > 0 and len(user_name) < 20 and user_name.isalnum():
            return db.create_user(user_name)
        else:
            return client_error.ClientError('Invalid user name', 400).message
    return client_error.ClientError('Invalid request method', 405).message





if __name__ == '__main__':
    app.run()
