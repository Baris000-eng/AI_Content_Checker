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
        response = requests.get(url)
        response.raise_for_status()  # This will raise an HTTPError for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        # Target only the meaningful text content: p, h1, h2, h3, div, span, a
        content = soup.find_all(['p', 'h1', 'h2', 'h3', 'div', 'span', 'a'])
        
        # Clean the content: remove empty strings and strip unnecessary whitespace
        text = " ".join([element.get_text() for element in content if element.get_text().strip() != ''])

        print(text) 
        # Clean up unwanted content like scripts, styles, etc.
        for script in soup(['script', 'style', 'footer', 'header', 'nav']):
            script.decompose()

        # Optionally, remove links (if you don't want them in the final text)
        text = re.sub(r'http\S+', '', text)  # Remove URLs from the text (if any)

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
        
        ai_prob = probs[0][1].item()  # AI-generated probability
        human_prob = probs[0][0].item()  # Human-written probability
        
        return ai_prob, human_prob
    
    except Exception as e:
        return f"Error in AI detection: {e}"

def main():
    url = 'https://www.google.com/'  
    content = scrape_content(url)

    if content:
        # Clean up the text 
        content_cleaned = re.sub(r'\s+', ' ', content.strip())  
        ai_prob, human_prob = is_ai_generated(content_cleaned)
        if ai_prob > human_prob:
            print("This content is likely AI-generated.")
        elif human_prob > ai_prob:
            print("This content is likely human-written.")
        else: 
            print("This content is both equally likely AI-generated or human-written.")


if __name__ == "__main__":
    main()

