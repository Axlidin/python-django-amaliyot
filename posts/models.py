from django.utils import timezone
from django.db import models
from taggit.managers import TaggableManager
from users.models import CustomUser

class   Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    title = models.CharField(max_length=250)
    content = models.TextField()
    image = models.ImageField(default='defaukt_post_image.png')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='user_posts')
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title

class PostVisit(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='visit_logs')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Visit on {self.timestamp} for post {self.post.title}'

class Reviews(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='izohlar')
    review_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Review by {self.user.username} on {self.post.title}'