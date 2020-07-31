"""
Main Entry Point
"""

import os

from flask import Flask, request, redirect, url_for, render_template, send_file
from modelRunner.runner import imginp


UPLOAD_FOLDER = 'static/input/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMPLATES_AUTO_RELOAD'] = True



def make_static_dir():
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "static")):
        os.mkdir(os.path.join(os.path.dirname(__file__), "static"))
        subfolders = ["input", "output"]
        for sf_name in subfolders:
            os.makedirs(os.path.join("static", sf_name))
    return


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        files = request.files.getlist('file')
        if files[0].filename == '':
            return redirect(request.url)

        make_static_dir()
        for file in files:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        imginp(os.path.join(app.config['UPLOAD_FOLDER'], files[0].filename),
                        os.path.join(app.config['UPLOAD_FOLDER'], files[1].filename))
        return send_file('static/output/image.jpg', as_attachment=True, 
                                            attachment_filename='processed-image.jpg', cache_timeout=0)
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
