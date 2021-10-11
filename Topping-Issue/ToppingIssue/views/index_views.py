from ToppingIssue import app
from flask import render_template
import json

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/categoryData')
def categoryData():
    data = json.dumps({'정치': ['청와대', '국회/정당', '북한', '행정', '국방/외교', '정치 일반'],
    '경제': ['금융', '증권', '산업/재계', '중기/벤처', '부동산', '글로벌 경제', '생활경제', '경제 일반'],
    '사회' : ['사건사고', '교육', '노동', '언론', '환경', '인권/복지', '식품/의료', '지역'],
    '세계' : ['아시아/호주', '미국/중남미', '유럽', '중동/아프리카', '세계 일반'],
    'IT/과학' : ['모바일', '인터넷/SNS', '통신/뉴미디어', 'IT 일반', '보안/해킹', '컴퓨터', '게임/리뷰', '과학 일반'] })
    return data