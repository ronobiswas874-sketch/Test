from flask import Flask, request, jsonify
from instagrapi import Client
import os

app = Flask(__name__)

IG_USERNAME = "ginx_6016"
IG_PASSWORD = "ranojit1"
IG_SETTINGS = "ig_settings.json"


class InstagramAPI:
    def __init__(self):
        self.cl = Client()
        self.login()

    def login(self):
        if os.path.exists(IG_SETTINGS):
            self.cl.load_settings(IG_SETTINGS)
        self.cl.login(IG_USERNAME, IG_PASSWORD)
        self.cl.dump_settings(IG_SETTINGS)

    def get_user_info(self, username):
        try:
            user_id = self.cl.user_id_from_username(username)
            info = self.cl.user_info(user_id)

            followers = self.cl.user_followers(user_id, amount=10)
            following = self.cl.user_following(user_id, amount=10)

            return {
                "account": {
                    "username": info.username,
                    "full_name": info.full_name,
                    "biography": info.biography,
                    "followers": info.follower_count,
                    "following": info.following_count,
                    "posts": info.media_count,
                    "private": info.is_private,
                    "verified": info.is_verified,
                    "profile_pic": str(info.profile_pic_url),
                },

                "followers_list": [
                    {
                        "username": u.username,
                        "full_name": u.full_name
                    } for u in followers.values()
                ],

                "following_list": [
                    {
                        "username": u.username,
                        "full_name": u.full_name
                    } for u in following.values()
                ]
            }

        except Exception as e:
            return {"error": str(e)}


ig = InstagramAPI()


@app.route("/info", methods=["GET"])
def info():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "username query parameter is required"}), 400

    data = ig.get_user_info(username)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
