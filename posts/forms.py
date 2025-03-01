from django import forms
from posts.models import Reviews, Category
from .models import Post
class PostReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ('review_text',)

class AddPostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Kategoriyani tanlang")
    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'category', 'tags')


