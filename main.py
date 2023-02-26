import os
import tweepy
import mail
from datetime import datetime, timezone, timedelta

# 認証に必要なキーとトークン
API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]


class tweet:
    created_at = ""
    text = ""


def search_tweet():
    # 戻り値
    tweet_list = []

    # APIの認証
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # 特定ユーザのタイムラインを取得
    api = tweepy.API(auth)
    timelines = api.user_timeline(screen_name=os.environ["USER_ID"])

    if len(timelines) != 0:

        # 1時間前の時刻を取得
        latest_date = datetime.now(timezone.utc) + timedelta(hours=-1)

        for tl in timelines:
            if tl.created_at >= latest_date:
                t = tweet()
                t.created_at = tl.created_at
                t.text = tl.text
                tweet_list.append(t)

    return tweet_list


if __name__ == "__main__":
    tweet_list = search_tweet()
    if len(tweet_list) != 0:
        text = ""
        count = len(tweet_list)
        for t in tweet_list:
            # タイムゾーン変更(UTC->JST)
            t.created_at = t.created_at.astimezone(timezone(timedelta(hours=+9)))
            text = text + "投稿日時:{}\n{}\n".format(t.created_at, t.text)
            text = text + "----------\n"
        mail.send_mail(text, count)
