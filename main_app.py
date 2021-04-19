from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

app = Flask(__name__)
app.secret_key = os.urandom(24)
upload_folder = r'uploads'
app.config['UPLOAD_FOLDER'] = upload_folder
allowed_extensions = ['.mp4', '.mkv', '.avi']
j = 0


def allowed_files(file_names):
    filename, extension = os.path.splitext(file_names)
    print(extension)
    if extension in allowed_extensions:
        return True
    else:
        return False


@app.route('/')
def file_upload_page():
    return render_template('file_upload_page.html')


@app.route('/uploaded_file', methods=['POST', 'GET'])
def process_files():
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))

    if request.method == 'POST':
        print('Yes')
        if 'files[]' not in request.files:
            flash('No file selected')
            return redirect(url_for('file_upload_page'))
        files = request.files.getlist('files[]')
        print('Received files')
        file_names = []
        b = []
        for file in files:
            print(file.filename)
            filename = secure_filename(file.filename)
            if allowed_files(filename):
                b.append(1)
            else:
                b.append(0)
            file_names.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        print(all(x == 1 for x in b))
        if not all(x == 1 for x in b):
            flash('File extension not supported')
            return redirect(url_for('file_upload_page'))

        output_video_name = video_merger(file_names)
        return redirect(url_for('download_file', output_file=output_video_name))


def video_merger(file_paths):
    global j
    clips = []
    for i in file_paths:
        clips.append(VideoFileClip(i))
    final_video = concatenate_videoclips(clips)
    output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], str(j) + '.mp4')
    output_file_name = str(j)+'.mp4'
    j += 1
    final_video.write_videofile(output_file_path)
    return output_file_name


@app.route('/output_file/<output_file>')
def download_file(output_file):
    return render_template('download_video.html', output_file_path=output_file)


@app.route('/get_file/<file_name>')
def get_file(file_name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], file_name, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
