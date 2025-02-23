from moviepy.editor import TextClip, CompositeVideoClip
from datetime import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Authenticate Google Drive
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Authenticates locally via a browser
drive = GoogleDrive(gauth)

# Countdown Logic
target_date = datetime(2029, 1, 21, 10, 0)  # January 21, 2029, 10 AM Washington time
now = datetime.utcnow()
days_remaining = (target_date - now).days

# Load a quote from a text file (one quote per line)
with open("quotes.txt", "r", encoding="utf-8") as file:
    quotes = file.readlines()
quote = quotes[days_remaining % len(quotes)].strip()

# Create Video Clips
countdown_text = f"{days_remaining} Days Left"
quote_text = f'"{quote}"'

# Countdown Clip
countdown_clip = TextClip(countdown_text, fontsize=100, color="white", size=(1080, 1920)).set_duration(10)
quote_clip = TextClip(quote_text, fontsize=50, color="blue", size=(1080, 1920)).set_duration(10).set_position(('center', 'bottom'))

# Combine Clips
final_clip = CompositeVideoClip([countdown_clip, quote_clip])

# Save the video locally
video_filename = "daily_countdown_video.mp4"
final_clip.write_videofile(video_filename, fps=24)

# Upload video to Google Drive
folder_id = "1mfWyf9k2hljjxx2wGpqKgNMM-flwHta6"  # Your Google Drive folder ID
file_drive = drive.CreateFile({'title': video_filename, 'parents': [{'id': folder_id}]})
file_drive.SetContentFile(video_filename)
file_drive.Upload()

print("Video uploaded successfully to Google Drive.")
