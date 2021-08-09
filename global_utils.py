from db_config import db_connection
import hashlib
import pandas as pd
import uuid


def insert_data_sign_up(user_name, password, confirm_password, following=''):
    db = db_connection()
    data = {}
    if confirm_password != password:
        data['status'] = "Failure"
        data["msg"] = "Password and Confirm password do not match"
        return data

    if len(password) < 5:
        data['status'] = "Failure"
        data["msg"] = "Password should be more than 5 character"
        return data

    duplicate_check = check_for_user_name(user_name)
    if duplicate_check == 0:
        data["status"] = "Failure"
        data["msg"] = "User Name already exist. Please provide a new one."
        return data

    data['msg'] = 'Success'
    password = encode_password(password)
    user_id = str(uuid.uuid4().hex)
    data["user_id"] = user_id
    sql_query = "INSERT INTO user(user_id, user_name, password, following)" \
                "VALUES('{}','{}','{}','{}')".format(user_id, user_name, password, following)
    cursor = db.cursor()
    cursor.execute(sql_query)
    db.commit()
    cursor.close()
    db.close()

    data["status"] = "Success"
    return data


def insert_tweet_in_db(user_id, tweet):
    db = db_connection()
    tweet_id = str(uuid.uuid4().hex)
    if not len(tweet):
        data = {"status": "Failure", "msg": "No text"}
        return data
    sql_query = "INSERT INTO tweet(tweet_id, user_id, tweet) VALUES('{}','{}','{}')".format(tweet_id, user_id, tweet)
    cursor = db.cursor()
    cursor.execute(sql_query)
    db.commit()
    cursor.close()
    db.close()
    data = {"status": "Success"}
    return data


def follow_unfollow(user_id, following_id, type_):
    db = db_connection()
    df = get_from_user(user_id)
    following_list_str = df["following"].values[0]
    if type_ == "follow":
        if not len(following_list_str):
            following_list = [following_id]
        else:
            following_list = following_list_str.split('||')
            following_list.append(following_id)
    elif type_ == "unfollow":
        following_list = following_list_str.split('||')
        following_list.remove(following_id)
    following_list_str = '||'.join([str(elem) for elem in following_list])
    sql_query = "UPDATE user SET following = '{}' WHERE user_id = '{}'".format(following_list_str, user_id)
    cursor = db.cursor()
    cursor.execute(sql_query)
    db.commit()
    cursor.close()
    db.close()
    data = {"status": "Success"}
    return data


def get_tweets(user_id):
    df = get_from_user(user_id)
    following_list_str = df["following"].values[0]
    user_list = [user_id]
    if len(following_list_str):
        following_list = following_list_str.split('||')
        user_list.extend(following_list)
    tweets_dict = get_from_tweet(user_list=user_list)
    return tweets_dict


def get_from_tweet(user_list):
    db = db_connection()
    sql_query = "SELECT tweet.user_id, tweet.tweet, tweet.tweet_id, user.user_name FROM tweet INNER JOIN user ON " \
                "tweet.user_id = user.user_id WHERE "
    for i in range(len(user_list)):
        if i == len(user_list)-1:
            query = "tweet.user_id='{}'".format(user_list[i]) + " ORDER BY tweet.created_at DESC"
        else:
            query = "tweet.user_id='{}' OR ".format(user_list[i])
        sql_query += query

    df = pd.read_sql(sql_query, db)
    db.close()
    return df.to_dict(orient='record')


def get_from_user(user_id):
    db = db_connection()
    sql_query = "SELECT * FROM user WHERE user_id = '{}'".format(user_id)
    df = pd.read_sql(sql_query, db)
    db.close()
    return df


def encode_password(password):
    result = hashlib.md5(password.encode())
    password = result.hexdigest()
    return password


def check_for_user_name(user_name):
    sql_query = "Select * from user where user_name = '{}'".format(user_name)
    db = db_connection()
    df = pd.read_sql(sql_query, db)
    db.close()
    if len(df) == 0:
        return 1
    else:
        return 0