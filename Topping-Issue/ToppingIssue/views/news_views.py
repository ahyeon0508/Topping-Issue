from ToppingIssue import app
from flask import render_template, request, make_response
import sqlite3 as sql
import pandas as pd
from ast import literal_eval
import json
from numpyencoder import NumpyEncoder

@app.route('/news', methods = ['GET'])
def news():
    selectCategory = request.args.get('subCategory')
    resp = make_response("category storage")

    if selectCategory is not None:
        resp.set_cookie('selectCategory', selectCategory)

    else:
        selectCategory = request.cookies.get('selectCategory')

    # 날짜, ap, dp
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    ap = request.args.get('ap')
    up = request.args.get('up')

    # default
    if startDate is None:
        startDate = '2021-05-01'
    
    if endDate is None:
        endDate = '2021-05-03'
    
    if ap is None:
        ap = 0.5 

    if up is None:
        up = 0.5

    # 날짜 설정(by 사용자)
    if startDate == endDate:
        date_list = "('" + startDate + "')"
    else:
        date_index = pd.date_range(start = startDate.replace('-', ''), end = endDate.replace('-', ''))
        date_list = str(tuple(date_index.strftime("%Y-%m-%d")))

    with sql.connect("ToppingIssue/ToppingIssue.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM news_data_" + str(selectCategory) + " WHERE DATE in " + date_list)
        rows = cur.fetchall()
        cols = [column[0] for column in cur.description]
        news_df = pd.DataFrame.from_records(data=rows, columns=cols)
    conn.close()

    news_df['Title'] = news_df['Title'].apply(lambda x: literal_eval(x))
    news_df['Link'] = news_df['Link'].apply(lambda x: literal_eval(x))

    newsData = dict()
    N_sentimentData = list()
    D_sentimentData = list()

    for i in range(0, len(user_dict)):
        newsData[news_df['key_word'][i]] = [news_df['Title'][i][0:3], news_df['Link'][i][0:3]]
        N_sentimentData.append([news_df['N_Good'][i], news_df['N_Bad'][i], news_df['N_Neut'][i]])
        D_sentimentData.append([news_df['D_Good'][i], news_df['D_Bad'][i], news_df['D_Neut'][i]])

    return render_template("news.html", newsData=newsData, subCategory='하이',
        N_sentimentData=json.dumps(N_sentimentData, cls=NumpyEncoder), D_sentimentData=json.dumps(D_sentimentData, cls=NumpyEncoder))

