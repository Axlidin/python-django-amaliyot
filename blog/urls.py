from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from posts.views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name='landing_page'),
    path("posts/", include("posts.urls")),
    path("users/", include("users.urls")),
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
