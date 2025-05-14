import requests

def make_request(url):
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        return f"Error while making the request: {str(e)}"
