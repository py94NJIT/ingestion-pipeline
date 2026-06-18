import requests
import time

def fetch_data_from_api(search_query: str) -> list:
    url = f"https://openlibrary.org/search.json?q={search_query}&limit=10"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("docs", [])
    else:
        print("API Error: ", response.status_code)
        return []


if __name__=="__main__":
    print(fetch_data_from_api("python programming"))