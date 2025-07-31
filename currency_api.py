# ============================
# Smart Calculator - sur4jkum4r
# CURRENCY API
# ============================

import requests

# ✅ APNI API KEY YAHI RAKH
API_KEY = "2b3b6533ab46679eaddbc242"  # Change kar lena agar nayi mile

def get_exchange_rate(from_currency, to_currency):
    try:
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}"
        response = requests.get(url)
        data = response.json()

        if data['result'] == 'success':
            return data['conversion_rate']
        else:
            print("⚠️ API Error:", data['error-type'])
            return None
    except Exception as e:
        print("⚠️ Connection Error:", e)
        return None