from .models import Emoji, Sticker
import json
from django.conf import settings

def emojis(request):
    emojis_data = []
    stickers_data = []
    file_path = settings.BASE_DIR / 'media_data.json'

    if file_path.exists():
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                emojis_data = data.get('emojis', [])
                stickers_data = data.get('stickers', [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading or parsing media_data.json: {e}")

    # Convert plain dictionaries back to objects with .image attribute for consistency
    # This is a simplification; in a real app, you might want to create dummy model instances
    # or a custom object to hold this data if the templates expect it.
    class MediaItem:
        def __init__(self, name, image_url):
            self.name = name
            self.image = image_url # Store URL directly
            self.pk = name # Use name as primary key for templating if needed

    emojis_objects = [MediaItem(item['name'], item['image_url']) for item in emojis_data]
    stickers_objects = [MediaItem(item['name'], item['image_url']) for item in stickers_data]

    return {
        'emojis': emojis_objects,
        'stickers': stickers_objects,
    }
