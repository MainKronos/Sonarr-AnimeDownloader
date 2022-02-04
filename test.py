import requests
import json

res = requests.get("http://192.168.1.11:8989/api/wanted/missing?apikey=f10994e9f3494368a31a3088aba6b9fc&sortKey=airDateUtc&page=0")


print(res.json()["records"][0]["series"]["tvdbId"])

# print(json.dumps(res.json(), indent=2))