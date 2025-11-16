from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import requests
from bs4 import BeautifulSoup
import config
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
import config

# Load tokenizer and model globally for AI detection (using RoBERTa for OpenAI detection)
tokenizer = AutoTokenizer.from_pretrained(config.MODEL_NAME)  
model = AutoModelForSequenceClassification.from_pretrained(config.MODEL_NAME)  

print("\n")
print("\n")
print("\n")
print("\n")

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

        # Remove URLs inside the scraped text
        text = re.sub(r'http\S+', '', text)

        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

# Function to detect if the text is AI-generated using RoBERTa-based model
def is_ai_generated(text):
    try:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            probs = F.softmax(outputs.logits, dim=-1)
        
        print(probs)
        
        ai_prob = probs[0][0].item()  # AI-generated probability
        human_prob = probs[0][1].item()  # Human-written probability
        
        return ai_prob, human_prob
    
    except Exception as e:
        return f"Error in AI detection: {e}"

def main():
    url = 'https://www.google.com/'  
    content = scrape_content(url)

    if content:
        # Clean up the text 
        content_cleaned = re.sub(r'\s+', ' ', content.strip())  
        print(content_cleaned)
        ai_prob, human_prob = is_ai_generated(content_cleaned)
        if ai_prob > human_prob:
            print("This content is likely AI-generated.")
        elif human_prob > ai_prob:
            print("This content is likely human-written.")
        else: 
            print("This content is both equally likely AI-generated or human-written.")


if __name__ == "__main__":
    main()

