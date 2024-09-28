import os
import dotenv
import requests
from requests.exceptions import RequestException, Timeout

dotenv.load_dotenv()

def fetch_social_media_data(name):
    url = "https://social-links-search.p.rapidapi.com/search-social-links"

    querystring = {"query":name}

    headers = {
        "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
        "x-rapidapi-host": "social-links-search.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            print(f"Response from API: {response.json()}")
            return response.json()
        else:
            print(f"Error occurred while fetching data: {response.json()}")
            return 
    except RequestException as e:
        print(f"Error occurred while fetching data: {str(e)}")
        return