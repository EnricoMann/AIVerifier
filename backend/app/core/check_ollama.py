import requests
import time

OLLAMA_URL = "http://host.docker.internal:11434"
MODEL_NAME = "llama3"

def ensure_ollama_ready():
    print("🔍 Checking Ollama service...")
    for _ in range(10):
        try:
            r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
            if r.status_code == 200:
                print("✅ Ollama is running.")
                return True
        except Exception:
            print("⏳ Waiting for Ollama to start...")
            time.sleep(2)
    print("❌ Ollama is not responding at host.docker.internal:11434")
    return False

def ensure_model_downloaded():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags")
        models = r.json().get("models", [])
        if not any(MODEL_NAME in m.get("name", "") for m in models):
            print(f"⚠️ Model '{MODEL_NAME}' not found on Ollama.")
            print(f"   → Please run manually on your host:")
            print(f"     ollama pull {MODEL_NAME}\n")
        else:
            print(f"✅ Model '{MODEL_NAME}' already available.")
    except Exception as e:
        print(f"⚠️ Could not check models: {e}")

if __name__ == "__main__":
    if ensure_ollama_ready():
        ensure_model_downloaded()
