from bs4 import BeautifulSoup
import requests

def scrape_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return links[:5]  # Return the first 5 links found
    except Exception as e:
        return f"Error while scraping links: {str(e)}"

def web_scrape(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        return text[:500]  # Return the first 500 characters of the scraped text
    except Exception as e:
        return f"Error while scraping: {str(e)}"
