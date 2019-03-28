import secrets
import os
from flask import url_for, current_app
from app import mail
from PIL import Image
from flask_mail import Message

def get_rnd_filename(fname):
    '''Returns the full path for the picture with a new random filename'''
    _, f_ext = os.path.splitext(fname)
    return secrets.token_hex(8) + f_ext

def resize_img(pic, width, height):
    '''Returns the resized img file'''
    output_size = (width, height)
    img = Image.open(pic)
    img.thumbnail(output_size)
    return img

def delete_old_pic(f_path, folder_name=None):
    '''Deletes old user picture from filesystem'''
    if f_path == 'default.svg':
        # avoids default user pic removal
        return

    if not folder_name:
        old_pic_path = os.path.join(current_app.root_path, 'static/assets/users', f_path)
    else:
        old_pic_path = os.path.join(current_app.root_path, 'static/assets',folder_name, f_path)

    if os.path.exists(old_pic_path):
        print(f'File: {old_pic_path} succesfully deleted!')
        os.remove(old_pic_path)


def save_new_user_pic(form_pic):
    '''Saves a downscaled version of the submitted user picture to the filesystem'''
    new_fname = get_rnd_filename(form_pic.filename)
    new_pic_path = os.path.join(current_app.root_path, 'static/assets/users', new_fname)
    r_pic = resize_img(form_pic, 200, 200)
    r_pic.save(new_pic_path) # saves picture to fs

    return new_fname


def send_reset_email(user):
    token = user.get_psw_reset_token()
    reset_link = url_for('users.reset_password', token=token, _external=True )

    message = Message('Password reset request', sender='devtest889900@gmail.com')
    message.add_recipient(user.email)
    message.body = 'We received your password reset request.\n' \
    + 'Please click on the link below in order to reset your password:\n\n' \
    + reset_link  # external to get the absolute url path

    print(f'Link to reset the password: {reset_link}')
    # Not working
    #mail.send(message)
