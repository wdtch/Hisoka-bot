#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from requests_oauthlib import OAuth1Session

class MyTwitterLib(object):

    # 認証(やり方要検討)
    def __init__(self, CK, CS, AT, AS):
        self.session = OAuth1Session(CK, CS, AT, AS)
        self._since_id_tl = ""
        self._since_id_m = ""

    # TL取得
    def get_timeline(self, num=None, since_id=None, recording_since_id=True):
        url = "https://api.twitter.com/1.1/statuses/home_timeline.json"

        if num is not None:
            if since_id is not None:
                params = {"count" : num, "since_id" : since_id}
            else:
                params = {"count" : num}
        else:
            if since_id is not None:
                params = {"since_id" : since_id}
            else:
                params = {}

        # OAuthでGETメソッドを用いてタイムラインを取得
        req = self.session.get(url, params=params)

        # 取得成功
        if req.status_code == 200:
            # json形式で取得したタイムラインをパース
            timeline = list(map(Tweet, json.loads(req.text)))

            if timeline != [] and recording_since_id:
                self._since_id_tl = timeline[0].tweet_id

            return timeline

        # 取得失敗
        else:
            print("Error code {}: Failed to get timeline.".format(req.status_code))
            return None

    # mention取得
    def get_mentions(self, num=None, since_id=None, recording_since_id=True):
        url = "https://api.twitter.com/1.1/statuses/mentions_timeline.json"

        if num is not None:
            if since_id is not None:
                params = {"count" : num, "since_id" : since_id}
            else:
                params = {"count" : num}
        else:
            if since_id is not None:
                params = {"since_id" : since_id}
            else:
                params = {}

        # OAuthでGETメソッドを用いてタイムラインを取得
        req = self.session.get(url, params=params)

        # 取得成功
        if req.status_code == 200:
            # json形式で取得したタイムラインをパース
            mentions = list(map(Tweet, json.loads(req.text)))

            if mentions != [] and recording_since_id:
                self._since_id_m = mentions[0].tweet_id

            return mentions

        # 取得失敗
        else:
            print("Error code {}: Failed to get mentions.".format(req.status_code))
            return None

    # ツイート
    def tweet(self, text):
        url = "https://api.twitter.com/1.1/statuses/update.json"
        params = {"status": text}

        req = self.session.post(url, params=params)

        # ツイート成功
        if req.status_code == 200:
            return 0
        else:
            print("Error code {}: Failed to tweet.")
            return -1



class Tweet(object):

    def __init__(self, req):
        self.text = req["text"]
        self.time = req["created_at"]
        self.user_name = req["user"]["name"]
        self.user_id = req["user"]["screen_name"]
        self.tweet_id = req["id_str"]
        self.reply_id = req["in_reply_to_screen_name"]

    # リプライ
    def reply(self, text):
        url = "https://api.twitter.com/1.1/statuses/update.json"
        params = {"status": text, "in_reply_to_status_id": self.tweet_id}

        req = self.session.post(url, params=params)

        # ツイート成功
        if req.status_code == 200:
            return 0
        else:
            print("Error code {}: Failed to reply.")
            return -1

# test
if __name__ == '__main__':
    import auth
    twitter = MyTwitterLib(auth.CK, auth.CS, auth.AT, auth.AS)

    with open("since_id.txt", "r") as f:
        since_id = f.readline()

    for tl in twitter.get_timeline(10):
        print(tl.__dict__)

    for m in twitter.get_mentions(num=10, since_id=since_id):
        print(m.__dict__)
    twitter.tweet("ツイートテストだお")