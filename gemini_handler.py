# === gemini_handler.py ===

import google.generativeai as genai

def generate_with_gemini(prompt: str, api_key: str = None) -> str:
    """
    Gemini 1.5 Flash modeli ile içerik üretir.
    Sadece fonksiyona parametre olarak gelen api_key kullanılır;
    eğer api_key yoksa hata fırlatılır.
    """
    if not api_key:
        raise ValueError(
            "Gemini API anahtarı bulunamadı. "
            "Lütfen sidebar’dan kendi anahtarınızı girin."
        )

    # Sadece kullanıcıdan gelen anahtar ile yapılandır
    genai.configure(api_key=api_key)

    # Model örneğini oluştur ve içeriği üret
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    try:
        response = model.generate_content(prompt)
        return response.text or "🛑 Yanıt alınamadı."
    except Exception as e:
        return f"❌ Hata oluştu: {e}"
