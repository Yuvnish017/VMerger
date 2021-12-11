# Importing libraries...
from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

# creating Flask object and random secret key
app = Flask(__name__)
app.secret_key = os.urandom(24)

# folder name where the uploads will be stored
upload_folder = r'uploads'
app.config['UPLOAD_FOLDER'] = upload_folder

# uncomment the below line to impose restrictions on size of uploaded file
# app.config['MAX_CONTENT_LENGTH'] = 100*1024*1024

# allowed file extensions on the web page
allowed_extensions = ['.mp4', '.mkv', '.avi']

# for output file name
j = 0


def allowed_files(file_names):
    """
    to check if file extension is supported by the application
    :param file_names: name of the file
    :return: True/False based on whether the file has the correct extension or not
    """
    filename, extension = os.path.splitext(file_names)
    if extension in allowed_extensions:
        return True
    else:
        return False


@app.route('/')
def file_upload_page():
    """
    opens the homepage of the application
    """
    return render_template('file_upload_page.html')


@app.route('/uploaded_file', methods=['POST', 'GET'])
def process_files():
    """
    processes the uploaded files, merge them and save them in the uploads folder
    """

    # removing files from uploads folder to free up space
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))

    if request.method == 'POST':
        # check if no file was uploaded by the user
        if 'files[]' not in request.files:
            flash('No file selected')
            return redirect(url_for('file_upload_page'))

        # get the list of files uploaded
        files = request.files.getlist('files[]')
        file_names = []
        b = True
        for file in files:
            filename = secure_filename(file.filename)

            # check if files have the supported file extensions
            if not allowed_files(filename):
                b = False
            file_names.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        if not b:
            flash('File extension not supported')
            return redirect(url_for('file_upload_page'))

        output_video_name = video_merger(file_names)
        return redirect(url_for('download_file', output_file=output_video_name))


def video_merger(file_paths):
    """
    for merging video files
    :param file_paths: paths of video files to be merged
    :return: output file name
    """
    global j
    clips = []
    for i in file_paths:
        clips.append(VideoFileClip(i))
    final_video = concatenate_videoclips(clips)
    output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], str(j) + '.mp4')
    output_file_name = str(j)+'.mp4'
    j += 1

    # writing the output video file to the uploads folder
    final_video.write_videofile(output_file_path)
    return output_file_name


@app.route('/output_file/<output_file>')
def download_file(output_file):
    """
    opening download page once the files are processed
    """
    return render_template('download_video.html', output_file_path=output_file)


@app.route('/get_file/<file_name>')
def get_file(file_name):
    """
    for sending the required file from the directory
    :param file_name: file name
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], file_name, as_attachment=True)


if __name__ == '__main__':
    # running the app
    app.run(port='5004', debug=True)
