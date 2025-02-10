from moviepy.editor import *
from datetime import datetime
import requests
import xml.etree.ElementTree as ET

# Fetch the RSS feed
rss_url = "http://www.daystoendoftrumppresidency.com/feed.xml"
response = requests.get(rss_url)

# Check if the request was successful
if response.status_code != 200:
    raise Exception("Failed to fetch RSS feed")

rss_content = response.content

# Parse the RSS feed
root = ET.fromstring(rss_content)
item = root.find(".//item")

# Extract countdown and quote
countdown_text = item.find("title").text  # Example: "Countdown: 1442 Days"
quote_text = item.find("description").text  # Example: '"The best way to predict the future is to create it." - Peter Drucker'

# Split quote and author
if " - " in quote_text:
    quote, author = quote_text.split(" - ")
else:
    quote, author = quote_text, ""

# Video dimensions
W, H = 1080, 1920  # TikTok vertical video size

# Create a solid color background (same as website: #6793AC)
background = ColorClip(size=(W, H), color=(103, 147, 172)).set_duration(10)  # 10-second video

# Countdown Timer (Days)
countdown_txt = TextClip(countdown_text, fontsize=100, color="white", font="Lato-Bold")
countdown_txt = countdown_txt.set_position("center").set_duration(10)

# Quote Text
quote_txt = TextClip(quote.strip('"'), fontsize=70, color="yellow", font="Lato-Bold")
quote_txt = quote_txt.set_position(("center", H//2)).set_duration(10)

# Author Name (Smaller, Italic)
author_txt = TextClip("- " + author, fontsize=50, color="white", font="Lato-Italic")
author_txt = author_txt.set_position(("center", H//2 + 100)).set_duration(10)

# Combine all elements
final_video = CompositeVideoClip([background, countdown_txt, quote_txt, author_txt])

# Save the video
final_video.write_videofile("tiktok_countdown.mp4", fps=30, codec="libx264")

