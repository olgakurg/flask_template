from sqlalchemy import create_engine, func

from sqlalchemy.orm import (
    Session as SessionType,
    sessionmaker,
    scoped_session,
)

from db.models import User, Tag, Post, Tag_Post, Base
from datetime import datetime
from werkzeug.security import generate_password_hash
from core.settings import config
from core.logger import logger

engine = create_engine(url=config["dsl"])
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
Base.metadata.create_all(bind=engine)
session: SessionType = Session()


def create_user(session, username, password):
    hash = generate_password_hash(password)
    user = User(username=username, _password=hash)
    session.add(user)
    return user


def create_users(session, usernames):
    users = []
    for username in usernames:
        user = User(username=username)
        session.add(user)
        users.append(user)

    return users


def get_all_users(session):
    users = session.query(User).order_by(User.id).all()
    return users


def get_user_by_username(session, username):
    user = session.query(User).filter_by(username=username).one_or_none()
    return user


def get_user_by_id(session, user_id):
    user = session.get(User, user_id)
    return user


def get_users_by_username_match(session, username_part):
    users = session.query(User).filter(User.username.ilike(f"%{username_part}%")).all()
    return users


def update_username_by_id(session, user_id, new_username):
    user = session.get(User, user_id)
    user.username = new_username
    session.add(user)
    session.flush()
    return user


def get_tag_by_caption(session, caption):
    tag = session.query(Tag).filter(Tag.caption == caption).first()
    return tag


def create_tag(session, caption):
    existed_tag = get_tag_by_caption(session, caption)

    if existed_tag is not None:
        return existed_tag
    else:
        tag = Tag(caption=caption)
        session.add(tag)
        return tag.id


def create_tags(session, captions):
    tags = []
    for caption in captions:
        tag = create_tag(session, caption)
        tags.append(tag)

    return tags


def get_tag_by_id(session, tag_id):
    tag = session.get(Tag, tag_id)
    return tag


def create_post(session, caption, text, user_id, tag_List):
    post = Post(title=caption, text=text, user_id=user_id)
    session.add(post)

    if tag_List != []:
        tags = []
        for caption in tag_List:
            tag = create_tag(session, caption)
            tags.append(tag)

        post.tags = tags

    return post.id


def update_post_by_id(session, post_id):
    post = session.get(Post, post_id)
    session.add(post)
    return post


def get_posts_by_user_id(session, user_id):
    posts = session.query(Post).filter(Post.user_id == user_id).all()
    return posts


def get_posts_by_tag_id(session, tag_id):
    posts = session.query(Post).filter(Post.tags == tag_id).all()
    return posts


def get_posts_with_two_tags(session, user_id):
    query = (
        session.query(Tag_Post.post_id)
        .join(Post)
        .where(Post.user_id == user_id)
        .group_by(Tag_Post.post_id)
        .having(func.count(Tag_Post.tag_id) == 2)
    )
    post_ids = query.all()
    return post_ids


def get_all_tags(session):
    proxy_res = session.query(Tag).all()
    tags = [res for res in proxy_res]
    return tags


def get_some_post(session):
    logger.info("it works!")
    posts = []
    try:
        post = session.query(Post).where(Post.id == 1).one_or_none()
        posts.append(post)
    except Exception as e:
        logger.debug(e)
    return posts


def get_latest_posts(session):
    posts = []
    post = session.query(Post).where(Post.created_at < datetime.utcnow).limit(3).all()
    posts.append(post)
    return posts


def fake_filling():
    from faker import Faker

    fake = Faker()
    Base.metadata.drop_all()
    Base.metadata.create_all()
    with session.begin():
        username = fake.name()
        Faker.seed(0)
        password = fake.pystr(min_chars=3, max_chars=7)
        two_tags = [fake.pystr() for _ in range(1)]
        create_user(session, username, password)
        create_tags(session, two_tags)
        session.flush()
        create_post(session, "post_caption", "test_post", 1, two_tags)
        session.commit()
