from flask import Flask, render_template, request, redirect, url_for
from rembg import remove
from PIL import Image
import os



app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/output'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('image')
    if file and file.filename != '':
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_filename = 'no_bg_' + file.filename
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        file.save(input_path)

        with Image.open(input_path) as img:
            result = remove(img)
            result.save(output_path)

        # Redirect to result page to show processed image
        return redirect(url_for('result', filename=output_filename))

    return "No file uploaded."

@app.route('/result/<filename>')
def result(filename):
    return render_template('result.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
