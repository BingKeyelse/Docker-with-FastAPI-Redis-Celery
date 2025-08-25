from celery_config import celery
from transformers import pipeline
import torch

device = 0 if torch.cuda.is_available() else -1
pipe = pipeline("text-generation", model="openai-community/gpt2", device=device)

# pipe = pipeline("text-generation", model="openai-community/gpt2")

# @celery.task()
# def execute_llm(message):
#     return pipe(message)

@celery.task()
def execute_llm(text):
    return pipe(text, max_length=100)[0]["generated_text"]