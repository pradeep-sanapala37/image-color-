from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
from werkzeug.utils import secure_filename
import os
from deoldify import device
from deoldify.device_id import DeviceId
from deoldify.visualize import get_image_colorizer, get_video_colorizer
import torch

torch.cuda.empty_cache()

app = Flask(__name__)

# Configure upload and result folders
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_IMAGES'] = 'result_images'
app.config['RESULT_VIDEOS'] = 'result_videos'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov'}

# Initialize DeOldify colorizers
device.set(device=DeviceId.GPU0)
image_colorizer = get_image_colorizer(artistic=True)
video_colorizer = get_video_colorizer()

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_IMAGES'], exist_ok=True)
os.makedirs(app.config['RESULT_VIDEOS'], exist_ok=True)

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about_project')
def about_project():
    return render_template('about_project.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')
@app.route('/colorize_image', methods=['POST'])
def colorize_image():
    render_factor = int(request.form.get('render_factor', 35))
    watermarked = request.form.get('watermarked') == 'on'

    uploaded_file = request.files['source_image']
    if uploaded_file.filename == '':
        return redirect(url_for('index'))

    if allowed_file(uploaded_file.filename, ALLOWED_IMAGE_EXTENSIONS):
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(file_path)

        # Colorize the image
        colorized_image_path = image_colorizer.get_transformed_image(
            path=file_path, render_factor=render_factor, watermarked=watermarked
        )

        # Save colorized image in result_images
        colorized_image_filename = os.path.join(app.config['RESULT_IMAGES'], 'result.png')
        colorized_image_path.save(colorized_image_filename)

        return render_template('result.html', image_filename='result.png')
    else:
        return "Invalid image format."

@app.route('/colorize_video', methods=['POST'])
def colorize_video():
    render_factor = int(request.form.get('render_factor', 35))
    watermarked = request.form.get('watermarked') == 'on'

    uploaded_file = request.files['source_video']
    if uploaded_file.filename == '':
        return redirect(url_for('index'))

    if allowed_file(uploaded_file.filename, ALLOWED_VIDEO_EXTENSIONS):
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(file_path)

        # Ensure absolute path for video colorizer
        absolute_file_path = os.path.abspath(file_path)
        
        # Colorize the video
        colorized_video_path = video_colorizer.colorize_from_file_name(
            absolute_file_path, render_factor=render_factor, watermarked=watermarked
        )

        # Save the colorized video in result_videos
        colorized_video_filename = os.path.join(app.config['RESULT_VIDEOS'], 'result.mp4')
        os.rename(colorized_video_path, colorized_video_filename)

        return render_template('result.html', video_filename='result.mp4')
    else:
        return "Invalid video format."

# Route to serve colorized image
@app.route('/result_images/<filename>')
def get_result_image(filename):
    return send_from_directory(app.config['RESULT_IMAGES'], filename)

# Route to download the colorized image
@app.route('/download_result_image/<filename>')
def download_result_image(filename):
    return send_file(os.path.join(app.config['RESULT_IMAGES'], filename), as_attachment=True)

# Route to serve colorized video
@app.route('/result_videos/<filename>')
def get_result_video(filename):
    return send_from_directory(app.config['RESULT_VIDEOS'], filename)

# Route to download colorized video
@app.route('/download_result_video/<filename>')
def download_result_video(filename):
    return send_file(os.path.join(app.config['RESULT_VIDEOS'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
