from fastapi import FastAPI
from pydantic import BaseModel
from transformers import BartForConditionalGeneration, BartTokenizer
from keybert import KeyBERT

# Load pre-trained BART model and tokenizer
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

# Load spaCy for keyword extraction
kw_model = KeyBERT()

app = FastAPI()

class TextInput(BaseModel):
    text: str

def summarize_text(text: str, max_length: int = 130) -> str:
    inputs = tokenizer([text], max_length=1024, return_tensors="pt", truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length=max_length, num_beams=4, length_penalty=2.0, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def extract_keywords(text: str, top_n: int = 15) -> list:
    # Use KeyBERT to extract keywords
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words="english", top_n=top_n)
    return [keyword[0] for keyword in keywords]  # Extract only the keyword, not the score

@app.post("/summarize/")
async def summarize(input: TextInput):
    summary = summarize_text(input.text)
    keywords = extract_keywords(input.text)
    return {"summary": summary, "keywords": keywords}