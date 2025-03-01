from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views import View
from posts.forms import PostReviewForm, AddPostForm
from posts.models import Post, Reviews

class HomeView(View):
    def get(self, request):
        latest_posts = Post.objects.filter(status='published').order_by('-created_at')[:5]

        context = {
            'posts': latest_posts,
        }
        return render(request, 'landing_page.html', context)

class AddPostView(View):
    def get(self, request):
        post_form = AddPostForm()
        context = {
            'post_form': post_form,
        }
        return render(request, 'posts/add_post.html', context)

    def post(self, request):
        post_form = AddPostForm(request.POST, request.FILES)

        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.status = 'Draft'
            post.save()
            return redirect('posts:post_list')

        return render(request, 'posts/add_post.html', {'post_form': post_form})  # Xatolik bo‘lsa, formani qaytarish

class PostListView(View):
    def get(self, request):
        posts = Post.objects.filter(status='published').order_by('-created_at')
        return render(request, 'posts/post_list.html', {'posts': posts})

class PostDetailView(View):
    def get(self, request, id):
        post = Post.objects.get(id=id)
        review_form = PostReviewForm()
        reviews = post.izohlar.all().order_by('-created_at')
        context = {
            'post': post,
            'review_form': review_form,
            'reviews': reviews,
        }
        return render(request, 'posts/post_detail.html', context)

class AddPostReviewView(View):
    def post(self, request, id):
        post = Post.objects.get(id=id)
        reviews = post.izohlar.all().order_by('-created_at')
        review_form = PostReviewForm(data=request.POST)
        if review_form.is_valid():
            Reviews.objects.create(
                post=post,
                user=request.user,
                review_text=review_form.cleaned_data['review_text'],
            )
            return redirect(reverse("posts:detail", kwargs={'id': post.id}))
        context = {
            'post': post,
            'review_form': review_form,
            'reviews': reviews,
        }
        return render(request, 'posts/post_detail.html', context)

class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, post_id, review_id):
        post = Post.objects.get(id=post_id)
        revirew = post.izohlar.get(id=review_id)
        review_form =PostReviewForm(instance=revirew)
        context = {
                    'post': post,
                    'review': revirew,
                    'review_form': review_form,
                    }
        return render(request, 'posts/edit_review.html', context)

    def post(self, request, post_id, review_id):
        post = Post.objects.get(id=post_id)
        revirew = post.izohlar.get(id=review_id)
        review_form = PostReviewForm(instance=revirew, data=request.POST)
        if review_form.is_valid():
            revirew.review_text = review_form.cleaned_data['review_text']
            revirew.save()
            return redirect(reverse("posts:detail", kwargs={'id': post.id}))
        context = {
            'post': post,
            'review': revirew,
            'review_form': review_form,
        }
        return render(request, 'posts/edit_review.html', context)

class ConfirmDeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, post_id, review_id):
        post = Post.objects.get(id=post_id)
        revirew = post.izohlar.get(id=review_id)
        context = {
            'post': post,
            'review': revirew,
        }
        return render(request, 'posts/confirm_delete.html', context)

class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, post_id, review_id):
        post = Post.objects.get(id=post_id)
        revirew = post.izohlar.get(id=review_id)
        revirew.delete()
        messages.success(request, "You have successfully deleted this review")
        return redirect(reverse("posts:detail", kwargs={'id': post.id}))