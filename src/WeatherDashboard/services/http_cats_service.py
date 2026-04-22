import time

BASE_URL = "https://cataas.com/cat"

def get_cat_url(status_code: int = None) -> str:
    return f"{BASE_URL}?random={int(time.time() * 1000)}"