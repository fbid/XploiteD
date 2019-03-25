import secrets
import os
from flask import current_app
from PIL import Image

def get_rnd_filename(fname):
    '''Returns the full path for the picture with a new random filename'''
    _, f_ext = os.path.splitext(fname)
    return secrets.token_hex(8) + f_ext


def save_post_pic(form_pic):
    '''Saves a downscaled version of the submitted user picture to the filesystem'''
    new_fname = get_rnd_filename(form_pic.filename)
    new_pic_path = os.path.join(current_app.root_path, 'static/assets/posts', new_fname)
    form_pic.save(new_pic_path) # saves picture to fs

    return new_fname
