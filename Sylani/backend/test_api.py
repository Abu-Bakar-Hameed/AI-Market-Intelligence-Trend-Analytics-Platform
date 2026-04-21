import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def test_endpoints():
    errors = []
    
    # Define endpoints to test
    endpoints = [
        ("GET", "/docs", None),
        ("GET", "/trends?days=7", None),
        ("GET", "/insights", None),
        ("GET", "/top-keywords", None),
        ("POST", "/sentiment", {"text": "This is a great day!"}),
        ("POST", "/extract-keywords", {"text": "Artificial intelligence is revolutionizing technology."}),
        ("GET", "/growth-trend", None),
        ("POST", "/process-article", {"title": "AI in healthcare", "content": "AI is changing healthcare forever."}),
        ("GET", "/search?q=test", None),
        ("GET", "/analytics/summary", None)
    ]
    
    for method, path, json_data in endpoints:
        url = BASE_URL + path
        try:
            if method == "GET":
                response = requests.get(url)
            else:
                response = requests.post(url, json=json_data)
                
            if response.status_code >= 400:
                errors.append(f"❌ {method} {path} failed with status {response.status_code}: {response.text}")
            else:
                print(f"✅ {method} {path} - OK")
        except Exception as e:
            errors.append(f"❌ {method} {path} failed to connect: {str(e)}")
            
    if errors:
        print("\nErrors found:")
        for err in errors:
            print(err)
    else:
        print("\nAll endpoints tested successfully!")

if __name__ == "__main__":
    test_endpoints()
