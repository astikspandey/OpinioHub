from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Emoji, Sticker, Font, Category, Tag, Comment
from django.contrib.auth.decorators import login_required
from .forms import PostForm, EmojiForm, StickerForm, FontForm
from django.contrib.auth.forms import UserCreationForm
import requests
import json
import datetime
import os # Import os module
from django.http import HttpResponse
from django.conf import settings # Import settings

IMGBB_API_KEY = os.environ.get('IMGBB_API_KEY', 'bf71af88c7c8fc7fa23d8857d26acfa7')

# Create your views here.

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    context = {
        'posts': posts,
        'timestamp': int(datetime.datetime.now().timestamp())
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post,
        'timestamp': int(datetime.datetime.now().timestamp())
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            print(f"New Post Content: {post.content}") # Log post content to terminal
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author and not request.user.is_superuser:
        return redirect('post_detail', pk=post.pk) # Or render an error page

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            print(f"Updated Post Content: {post.content}") # Log updated post content to terminal
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author and not request.user.is_superuser:
        return redirect('post_detail', pk=post.pk) # Or render an error page

    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

@login_required
def emoji_upload(request):
    emojis = Emoji.objects.all()
    if request.method == 'POST':
        form = EmojiForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            image_file = request.FILES['image_file']

            # Upload to imgbb
            response = requests.post(
                'https://api.imgbb.com/1/upload',
                params={'key': IMGBB_API_KEY},
                files={'image': image_file.read()}
            )
            response.raise_for_status()  # Raise an exception for HTTP errors
            imgbb_data = response.json()

            if imgbb_data['success']:
                image_url = imgbb_data['data']['url']
                Emoji.objects.create(name=name, image=image_url)
                _save_media_json() # Update JSON after emoji upload
                return redirect('emoji_upload')
            else:
                # Handle imgbb upload failure
                form.add_error(None, "Image upload to imgbb failed.")
    else:
        form = EmojiForm()
    return render(request, 'blog/emoji_upload.html', {'form': form, 'emojis': emojis})

@login_required
def sticker_upload(request):
    stickers = Sticker.objects.all()
    if request.method == 'POST':
        form = StickerForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            image_file = request.FILES['image_file']

            # Upload to imgbb
            response = requests.post(
                'https://api.imgbb.com/1/upload',
                params={'key': IMGBB_API_KEY},
                files={'image': image_file.read()}
            )
            response.raise_for_status()  # Raise an exception for HTTP errors
            imgbb_data = response.json()

            if imgbb_data['success']:
                image_url = imgbb_data['data']['url']
                Sticker.objects.create(name=name, image=image_url)
                _save_media_json() # Update JSON after sticker upload
                return redirect('sticker_upload')
            else:
                # Handle imgbb upload failure
                form.add_error(None, "Image upload to imgbb failed.")
    else:
        form = StickerForm()
    return render(request, 'blog/sticker_upload.html', {'form': form, 'stickers': stickers})

@login_required
def emoji_delete(request, pk):
    emoji = get_object_or_404(Emoji, pk=pk)
    if not request.user.is_superuser:
        return redirect('emoji_upload') # Or render an error page

    if request.method == "POST":
        emoji.delete()
        _save_media_json() # Update JSON after emoji deletion
        return redirect('emoji_upload')
    return render(request, 'blog/emoji_confirm_delete.html', {'emoji': emoji})

@login_required
def sticker_delete(request, pk):
    sticker = get_object_or_404(Sticker, pk=pk)
    if not request.user.is_superuser:
        return redirect('sticker_upload') # Or render an error page

    if request.method == "POST":
        sticker.delete()
        _save_media_json() # Update JSON after sticker deletion
        return redirect('sticker_upload')
    return render(request, 'blog/sticker_confirm_delete.html', {'sticker': sticker})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') # Redirect to login page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# Helper function to export media data to JSON file
def _save_media_json():
    emojis_data = []
    for emoji in Emoji.objects.all():
        emojis_data.append({'name': emoji.name, 'image_url': emoji.image})

    stickers_data = []
    for sticker in Sticker.objects.all():
        stickers_data.append({'name': sticker.name, 'image_url': sticker.image})

    data = {
        'emojis': emojis_data,
        'stickers': stickers_data,
    }

    file_path = settings.BASE_DIR / 'media_data.json'
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Successfully saved media data to {file_path}")
    except Exception as e:
        print(f"Error saving media data to {file_path}: {e}")

def get_media_json(request):
    emojis_data = []
    for emoji in Emoji.objects.all():
        standardized_name = emoji.name.lower().replace(' ', '')
        emojis_data.append({'name': standardized_name, 'image': emoji.image})

    stickers_data = []
    for sticker in Sticker.objects.all():
        standardized_name = sticker.name.lower().replace(' ', '')
        stickers_data.append({'name': standardized_name, 'image': sticker.image})

    data = {
        'emojis': emojis_data,
        'stickers': stickers_data,
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def export_media_json(request):
    if not request.user.is_superuser:
        return redirect('post_list') # Redirect non-superusers

    _save_media_json()
    # Redirect back to the media upload page or a confirmation page
    return redirect('emoji_upload')

@login_required
def font_upload(request):
    fonts = Font.objects.all()
    if request.method == 'POST':
        form = FontForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            display_name = form.cleaned_data['display_name']
            font_weight = form.cleaned_data['font_weight']
            font_style = form.cleaned_data['font_style']
            font_file = request.FILES['font_file']

            # Determine font format from file extension
            file_extension = font_file.name.lower().split('.')[-1]
            format_mapping = {
                'ttf': 'truetype',
                'otf': 'opentype',
                'woff': 'woff',
                'woff2': 'woff2'
            }
            font_format = format_mapping.get(file_extension, 'opentype')

            # Create font instance - Django will handle file storage automatically
            font = Font.objects.create(
                name=name,
                display_name=display_name,
                font_file=font_file,
                font_format=font_format,
                font_weight=font_weight,
                font_style=font_style
            )

            return redirect('font_upload')
    else:
        form = FontForm()

    context = {
        'form': form,
        'fonts': fonts,
        'timestamp': int(datetime.datetime.now().timestamp())
    }
    return render(request, 'blog/font_upload.html', context)

@login_required
def font_delete(request, pk):
    font = get_object_or_404(Font, pk=pk)
    if not request.user.is_superuser:
        return redirect('font_upload')

    if request.method == "POST":
        font.delete()
        return redirect('font_upload')

    context = {
        'font': font,
        'timestamp': int(datetime.datetime.now().timestamp())
    }
    return render(request, 'blog/font_confirm_delete.html', context)

def dynamic_fonts_css(request):
    """Generate CSS with proper @font-face declarations for all fonts"""
    css_rules = []

    # Include built-in AftaSans fonts
    css_rules.append('''
/* AftaSans Regular Font (Built-in) */
@font-face {
    font-family: "AftaSans";
    src: url("/static/blog/fonts/AftaSansThin-Regular.otf") format("opentype");
    font-weight: normal;
    font-style: normal;
    font-display: swap;
}

/* AftaSans Italic Font (Built-in) */
@font-face {
    font-family: "AftaSans";
    src: url("/static/blog/fonts/AftaSansThin-Italic.otf") format("opentype");
    font-weight: normal;
    font-style: italic;
    font-display: swap;
}

/* Built-in font utility classes */
.ql-font-aftasans {
    font-family: "AftaSans", sans-serif !important;
}

.ql-editor .ql-font-aftasans {
    font-family: "AftaSans", sans-serif !important;
}''')

    # Add uploaded fonts from database
    for font in Font.objects.all():
        # Use the file URL from Django's file storage
        font_url = font.font_file.url if font.font_file else ""

        font_rule = f'''
/* {font.display_name} */
@font-face {{
    font-family: "{font.display_name}";
    src: url("{font_url}") format("{font.font_format}");
    font-weight: {font.font_weight};
    font-style: {font.font_style};
    font-display: swap;
}}

/* Quill editor utility class for {font.name} */
.ql-font-{font.name} {{
    font-family: "{font.display_name}", sans-serif !important;
}}

.ql-editor .ql-font-{font.name} {{
    font-family: "{font.display_name}", sans-serif !important;
}}'''
        css_rules.append(font_rule)

    css_content = '\n'.join(css_rules)

    response = HttpResponse(css_content, content_type="text/css")
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    response['Access-Control-Allow-Origin'] = '*'
    return response

def dynamic_fonts_list(request):
    """Return list of available fonts for the editor"""
    fonts_list = ["aftasans"]  # Built-in font

    # Add uploaded fonts from database
    for font in Font.objects.all():
        fonts_list.append(font.name)

    response = HttpResponse(json.dumps(fonts_list), content_type="application/json")
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    response['Access-Control-Allow-Origin'] = '*'
    return response
