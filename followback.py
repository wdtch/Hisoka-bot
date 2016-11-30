import json
import os
from requests_oauthlib import OAuth1Session

def followback():
    session = OAuth1Session(os.getenv("CK"),
                            os.getenv("CS"),
                            os.getenv("AT"),
                            os.getenv("AS"))

    get_url = "https://api.twitter.com/1.1/followers/list.json"
    get_params = {"screen_name": "hisoka_trumpbot", "count": "100"}

    get_req = session.get(get_url, params=get_params)
    followers_text = json.loads(get_req.text)

    follow_url = "https://api.twitter.com/1.1/friendships/create.json"
    for follower in followers_text["users"]:
        if not follower["following"]:
            follow_params = {"user_id": follower["id"]}
            follow_req = session.post(follow_url, params=follow_params)