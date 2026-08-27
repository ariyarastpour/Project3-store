from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    path("submit-review/", views.ReviewView.as_view(), name="submit-review"),
    path('review/create/<int:product_id>/', views.ReviewView.as_view(), name='create_review'),
    path('review/<int:review_id>/like/', views.LikeView.as_view(), name='like_review'),
    path('review/<int:review_id>/dislike/', views.DislikeView.as_view(), name='dislike_review'),
    path('review/<int:review_id>/reply/', views.ReplyReviewView.as_view(), name='reply_review'),
]