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

        # Comprehensive list of HTML tags that can contain meaningful text
        meaningful_tags = [
            # Headings
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    
            # Paragraphs and lists
            'p', 'li', 'ul', 'ol', 'dl', 'dt', 'dd',
    
            # Sections and structural
            'div', 'span', 'article', 'section', 'main', 'header', 'footer', 'nav', 'aside',
    
            # Emphasis and inline formatting
            'strong', 'em', 'b', 'i', 'mark', 'small', 'sub', 'sup', 'u', 'del', 'ins', 's', 'q', 'cite', 'code', 'pre', 'time',
    
            # Links
            'a', 'link', 
    
            # Tables
            'table', 'thead', 'tbody', 'tfoot', 'tr', 'td', 'th', 'caption',
    
            # Media captions
            'figure', 'figcaption',
    
            # Forms
            'form', 'label', 'button', 'option', 'select', 'textarea', 'input',
    
            # Quotes
            'blockquote', 'q', 'cite',
    
            # Details / summary
            'details', 'summary',
    
            # Address / contact
            'address',
    
            # Miscellaneous / semantic
            'abbr', 'data', 'time', 'var', 'samp', 'kbd', 'legend', 'fieldset',
    
            # Text containers
            'bdi', 'bdo', 'ruby', 'rt', 'rp', 'wbr'
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