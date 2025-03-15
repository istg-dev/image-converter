from flask import Flask, request, send_from_directory
from PIL import Image
import os

app = Flask(__name__)

# Create an 'uploads' folder if it doesn't exist
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def upload_form():
    return '''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Fresh Convert</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #1e1e2f;
                color: #c9d1d9;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background: linear-gradient(145deg, #1a1a2e, #2e2e4f);
            }
            .container {
                width: 90%;
                max-width: 600px;
                text-align: center;
                background-color: #2e2e3f;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 8px 15px rgba(0, 0, 0, 0.5);
            }
            h1 {
                color: #58a6ff;
                font-size: 2.5em;
                margin-bottom: 20px;
            }
            form {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            input[type="file"] {
                padding: 10px;
                border-radius: 5px;
                background-color: #3a3a4a;
                color: #c9d1d9;
                cursor: pointer;
            }
            input[type="file"]::file-selector-button {
                content: "Browse for an image...";
                background-color: #3a3a4a;
                color: #c9d1d9;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            select, button {
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 1rem;
            }
            select {
                background-color: #3a3a4a;
                color: #c9d1d9;
            }
            button {
                background-color: #58a6ff;
                color: #ffffff;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            button:hover {
                background-color: #2d75cb;
            }
            footer {
                margin-top: 20px;
                font-size: 0.9rem;
                color: #7a8599;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>FReSh Image Convert</h1>
            <form action="/convert" method="post" enctype="multipart/form-data">
                <input type="file" name="image" required>
                <label for="format">Converting to...</label>
                <select name="format" id="format">
                    <option value="png">PNG</option>
                    <option value="jpeg">JPEG</option>
                    <option value="bmp">BMP</option>
                    <option value="ico">ICO</option>
                </select>
                <button type="submit">Convert</button>
            </form>
            <footer>Convert your images quickly and easily!</footer>
        </div>
    </body>
    </html>
    '''

@app.route('/convert', methods=['POST'])
def convert_image():
    file = request.files['image']
    output_format = request.form['format']

    # Save the uploaded image to the uploads folder
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    # Create the output file path
    output_path = os.path.splitext(input_path)[0] + f".{output_format}"

    # Convert the image
    image = Image.open(input_path)

    # Ensure compatibility for formats like JPEG and ICO
    if image.mode in ('P', 'RGBA'):
        image = image.convert('RGB')

    image.save(output_path)

    # Automatically download the file
    return send_from_directory(
        UPLOAD_FOLDER, os.path.basename(output_path), as_attachment=True
    )

if __name__ == '__main__':
    app.run(debug=True)
