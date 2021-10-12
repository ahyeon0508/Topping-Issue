import sqlite3

conn = sqlite3.connect('ToppingIssue.db')
cur = conn.cursor()
cur.execute('CREATE TABLE news_data(Category TEXT, Clust_NO INTEGER, Title TEXT, Link TEXT, Article_cnt INTEGER, Comment_cnt INTEGER, N_Good INTEGER, N_Bad INTEGER, N_Neut INTEGER, D_Good INTEGER, D_Bad INTEGER, D_Neut INTEGER, Rank_score DOUBLE)')
cur.execute('INSERT INTO news_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', ('모바일', 1, "['폰카메라 더 작아진다…국내 연구진, 1만배 얇은 초박막렌즈 개발', '카툭튀 해결되나…기존 굴절렌즈보다 1만배 얇은 초박막렌즈 개발됐다']",
    "['https://www.dailian.co.kr/news/view/951598/?sc=Naver', 'https://www.news1.kr/articles/?4166391']", 5, 8, 20, 10, 5, 4, 6, 7, 2.5))
conn.commit()
conn.close()