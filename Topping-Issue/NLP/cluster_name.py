# 37번째 줄 ETRI API Key 입력

import re
import urllib3
import json
import pandas as pd

# ETRI API 호출
def ETRI_API(key, api_type, text, openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"):
    requestJson = {"access_key": key,"argument": {"text": text,"analysis_code": api_type}}
    http = urllib3.PoolManager()
    response = http.request("POST",openApiURL,headers={"Content-Type": "application/json; charset=UTF-8"},body=json.dumps(requestJson))
    print("[responseCode] " + str(response.status))
    return json.loads(str(response.data,"utf-8"))

# MORP 데이터 프레임 생성
def MORP_TO_DF(morp_df, test):
    for j in range(len(test['return_object']['sentence'])):
            for i in range(len(test['return_object']['sentence'][j]['morp'])):
                morp_df = morp_df.append(test['return_object']['sentence'][j]['morp'][i], ignore_index=True)
    return morp_df

# WORD 리스트 생성
def WORD_TO_LIST(word_list, test):
    for j in range(len(test['return_object']['sentence'])):
            for i in range(len(test['return_object']['sentence'][j]['word'])):
                word_list.append(test['return_object']['sentence'][j]['word'][i]['text'])
    return word_list

#텍스트에 포함되어 있는 특수 문자 제거
def clean_text(readData):
  text = re.sub('[-=+,#/\?:^@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', ' ', readData)
  text_rr = ' '.join(text.split())
  return text_rr

api_type = 'morp'
key = ''

title_list = ['애플 5G폰, 출시 두달새 삼성 年판매량 추월', "애플 '아이폰12' 두 달 성적, 1년 판매한 삼성 앞질렀다", '단 두달만에…애플, 삼성 5G폰 연간판매량 따라잡았다']
morp_df = pd.DataFrame(columns = ['id','lemma','type','position','weight'])
word_list = []
have_not_word_list = []
cluster_name_list = []

for title in title_list:
    test_text1 = clean_text(title)
    test_response1 = ETRI_API(key, api_type, test_text1)
    morp_df = MORP_TO_DF(morp_df, test_response1)
    word_list = WORD_TO_LIST(word_list, test_response1)

morp_df = morp_df[morp_df['type'].isin(['NNG','NNP'])] # 일반명사, 고유명사
morp_df = morp_df['lemma'].value_counts().reset_index()
morp_df.columns = ['lemma', 'size']
many_morp_list = morp_df[morp_df['size'] > (len(title_list)*0.5)]['lemma'].tolist()

for morp in many_morp_list:
    if morp not in word_list:
        have_not_word_list.append(morp)
    else:
        cluster_name_list.append(morp)

for i in range(len(have_not_word_list)-1):
    temp = have_not_word_list[i]
    cnt = 0
    while True:
        if (temp + have_not_word_list[i+1]) in ''.join(word_list):
            temp += have_not_word_list[i+1]
            i += 1
            cnt += 1
        elif cnt > 0:
            cluster_name_list.append(temp)
            break
        else:
            break
        if i == (len(have_not_word_list)-1):
            cluster_name_list.append(temp)
            break

print(cluster_name_list) # ['애플', '삼성', '판매량']