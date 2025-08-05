from flask import Flask, jsonify
import threading
import time
import requests
import webbrowser
import random
import sys

app = Flask(__name__)

status_data = {
    "massar_up": False,
    "last_checked": None,
    "message": "Massar site is currently down."
}

MASSAR_URL = "https://cnc2025.ensem.ac.ma/"

def check_massar_status():
    while True:
        try:
            response = requests.get(MASSAR_URL, timeout=10)
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

            if response.status_code == 200:
                print(f"[{timestamp}] ✅ Massar is back online!")
                status_data["massar_up"] = True
                status_data["message"] = "✅ Massar is back online!"
                status_data["last_checked"] = timestamp

                webbrowser.open(MASSAR_URL)
                print("✅ Browser opened. Exiting program now.")
                sys.exit(0)

            else:
                print(f"[{timestamp}] ❌ Massar still down (code {response.status_code})")
                status_data["massar_up"] = False

        except requests.RequestException as e:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] ❌ Error: {e}")
            status_data["massar_up"] = False

        status_data["last_checked"] = time.strftime('%Y-%m-%d %H:%M:%S')
        time.sleep(random.uniform(1, 3))

@app.route('/status')
def get_status():
    return jsonify(status_data)

def run_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    print("🟢 Starting Massar checker...")

    # Start Flask in a thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Run the checker in the main thread (so sys.exit() works)
    check_massar_status()
