import requests, json

r = requests.get("https://api.github.com/repos/Aeonss/WebtoonReader/releases/latest")

print(json.loads(r.content).get("tag_name"))