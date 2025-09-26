# lyrics_model.py
import os
MOCK_MODE = os.getenv("MOCK_MODE", "1") == "1"

def generate_lyrics(poem_text: str, mood: str = "", style_examples=None) -> str:
    if MOCK_MODE:
        # Simple transformation for mock testing
        header = f"(mock lyrics — mood: {mood})\n\n"
        return header + poem_text + "\n\n(chorus: la la la)"
    # Real model: example stub where you call OpenAI
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = f"Rewrite the following poem into song lyrics with mood='{mood}':\n\n{poem_text}\n\nProvide verses + chorus."
    resp = openai.ChatCompletion.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}], max_tokens=600)
    return resp["choices"][0]["message"]["content"]