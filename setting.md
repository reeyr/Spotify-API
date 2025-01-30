1. Flask로 HTML 웹 구성하기
   - return_template 이용하기: .html 파일을 text 형태로 반환해줌
     
     (1) from flask import Flask, render_template
         app = Flask(_name_)
     
     (2) templates 폴더 추가:
     render_template을 사용할 모든 파일은 templates 폴더 내에 존재해야 함
     
     *폴더 경로 확인
      SPOTIFY API/
     
      │── app.py  (Flask 실행 파일)
     
      │── .env
     
      │── templates/
     
      │   ├── index.htm
     

   - HTML 파일 연결
     (1) app.route():
     바로 아래 함수가 리턴하는 문장 그대로 HTML 형식으로 변환됨
     
     (html 파일 -> text 형태 변환 = render_template)
     
     ex)
     @app.route("/")
     def hello_world():
         return render_template('index.html')
     
     --> render_template() 사용
     
     @app.route("/")
     def hello_world():
         return "p> Hello, World!</p"
     
     --> p>태그로 문장 그대로 출력
     

2. Flask 서버 연결
   (1) cmd에서 프로젝트 폴더로 이동:
   cmd > cd "프로젝트 폴더 경로" (py 파일이 있는 곳)
   
   (2) 프로젝트 이동 후 Flask 실행:
   cmd(폴더) > python app.py 명령
   
   (3) Running on http://... 확인:
   브라우저에 해당 주소로 접속해서 확인하기

   *flask가 없다면 패키지 설치 필요
   cmd > pip install flask python-dotenv requests

   **cmd 입력 시, 경로에 한글이 있다면 ""로 감싸기
