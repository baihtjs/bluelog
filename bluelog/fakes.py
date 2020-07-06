from random import random
from sqlite3 import IntegrityError

from faker import Faker

from bluelog.extensions import db
from models import Admin, Category, Post, Comment


def fake_admim():
    admin = Admin(
        username = 'admin',
        blog_title = 'Bluelog',
        blog_sub_title = "No, I'm the real thing.",
        name = 'Mima Jirigoe',
        about = 'Um, Mima Kirigoem, had a fun time as a member of CHAM...'
    )
    admin.set_password('helloflask')
    db.session.add(admin)
    db.session.commit()

fake = Faker()
def fake_categories(count=10):
    category = Category(name='Default')
    db.session.add(category)
    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def fake_post(count=50):
    post = Post(title=fake.sentence(),
                body=fake.text(2000),
                catepory=Category.query.get(random.randint(1, Category.query.count())),
                timestamp = fake.date_time_this_year()
    )
    db.session.add(post)
    db.session.commit()

def fake_comments(count=50):
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    salt = int(count*0.1)
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
        comment = Comment(
            author='Mima Kirigoe',
            email='emima@example.com',
            site='example.com',
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()
