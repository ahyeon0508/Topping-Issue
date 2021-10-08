from ToppingIssue import app
from flask import render_template
import pickle

@app.route('/news')
def clusterData():
    with open('데이터명', 'rb') as f:
        df = pickle.load(f)
        df = df[df['Date'] == '2021-04-24']

    newsData = {}
    for i in range(1, len(df)):
        newsData[df['Title'][i][0]] = [df['Title'][i][1:4], df['Link'][i][0:4]]

    sentimentData = {"N_Good" : [50, 40, 60, 20, 90], "N_Bad" : [40, 20, 30, 50, 5], "N_neut" : [10, 40, 10, 30, 5], "D_Good" : [50, 40, 60, 20, 90], "D_Bad" : [40, 20, 30, 50, 5], "D_neut" : [10, 40, 10, 30, 5]}
    return render_template("news.html", newsData=newsData, sentimentData=sentimentData)