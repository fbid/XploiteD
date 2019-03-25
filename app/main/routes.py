from flask import Blueprint
from flask import request, render_template, send_from_directory, render_template_string, request
from app.models.post import Post

main = Blueprint('main', '__name__')

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int) # default page=1
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
    return render_template('home.html', posts=posts)

@main.route('/about')
def about():
    return render_template('about.html', title='About Us')

@main.route('/robots.txt')
def static_from_root():
    return send_from_directory('static', request.path[1:])

@main.app_errorhandler(404)
def page_not_found(e):
    template = '''{% extends "base.html" %}
{% block content %}
<div class="flex-grow error center-content">
    <h1>Oops! That page doesn't exist.</h1>
    <h3>'''+request.url+'''</h3>
</div>
{% endblock %}'''
    return render_template_string(template), 404
