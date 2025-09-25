from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

class Emoji(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.URLField(max_length=200)

    def __str__(self):
        return self.name

class Sticker(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.URLField(max_length=200)

    def __str__(self):
        return self.name

def font_upload_path(instance, filename):
    """Generate upload path for font files"""
    return f'fonts/{filename}'

class Font(models.Model):
    name = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100)
    font_file = models.FileField(upload_to=font_upload_path)  # Local file storage
    font_format = models.CharField(max_length=20, choices=[
        ('truetype', 'TTF'),
        ('opentype', 'OTF'),
        ('woff', 'WOFF'),
        ('woff2', 'WOFF2')
    ], default='opentype')
    font_weight = models.CharField(max_length=20, default='normal')
    font_style = models.CharField(max_length=20, choices=[
        ('normal', 'Normal'),
        ('italic', 'Italic'),
        ('oblique', 'Oblique')
    ], default='normal')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name_plural = "Fonts"

    def delete(self, *args, **kwargs):
        """Delete the font file when the model instance is deleted"""
        if self.font_file:
            try:
                self.font_file.delete(save=False)
            except:
                pass
        super().delete(*args, **kwargs)
