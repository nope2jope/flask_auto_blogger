from flask import Flask, render_template
from post_class import Post
import datetime
import requests

year_today = datetime.datetime.now().year

application = Flask(__name__)

all_posts = requests.get('https://api.npoint.io/e0eb025823d97820e87d').json()

@application.route('/')
def homepage():
    return render_template('index.html', year=year_today)


@application.route('/guess/<username>')
def medium(username):
    request_age = requests.get(f'https://api.agify.io?name={username}')
    request_age.raise_for_status()
    user_age = request_age.json()['age']

    request_gender = requests.get(f'https://api.genderize.io?name={username}')
    request_gender.raise_for_status()
    user_gender = request_gender.json()['gender']

    return render_template('guesser.html', name=username.capitalize(), age=user_age, gender=user_gender)

@application.route('/blog')
def blogger():
    return render_template('blog.html', blog_posts=all_posts, year=year_today)

@application.route('/post<int:num>')
def fetch_post(num):
    selected_post = None
    for post in all_posts:
        if post['id'] == num:
            selected_post = post

    return render_template('posts.html', post=selected_post, num_choice=num, year=year_today)



if __name__ == '__main__':
    application.run(debug=True)
