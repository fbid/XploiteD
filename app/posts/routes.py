from flask import Blueprint
from flask import redirect, request, url_for, flash, abort, render_template
from flask_login import current_user, login_required
from app import db
from app.posts.forms import NewPostForm
from app.models.post import Post
from app.posts.utils import save_post_pic

posts = Blueprint('posts', '__name__')

@posts.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = NewPostForm()

    if form.validate_on_submit():
        new_pic_fname = save_post_pic(form.post_img.data)

        new_post = Post(image_file=new_pic_fname, title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash('Post succesfully submitted', 'success')
        return redirect(url_for('main.home'))

    return render_template('posts/new_post.html', title='New Post', form=form, legend='New Post')

@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    if post:
        return render_template('posts/post.html', title=post.title, post=post)
    else:
        pass

@posts.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = NewPostForm()
    post = Post.query.get_or_404(post_id)

    # Post not found in the db
    if post.author != current_user:
        abort(403)

    # Get post edit page
    if request.method == 'GET':
        # Filling in the form
        form.title.data = post.title
        form.content.data = post.content
        return render_template('posts/new_post.html', title='Update Post', form=form, legend='Update Post')

    # Post request when submitting the form from post edit page
    elif request.method == 'POST':
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash('The post has been succesfully edited', 'success')
            return redirect(url_for('posts.post',post_id=post.id))

@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Post not found in the db
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()

    flash('Post succesfully deleted', 'success')
    return redirect(url_for('main.home'))
