from django.urls import path
from .views import (BlogListView,
                    BlogDetailView,
                    BlogCreateView,
                    BlogUpdateView,
                    BlockDeleteView)

urlpatterns = [
    path('', BlogListView.as_view(), name='home'),
    path('post/<int:pk>/', BlogDetailView.as_view(), name='single_post'),
    path('post/new/', BlogCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', BlogUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete', BlockDeleteView.as_view(), name='post_delete')
]
