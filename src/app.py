from flask import Flask, render_template

from core.settings import config
from db.service import get_some_post, get_all_tags, session


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/all")
def index():
    posts = get_some_post(session)
    for post in posts:
        post.text = post.text[0:500]
    tags = get_all_tags(session)
    return render_template("index.html", post_list=posts, tag_list=tags)


@app.route("/post")
def post():
    posts = get_some_post(session)
    tags = get_all_tags(session)
    return render_template("post.html", post_list=posts, tag_list=tags)


if __name__ == "__main__":
    app.config["SECRET_KEY"] = config["app_key"]
    app.run(host="0.0.0.0", port=5000, debug=config["debug"])
