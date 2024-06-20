import requests

api_key = "브롤 api"
url = "https://api.brawlstars.com/v1/brawlers"
headers = {
    "Authorization": f"Bearer {api_key}"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("API 키가 유효합니다.")
    print(response.json())  # 성공적인 응답을 확인
else:
    print(f"API 키가 유효하지 않습니다. 상태 코드: {response.status_code}")
