from flask import Flask, request, jsonify, render_template
import json
import os
import base64
from requests import post, get
from dotenv import load_dotenv

load_dotenv() #환경변수 로드(api의 CLIENT_ID, CLIENT_SECRET 키 사용)

app = Flask(__name__) #플라스크 생성

#환경변수에서 아이디랑 시크릿 가져오기
client_id = os.getenv("CLIENT_ID") 
client_secret = os.getenv("CLIENT_SECRET")

def get_token(): #api에 접근하기 위한 액세스 토큰 요청
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = { 
        #id와 secret을 base64 인코딩, autho-헤더에 포함
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    } 
    data = {"grant_type": "client_credentials"} #grant_type 설정, 크라이언트 크리덴셜 인증방식으로
    result = post(url, headers=headers, data=data)
    json_result = result.json()
    return json_result.get("access_token") #

def search_artist(token, artist_name): #아티스트 정보 검색
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    query = f"?q={artist_name}&type=artist&limit=1" #검색 요청 시 q와 type을 artist로 설정

    result = get(url + query, headers=headers)
    json_result = result.json().get("artists", {}).get("items", []) #api응답에서 artists -> items 리스트 추출(최대1)

    if not json_result:
        return None
    return json_result[0] #리스트 첫 번째 아티 반환

def get_top_tracks(token, artist_id): #아티스트의 인기 곡 가져옴
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US" #나라 변경 시 해당 나라기준으로 설정됨
    headers = {"Authorization": f"Bearer {token}"}
    result = get(url, headers=headers)
    return result.json().get("tracks", [])

@app.route("/")
def index(): #기본 웹페이지 렌더링
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def search(): #api 엔드포인트: 클라이언트에서 아티 이름을 GET으로 받아 검색
    artist_name = request.args.get("artist")
    if not artist_name: #arist 파라미터 없으면 400 에러 반환
        return jsonify({"error": "No artist provided"}), 400

    token = get_token()
    artist = search_artist(token, artist_name)
    if not artist: #아티 검색 안 되면 404에러 반환
        return jsonify({"error": "Artist not found"}), 404

    artist_id = artist["id"]
    tracks = get_top_tracks(token, artist_id)

    return jsonify({ #검색된 아티 이름, 이미지, 인기 트랙 반환(JSON 형태)
        "artist_name": artist["name"],
        "artist_image": artist["images"][0]["url"] if artist["images"] else "",
        "tracks": [{"name": track["name"], "preview_url": track["preview_url"]} for track in tracks]
    })

if __name__ == "__main__": #디버그 모드로 flask 실행
    app.run(debug=True)
