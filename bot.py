import os
import requests
from PIL import Image
from io import BytesIO
from atproto import Client, models

# --- Configuration ---
LASTFM_USER = "thetenthlisten"
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
BSKY_HANDLE = "mintyice.online"
BSKY_PASSWORD = os.getenv("BSKY_PASSWORD")

def get_top_albums():
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={LASTFM_USER}&api_key={LASTFM_API_KEY}&period=7day&limit=9&format=json"
    data = requests.get(url).json()
    return [album['image'][-1]['#text'] for album in data['topalbums']['album']]

def create_grid(image_urls):
    images = [Image.open(BytesIO(requests.get(url).content)).convert("RGB") for url in image_urls]
    grid = Image.new('RGB', (900, 900))
    for i, img in enumerate(images):
        img = img.resize((300, 300))
        grid.paste(img, ((i % 3) * 300, (i // 3) * 300))
    
    img_byte_arr = BytesIO()
    grid.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()

def post_to_bluesky(image_data):
    client = Client()
    client.login(BSKY_HANDLE, BSKY_PASSWORD)
    
    # Upload the image first
    upload = client.upload_blob(image_data)
    
    # Create the post with the image attachment
    client.send_image(
        text="My weekly 3x3 music chart! 🎵",
        image=upload.blob,
        image_alt="A 3x3 grid of my most listened to albums this week."
    )

if __name__ == "__main__":
    album_urls = get_top_albums()
    grid_img = create_grid(album_urls)
    post_to_bluesky(grid_img)