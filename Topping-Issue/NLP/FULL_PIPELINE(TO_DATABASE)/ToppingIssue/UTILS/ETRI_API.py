import urllib3
import json


def ETRI_API(key, api_type, text, openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"):
    requestJson = {"access_key": key,"argument": {"text": text,"analysis_code": api_type}}
    http = urllib3.PoolManager()
    response = http.request("POST",openApiURL,headers={"Content-Type": "application/json; charset=UTF-8"},body=json.dumps(requestJson))
    #print("[responseCode] " + str(response.status))
    return json.loads(str(response.data,"utf-8"))