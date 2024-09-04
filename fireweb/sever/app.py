import os
from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

# 업로드된 파일을 저장할 디렉토리 설정
UPLOAD_FOLDER = 'static/uploads/'
##app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
##    if request.method == 'POST':
##        file = request.files['file']
##
##        if file:
##            # 파일 저장 경로 설정
##            filename = file.filename
##            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
##            file.save(filepath)
##            return render_template('index.html', filename=filename)
##    
    return render_template('index.html', filename=None)

if __name__ == '__main__':
    # 서버 실행
    #app.run(debug=False)
    app.run(host='0.0.0.0', port=1234)






##<!DOCTYPE html>
##<html lang="ko">
##<head>
##    <meta charset="UTF-8">
##    <meta name="viewport" content="width=device-width, initial-scale=1.0">
##    <title>사진 업로드</title>
##    <style>
##        body, html {
##            margin: 0;
##            padding: 0;
##            height: 100%;
##            display: flex;
##            flex-direction: column;
##            justify-content: center;
##            align-items: center;
##            background-color: #f0f0f0;
##        }
##        img {
##            max-width: 80%;
##            max-height: 80%;
##            object-fit: contain;
##            margin-bottom: 20px;
##        }
##        .buttons {
##            display: flex;
##            gap: 20px;
##            flex-wrap: wrap;
##        }
##        .buttons button {
##            padding: 20px 40px; /* 버튼 크기 확대 */
##            font-size: 24px; /* 폰트 크기 확대 */
##            background-color: #007BFF;
##            color: white;
##            border: none;
##            border-radius: 10px; /* 둥근 모서리 */
##            cursor: pointer;
##            transition: background-color 0.3s, transform 0.3s;
##        }
##        .buttons button:hover {
##            background-color: #0056b3;
##            transform: scale(1.1); /* 버튼에 마우스를 올렸을 때 크기 증가 */
##        }
##        .buttons button:active {
##            background-color: #004080;
##        }
##    </style>
##    <script>
##        const images = {
##            1: "{{ url_for('static', filename='uploads/1층.png') }}",
##            2: "{{ url_for('static', filename='uploads/2층.png') }}",
##            3: "{{ url_for('static', filename='uploads/3층.png') }}",
##            4: "{{ url_for('static', filename='uploads/4층.png') }}",
##            5: "{{ url_for('static', filename='uploads/5층.png') }}",
##            6: "{{ url_for('static', filename='uploads/6층.png') }}",
##            7: "{{ url_for('static', filename='uploads/7층.png') }}",
##            전체: "{{ url_for('static', filename='uploads/전체도.png') }}"
##        };
##
##        function showFloor(floor) {
##            const image = document.getElementById("image");
##            image.src = images[floor];
##        }
##    </script>
##</head>
##<body>
##    <img id="image" src="{{ url_for('static', filename='uploads/전체도.png') }}" alt="업로드된 이미지">
##    <div class="buttons">
##        <button onclick="showFloor(1)">1층</button>
##        <button onclick="showFloor(2)">2층</button>
##        <button onclick="showFloor(3)">3층</button>
##        <button onclick="showFloor(4)">4층</button>
##        <button onclick="showFloor(5)">5층</button>
##        <button onclick="showFloor(6)">6층</button>
##        <button onclick="showFloor(7)">7층</button>
##        <button onclick="showFloor('전체')">전체도</button>
##    </div>
##</body>
##</html>

