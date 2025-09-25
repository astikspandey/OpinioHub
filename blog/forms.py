from django import forms
from .models import Post, Emoji, Sticker, Font

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Post
        fields = ('title', 'content',)

class EmojiForm(forms.ModelForm):
    image_file = forms.ImageField(label='Emoji Image')

    class Meta:
        model = Emoji
        fields = ('name',)

class StickerForm(forms.ModelForm):
    image_file = forms.ImageField(label='Sticker Image')
    class Meta:
        model = Sticker
        fields = ('name',)

class FontForm(forms.ModelForm):
    font_file = forms.FileField(
        label='Font File',
        help_text='Upload TTF, OTF, WOFF, or WOFF2 font files'
    )

    class Meta:
        model = Font
        fields = ('name', 'display_name', 'font_weight', 'font_style')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., roboto-regular (lowercase, no spaces)'
            }),
            'display_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Roboto Regular'
            }),
            'font_weight': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'normal, bold, 400, 700, etc.'
            }),
        }

    def clean_name(self):
        name = self.cleaned_data['name'].lower().replace(' ', '-')
        if not name.replace('-', '').replace('_', '').isalnum():
            raise forms.ValidationError("Font name can only contain letters, numbers, hyphens, and underscores.")
        return name

    def clean_font_file(self):
        font_file = self.cleaned_data['font_file']
        if font_file:
            # Check file extension
            valid_extensions = ['.ttf', '.otf', '.woff', '.woff2']
            file_extension = font_file.name.lower().split('.')[-1] if '.' in font_file.name else ''
            if f'.{file_extension}' not in valid_extensions:
                raise forms.ValidationError(f"Only {', '.join(valid_extensions)} files are allowed.")
        return font_file
