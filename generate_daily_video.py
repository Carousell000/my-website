import os
import json
import base64

# 🔐 Get the encoded Google credentials from GitHub Secrets
encoded_credentials = os.environ.get("GOOGLE_DRIVE_CREDENTIALS")

if not encoded_credentials:
    raise ValueError("🚨 GOOGLE_DRIVE_CREDENTIALS secret is missing! Ensure it's saved correctly in GitHub.")

try:
    # 🔓 Decode the Base64 string
    decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")

    # 🧾 Convert the string back into a JSON object
    credentials_dict = json.loads(decoded_credentials)

    # 💾 Save it as credentials.json
    with open("credentials.json", "w") as f:
        json.dump(credentials_dict, f)

    print("✅ Google credentials saved to credentials.json")
except Exception as e:
    raise ValueError(f"🚨 Failed to decode GOOGLE_DRIVE_CREDENTIALS: {e}")

# ✅ Step 5: Import required libraries for video generation
from moviepy.editor import *
from datetime import datetime

# ✅ Step 6: Generate Countdown Timer Text
target_date = datetime(2029, 1, 21, 10, 0)  # January 21, 2029, 10 AM Washington time
today = datetime.utcnow()
days_remaining = (target_date - today).days
countdown_text = f"{days_remaining} Days Left"

# ✅ Step 7: Load Quote of the Day
import pandas as pd
quotes = pd.read_csv("quotes.csv")
quote_index = days_remaining % len(quotes)
quote, author = quotes.iloc[quote_index]["quote"], quotes.iloc[quote_index]["author"]
quote_text = f'"{quote}"\n\n— {author}'

# ✅ Step 8: Create Video Clip
video = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=10)
countdown_txt = TextClip(countdown_text, fontsize=100, color="white", font="Arial-Bold").set_position("center").set_duration(10)
quote_txt = TextClip(quote_text, fontsize=50, color="yellow", font="Arial-Italic").set_position(("center", 800)).set_duration(10)

# ✅ Step 9: Overlay Text on Video
final_video = CompositeVideoClip([video, countdown_txt, quote_txt])

# ✅ Step 10: Save Video
video_path = "countdown_video.mp4"
final_video.write_videofile(video_path, fps=24, codec="libx264")

print("✅ Video successfully generated:", video_path)
