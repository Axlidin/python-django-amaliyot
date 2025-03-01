from django.urls import path

from posts.views import PostListView, PostDetailView, AddPostReviewView, EditReviewView, ConfirmDeleteReviewView, \
    DeleteReviewView, AddPostView

app_name = 'posts'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:id>/', PostDetailView.as_view(), name='detail'),
    path("<int:id>/reviews/", AddPostReviewView.as_view(), name='reviews'),
    path("<int:post_id>/reviews/<int:review_id>/edit/", EditReviewView.as_view(), name='edit_review'),
    path("<int:post_id>/reviews/<int:review_id>/delete/confirm", ConfirmDeleteReviewView.as_view(), name='confirm-delete-review'),
    path("<int:post_id>/reviews/<int:review_id>/delete", DeleteReviewView.as_view(), name='delete-review'),
    path("create/", AddPostView.as_view(), name='create')

]
