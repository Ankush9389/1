from app import app

if __name__ == '__main__':
import os

port = int(os.environ.get("PORT", 5000))  # default to 5000 locally
app.run(host="0.0.0.0", port=port)  # ✅ Correct

