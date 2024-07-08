from flask import Flask, render_template, request, send_from_directory
import os
from PIL import Image
import webbrowser
import random
import string

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ASCII_FOLDER = 'ascii_art'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ASCII_FOLDER, exist_ok=True)

def image_to_ascii(image_path):
    try:
        # 이미지 열기
        image = Image.open(image_path)

        # 이미지를 그레이스케일로 변환
        image = image.convert("L")

        # 이미지 크기 조정 (선택 사항)
        aspect_ratio = image.width / image.height
        new_width = 100
        new_height = int(new_width / aspect_ratio * 0.55)  # 조정 가능한 비율
        image = image.resize((new_width, new_height))

        # 픽셀 밝기에 따른 아스키 문자 매핑
        ascii_chars = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

        # ASCII 아트 생성
        ascii_art = ""
        for pixel in image.getdata():
            ascii_art += ascii_chars[pixel // 4]

        return ascii_art
    except Exception as e:
        print(f"Error converting image to ASCII: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            img_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(img_path)

            ascii_art = image_to_ascii(img_path)
            if ascii_art:
                ascii_file = os.path.join(ASCII_FOLDER, f"ascii_{os.path.splitext(file.filename)[0]}.txt")
                with open(ascii_file, 'w') as f:
                    f.write(ascii_art)

                return render_template('index.html', original_img=file.filename, ascii_img=f"ascii_{os.path.splitext(file.filename)[0]}.txt")
            else:
                return "Error processing image", 500

    return render_template('index.html')

@app.route('/uploads/<filename>')
def send_uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/ascii-art/<filename>')
def send_ascii_file(filename):
    return send_from_directory(ASCII_FOLDER, filename)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    open_browser()
    app.run(debug=True)
