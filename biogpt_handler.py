from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Tokenizer ve modeli indiriyoruz
# Daha hızlı çalışması için base model seçtik
model_name = "microsoft/BioGPT"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Tahmin fonksiyonu
def generate_explanation(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_length=256,
        do_sample=True,
        top_p=0.9,
        top_k=50,
        temperature=0.8
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)