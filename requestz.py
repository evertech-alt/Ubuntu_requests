import requests
import os
import hashlib
from urllib.parse import urlparse
from mimetypes import guess_extension

SAVE_DIR = "Fetched_Images"

def get_filename_from_url(url, content_type=None):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename or '.' not in filename:
        ext = guess_extension(content_type.split(';')[0]) if content_type else '.jpg'
        filename = f"image_{hashlib.md5(url.encode()).hexdigest()[:8]}{ext}"
    return filename

def is_duplicate(content_hash):
    for existing_file in os.listdir(SAVE_DIR):
        existing_path = os.path.join(SAVE_DIR, existing_file)
        if os.path.isfile(existing_path):
            with open(existing_path, 'rb') as ef:
                existing_hash = hashlib.md5(ef.read()).hexdigest()
                if existing_hash == content_hash:
                    return True
    return False

def download_image(url):
    try:
        headers = {'User-Agent': 'UbuntuFetcher/1.0'}
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith("image/"):
            print(f"Skipped (Not an image): {url}")
            return

        filename = get_filename_from_url(url, content_type)
        filepath = os.path.join(SAVE_DIR, filename)

        content_hash = hashlib.md5(response.content).hexdigest()
        if is_duplicate(content_hash):
            print(f"Skipped (Duplicate): {url}")
            return

        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"Saved: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Network error for {url}")
        print(f"  {e}")
    except Exception as e:
        print(f"Error downloading {url}")
        print(f"  {e}")

def main():
    print("Ubuntu Image Fetcher")
    print("A simple tool for respectful image collection.\n")

    os.makedirs(SAVE_DIR, exist_ok=True)

    print("Enter image URLs one at a time. Type 'done' when finished:\n")
    urls = []
    while True:
        url = input("> ").strip()
        if url.lower() == 'done':
            break
        if url:
            urls.append(url)

    if not urls:
        print("\nNo URLs entered. Exiting.")
        return

    print(f"\nStarting download of {len(urls)} image(s)...\n")

    for url in urls:
        download_image(url)

    print("\nDone. Images saved to the Fetched_Images folder.")

if _name_ == "_main_":
    main()