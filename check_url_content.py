import requests
import re
from bs4 import BeautifulSoup



def scrape_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove unwanted tags BEFORE extraction
        for tag in soup(['script', 'style', 'footer', 'header', 'nav', 'aside']):
            tag.decompose()

        # Tags that usually contain meaningful text
        meaningful_tags = [
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'p', 'li',
            'div', 'span', 'a',
            'strong', 'em', 'b', 'i',
            'article', 'section', 'main'
        ]

        # Extract text
        elements = soup.find_all(meaningful_tags)

        text = " ".join(
            element.get_text(strip=True)
            for element in elements
            if element.get_text(strip=True)
        )

        # Remove realistic URLs 
        text = re.sub(r'https?://[^\s]+\.[^\s]+', '', text)

        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None