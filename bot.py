import os
import requests
from PIL import Image
from io import BytesIO
from atproto import Client, models

# --- ⚠️ REQUIRED: CHANGE THESE TWO LINES ⚠️ ---
LASTFM_USER = "thetenthlisten"  # e.g., "musicfan99"
BSKY_HANDLE = "mintyice.online"      # e.g., "johndoe.bsky.social"
# ----------------------------------------------

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
BSKY_PASSWORD = os.getenv("BSKY_PASSWORD")

def get_top_albums():
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={LASTFM_USER}&api_key={LASTFM_API_KEY}&period=7day&limit=9&format=json"
    response = requests.get(url).json()
    
    if 'error' in response:
        raise Exception(f"Last.fm Error: {response.get('message')} (Error Code: {response.get('error')})")
    
    if 'topalbums' not in response or not response['topalbums']['album']:
        raise Exception("No albums found for this user in the last 7 days.")
        
    return [album['image'][-1]['#text'] for album in response['topalbums']['album']]

def create_grid(image_urls):
    images = []
    for url in image_urls:
        if not url: # Use a placeholder if an album has no cover art
            images.append(Image.new('RGB', (300, 300), color='gray'))
            continue
        resp = requests.get(url)
        images.append(Image.open(BytesIO(resp.content)).convert("RGB"))

    grid = Image.new('RGB', (900, 900))
    for i, img in enumerate(images):
        img = img.resize((300, 300))
        grid.paste(img, ((i % 3) * 300, (i // 3) * 300))
    
    img_byte_arr = BytesIO()
    grid.save(img_byte_arr, format='JPEG', quality=90)
    return img_byte_arr.getvalue()

def post_to_bluesky(image_data):
    client = Client()
    client.login(BSKY_HANDLE, BSKY_PASSWORD)
    
    # We use the direct 'send_image' helper with the raw bytes
    # This is more stable across different library versions
    client.send_image(
        text=f"test post please ignore! 🎵",
        image=image_data,
        image_alt="A 3x3 grid of my most listened to albums this week."
    )
    print("Post successful!")

if __name__ == "__main__":
    try:
        album_urls = get_top_albums()
        grid_img = create_grid(album_urls)
        post_to_bluesky(grid_img)
    except Exception as e:
        print(f"❌ BOT FAILED: {e}")
        exit(1)