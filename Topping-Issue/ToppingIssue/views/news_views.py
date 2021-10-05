from ToppingIssue import app
from flask import render_template

@app.route('/news')
def clusterData():
    newsData = {"메인 타이틀1": ["1", "2", "3", "4", "5"], "메인 타이틀2": ["10", "2", "3", "4", "5"],
    "메인 타이틀3": ["1", "2", "3", "4", "5"], "메인 타이틀4": ["1", "2", "3", "4", "5"]}
    sentimentData = {"N_Good" : [50, 40, 60, 20, 90], "N_Bad" : [40, 20, 30, 50, 5], "N_neut" : [10, 40, 10, 30, 5], "D_Good" : [50, 40, 60, 20, 90], "D_Bad" : [40, 20, 30, 50, 5], "D_neut" : [10, 40, 10, 30, 5]}
    return render_template("news.html", newsData=newsData, sentimentData=sentimentData)