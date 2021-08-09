from flask import Flask, request, make_response
from flask_cors import CORS
from global_utils import insert_data_sign_up, insert_tweet_in_db, follow_unfollow, get_tweets
import json

app = Flask(__name__)
CORS(app)


@app.route("/api/sign-up", methods=['GET', 'POST'])
def sign_up():
    user_name = request.form.get("user_name")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    data = insert_data_sign_up(user_name=user_name, password=password, confirm_password=confirm_password)
    return make_response(json.dumps(data))


@app.route("/api/post-tweet", methods=['GET', 'POST'])
def post_tweet():
    tweet = request.form.get("tweet")
    user_id = request.form.get("user_id")
    data = insert_tweet_in_db(user_id=user_id, tweet=tweet)
    return make_response(json.dumps(data))


@app.route("/api/follow-unfollow-user", methods=['GET', 'POST'])
def follow_unfollow_user():
    user_id = request.form.get("user_id")
    following_id = request.form.get("following_id")
    type_ = request.form.get("type_")
    data = follow_unfollow(user_id=user_id, following_id=following_id, type_=type_)
    return make_response(json.dumps(data))


@app.route("/api/get-timeline-feed", methods=['GET', 'POST'])
def get_timeline_feed():
    user_id = request.form.get("user_id")
    data = get_tweets(user_id)
    return make_response(json.dumps(data))


@app.route("/api/get-follow-options", methods=['GET', 'POST'])
def get_follow_options():
    user_id = request.form.get("user_id")
    data = get_tweets(user_id)
    return make_response(json.dumps(data))


if __name__ == '__main__':
    app.run(debug="true", port=5999, host='0.0.0.0')
