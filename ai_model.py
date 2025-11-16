from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
import config

# Load tokenizer and model globally
tokenizer = AutoTokenizer.from_pretrained(config.MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(config.MODEL_NAME)

def predict_chunks(chunks):
    """ Predict AI-generated probabilities for a list of text chunks """
    results = []
    
    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            probs = F.softmax(outputs.logits, dim=-1)
        
        ai_prob = probs[0][0].item()  # AI-generated probability, fake 
        human_prob = probs[0][1].item()  # Human-written probability, real
        results.append((ai_prob, human_prob))
    
    return results
