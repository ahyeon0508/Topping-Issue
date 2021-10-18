import sqlite3
import pickle

conn = sqlite3.connect('ToppingIssue.db')

def build_db(file_name):
    with open(file_name, 'rb') as f:
        news_df = pickle.load(f)

    news_df['DATE'] = news_df['DATE'].dt.strftime("%Y-%m-%d")

    news_df['Title'] = news_df['Title'].astype('str')
    news_df['Title'] = news_df['Title'].str.replace("'", "\'")
    news_df['Link'] = news_df['Link'].astype('str')

    news_df.drop(['Content', 'Clean_text'], axis=1, inplace=True)

    return news_df

news_df = build_db('2021_102.bin')
news_df.to_sql('news_data_102', conn)

news_df = build_db('2021_201.bin')
news_df.to_sql('news_data_201', conn)

conn.commit()
conn.close()