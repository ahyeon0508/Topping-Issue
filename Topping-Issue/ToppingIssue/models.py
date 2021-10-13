import sqlite3
import pickle

conn = sqlite3.connect('ToppingIssue.db')
with open('0501-0503_final(10002).bin', 'rb') as f:
    news_df = pickle.load(f)

news_df['DATE'] = news_df['DATE'].dt.strftime("%Y-%m-%d")

news_df['Title'] = news_df['Title'].astype('str')
news_df['Title'] = news_df['Title'].str.replace("'", "\'")
news_df['Link'] = news_df['Link'].astype('str')

news_df.drop(['Content', 'Clean_text'], axis=1, inplace=True)
news_df.to_sql('news_data_101', conn)

conn.commit()
conn.close()