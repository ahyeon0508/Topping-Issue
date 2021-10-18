from ToppingIssue import app
from flask import render_template, request, session
import sqlite3 as sql
import pandas as pd
from ast import literal_eval
import json
from numpyencoder import NumpyEncoder

app.secret_key = 'category'

def min_max(data):
    if len(data) == 1:
        return data
    else:
        x_min, x_max = min(data), max(data)
        return (data-x_min)/(x_max-x_min)

@app.route('/news', methods = ['GET'])
def news():
    selectCategory = request.args.get('subCategory')

    if selectCategory is None:
        selectCategory = session['selectCategory']
    
    else:
        session['selectCategory'] = selectCategory

    # 날짜, ap, dp
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    ap = request.args.get('ap')
    up = request.args.get('up')

    # default
    if startDate is None:
        startDate = '2021-08-01'
    
    if endDate is None:
        endDate = '2021-08-07'
    
    if ap is None:
        ap = 0.5

    if up is None:
        up = 0.5

    ap = float(ap) / (float(ap) + float(up))
    up = float(up) / (float(ap) + float(up))

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

    # keyword, sub_keyword
    news_df.loc[news_df['key_word'] == '0', 'key_word'] = 'NA'
    news_df.loc[news_df['sub_words'] == '0', 'sub_words'] = 'NA'

    key_word_list = list(news_df['key_word'].unique())
    key_word_list.remove('NA')

    user_dict = dict()
    score_dict = dict()
    for key_word in key_word_list:
        news_df['Rank_score'] = ap*(min_max(news_df['Article_cnt'])) + up*(min_max(news_df['Comment_cnt']) + min_max(news_df['Sentiment_cnt']))/2
        temp_df = news_df.loc[news_df['key_word'] == key_word,:].copy()
        temp_df['Sub_rank'] = list(ap*((min_max(temp_df['Article_cnt']))) + up*(min_max(temp_df['Comment_cnt']) + min_max(temp_df['Sentiment_cnt']))/2)
        temp_df.sort_values(by = ['Sub_rank'], ascending = False, inplace = True)
        user_dict[key_word] = temp_df.copy()
        score_dict[key_word] = user_dict[key_word].Rank_score.sum()

    score_dict = sorted(score_dict.items(), key=lambda x : x[1], reverse = True)

    # 전송 데이터
    newsName_list, news_dict, subNews_list = list(), dict(), list()
    N_sentiment_list, D_sentiment_list = list(), list()
    N_sub_sentiment_list, D_sub_sentiment_list = list(), list()

    term_chart_df = pd.DataFrame(columns = ['DATE', 'key_word', 'sub_words', 'Rank_score', 'Sub_rank'])

    for i in range(10):
        temp_news_title, temp_news_link, temp_N_sentiment, temp_D_sentiment = list(), list(), list(), list()
        temp_subnews_title, temp_subnews_link, temp_N_sub_sentiment, temp_D_sub_sentiment, temp_subwords = list(), list(), list(), list(), list()

        user_dict[score_dict[i][0]].reset_index(drop=True, inplace=True)

        # term-chart-df
        if i < 5:
            term_chart_df = term_chart_df.append(user_dict[score_dict[i][0]][['DATE', 'key_word', 'sub_words', 'Rank_score', 'Sub_rank']], ignore_index=True)

        for j in range(len(user_dict[score_dict[i][0]])):
            if user_dict[score_dict[i][0]].loc[j]['sub_words'] == 'NA':
                temp_news_title.append(user_dict[score_dict[i][0]].loc[j]['Title'][:3])
                temp_news_link.append(user_dict[score_dict[i][0]].loc[j]['Link'][:3])
                temp_N_sentiment.append([user_dict[score_dict[i][0]].loc[j]['N_Good'], user_dict[score_dict[i][0]].loc[j]['N_Bad'], user_dict[score_dict[i][0]].loc[j]['N_Neut']])
                temp_D_sentiment.append([user_dict[score_dict[i][0]].loc[j]['D_Good'], user_dict[score_dict[i][0]].loc[j]['D_Bad'], user_dict[score_dict[i][0]].loc[j]['D_Neut']])
            else:
                temp_subnews_title.append(user_dict[score_dict[i][0]].loc[j]['Title'][:4])
                temp_subnews_link.append(user_dict[score_dict[i][0]].loc[j]['Link'][:4])
                temp_N_sub_sentiment.append([user_dict[score_dict[i][0]].loc[j]['N_Good'], user_dict[score_dict[i][0]].loc[j]['N_Bad'], user_dict[score_dict[i][0]].loc[j]['N_Neut']])
                temp_D_sub_sentiment.append([user_dict[score_dict[i][0]].loc[j]['D_Good'], user_dict[score_dict[i][0]].loc[j]['D_Bad'], user_dict[score_dict[i][0]].loc[j]['D_Neut']])
                temp_subwords.append('# ' + user_dict[score_dict[i][0]].loc[j]['sub_words'])

        # 모두 sub_word가 있는 경우
        if len(temp_news_title) == 0:
            newsName_list.append(score_dict[i][0])
            news_dict[score_dict[i][0]] = [temp_subnews_title[0][:2], temp_subnews_link[0][:2]]
            subNews_list.append([temp_subwords[1:3], temp_subnews_title[1:3], temp_subnews_link[1:3]])
            N_sentiment_list.append(temp_N_sub_sentiment[0])
            D_sentiment_list.append(temp_D_sub_sentiment[0])
            N_sub_sentiment_list.append(temp_N_sub_sentiment[1:3])
            D_sub_sentiment_list.append(temp_D_sub_sentiment[1:3])

        else:
            newsName_list.append(score_dict[i][0])
            news_dict[score_dict[i][0]] = [temp_news_title[0], temp_news_link[0]]
            subNews_list.append([temp_subwords[:2], temp_subnews_title[:2], temp_subnews_link[:2]])
            N_sentiment_list.append(temp_N_sentiment[0])
            D_sentiment_list.append(temp_D_sentiment[0])
            N_sub_sentiment_list.append(temp_N_sub_sentiment[:2])
            D_sub_sentiment_list.append(temp_D_sub_sentiment[:2])

    # 기간에 따른 핵심 키워드 추출 기능
    termChartDate = pd.date_range(start = startDate, end = endDate).strftime("%Y-%m-%d").tolist()

    term_keyword_list = term_chart_df['key_word'].unique()
    termChartData = dict()
    termChartsubData = list()

    for keyword in term_keyword_list:
        termChartData[keyword] = []

    for date in termChartDate:
        temp_chart_df = term_chart_df[term_chart_df['DATE'] == date]
        temp_chart_df = temp_chart_df[temp_chart_df['sub_words'] != "NA"]
        temp_sub_word = list()
        for keyword in term_keyword_list:
            temp_score_list = termChartData.get(keyword)

            if len(temp_chart_df[temp_chart_df['key_word'] == keyword]['Sub_rank'].to_list()) == 0:
                temp_score_list.append('')
            else:
                temp_score_list.append(temp_chart_df[temp_chart_df['key_word'] == keyword]['Sub_rank'].to_list()[0])
            temp_sub_word.append(temp_chart_df[temp_chart_df['key_word'] == keyword]['sub_words'].to_list()[:2])
        termChartsubData.append(temp_sub_word)

    return render_template("news.html", newsName=newsName_list, newsData=json.dumps(news_dict, ensure_ascii=False), subNewsData=subNews_list, termChartData=json.dumps(termChartData, ensure_ascii=False), termChartDate=json.dumps(termChartDate), termChartsubData=json.dumps(termChartsubData),
        N_sentimentData=json.dumps(N_sentiment_list, cls=NumpyEncoder), D_sentimentData=json.dumps(D_sentiment_list, cls=NumpyEncoder),
        N_sub_sentimentData=json.dumps(N_sub_sentiment_list, cls=NumpyEncoder), D_sub_sentimentData=json.dumps(D_sub_sentiment_list, cls=NumpyEncoder), enumerate=enumerate)