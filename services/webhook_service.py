import requests

WEBHOOK_URL = "http://127.0.0.1:8000/webhook"

def send_signal(signal):
    try:
        response = requests.post(
            WEBHOOK_URL,
            json=signal,
            timeout=5
        )

        print(response.status_code)

        return response.status_code == 200

    except Exception as e:
        print(e)
        return False