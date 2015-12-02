#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from requests_oauthlib import OAuth1Session
import ftputil

# myfile
import ftpauth


class MyTwitterLib(object):

    # 認証
    def __init__(self, CK, CS, AT, AS):
        self.session = OAuth1Session(CK, CS, AT, AS)

    # TL取得
    def get_timeline(self, num):
        url = "https://api.twitter.com/1.1/statuses/home_timeline.json"

        _ftp = ftputil.FTPHost(ftpauth.host, ftpauth.user, ftpauth.pwd)
        print("FTP Access Succeeded.")

        if _ftp.path.exists("./since_id_tl.txt"):
            with _ftp.open("./since_id_tl.txt") as f:
                since_id = f.readline()
            params = {"count": num, "since_id": since_id}
        else:
            since_id = ""
            params = {"count": num}

        # OAuthでGETメソッドを用いてタイムラインを取得
        req = self.session.get(url, params=params)

        # 取得成功
        if req.status_code == 200:
            # json形式で取得したタイムラインをパース
            timeline = list(map(Tweet, json.loads(req.text)))

            if timeline != []:
                with _ftp.open("./since_id_tl.txt", "w") as f:
                    f.write(timeline[0].tweet_id)

            return timeline

        # 取得失敗
        else:
            print(
                "Error code {}: Failed to get timeline.".format(req.status_code))
            return None

    # mention取得
    def get_mentions(self, num):
        url = "https://api.twitter.com/1.1/statuses/mentions_timeline.json"

        # 最後に取得したmentionのIDを取得
        _ftp = ftputil.FTPHost(ftpauth.host, ftpauth.user, ftpauth.pwd)
        if _ftp.path.exists("./since_id_m.txt"):
            with _ftp.open("./since_id_m.txt") as f:
                since_id = f.readline()
            params = {"count": num, "since_id": since_id}
        else:
            since_id = ""
            params = {"count": num}

        # OAuthでGETメソッドを用いてタイムラインを取得
        req = self.session.get(url, params=params)

        # 取得成功
        if req.status_code == 200:
            # json形式で取得したタイムラインをパース
            mentions = list(map(Tweet, json.loads(req.text)))

            # 取得した最新のmentionのIDを記録
            if mentions != []:
                _ftp = ftputil.FTPHost(ftpauth.host, ftpauth.user, ftpauth.pwd)
                with _ftp.open("./since_id_m.txt", "w") as f:
                    f.write(mentions[0].tweet_id)

            return mentions

        # 取得失敗
        else:
            return None

    # ツイート
    def tweet(self, text):
        url = "https://api.twitter.com/1.1/statuses/update.json"
        params = {"status": text}

        req = self.session.post(url, params=params)

        return req.status_code

    # リプライ
    def reply(self, to_mention, text):
        url = "https://api.twitter.com/1.1/statuses/update.json"
        params = {"status": "@" + to_mention.user_id + " " + text,
                  "in_reply_to_status_id": to_mention.tweet_id}

        req = self.session.post(url, params=params)

        return req.status_code



class Tweet(object):

    def __init__(self, req):
        self.text = req["text"]
        self.time = req["created_at"]
        self.user_name = req["user"]["name"]
        self.user_id = req["user"]["screen_name"]
        self.tweet_id = req["id_str"]
        self.reply_id = req["in_reply_to_screen_name"]


# test
if __name__ == '__main__':
    import auth
    twitter = MyTwitterLib(auth.CK, auth.CS, auth.AT, auth.AS)

    timeline = twitter.get_timeline(10)
    print(timeline)
    for tl in timeline:
        print(tl.__dict__)
        print("")

    mentions = twitter.get_mentions(10)
    print(mentions)
    for m in mentions:
        print(m.__dict__)
        print("")
    # twitter.tweet("ツイートテスト")
