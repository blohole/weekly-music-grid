import os
import requests
from PIL import Image
from io import BytesIO
from atproto import Client

# --- REQUIRED CONFIG ---
LASTFM_USER = "thetenthlisten"
BSKY_HANDLE = "mintyice.online"
# -----------------------

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
BSKY_PASSWORD = os.getenv("BSKY_PASSWORD")

def get_chart_data():
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={LASTFM_USER}&api_key={LASTFM_API_KEY}&period=7day&limit=9&format=json"
    response = requests.get(url).json()
    
    if 'error' in response:
        raise Exception(f"Last.fm Error: {response.get('message')}")
    
    albums = response['topalbums']['album']
    
    # Extract names for the caption
    descriptions = [f"• {a['artist']['name']} - {a['name']}" for a in albums]
    # Extract image URLs for the grid
    image_urls = [a['image'][-1]['#text'] for a in albums]
    
    return descriptions, image_urls

def create_grid(image_urls):
    images = []
    for url in image_urls:
        resp = requests.get(url) if url else None
        img = Image.open(BytesIO(resp.content)).convert("RGB") if resp else Image.new('RGB', (300, 300), color='gray')
        images.append(img.resize((300, 300)))

    grid = Image.new('RGB', (900, 900))
    for i, img in enumerate(images):
        grid.paste(img, ((i % 3) * 300, (i // 3) * 300))
    
    img_byte_arr = BytesIO()
    grid.save(img_byte_arr, format='JPEG', quality=90)
    return img_byte_arr.getvalue()

def post_to_bluesky(image_data, descriptions):
    client = Client()
    client.login(BSKY_HANDLE, BSKY_PASSWORD)
    
    # Create a nice header and join the album list
    header = f"weekly last.fm top albums\n\n"
    full_text = header + "\n".join(descriptions)
    
    # Bluesky has a 300-character limit per post. 
    # If the list is too long, we'll truncate it so the post doesn't fail.
    if len(full_text) > 297:
        full_text = full_text[:297] + "..."

    client.send_image(
        text=full_text,
        image=image_data,
        image_alt="A 3x3 grid of my top albums this week."
    )
    print("Post with text successful!")

if __name__ == "__main__":
    try:
        desc, urls = get_chart_data()
        grid_img = create_grid(urls)
        post_to_bluesky(grid_img, desc)
    except Exception as e:
        print(f"❌ BOT FAILED: {e}")
        exit(1)