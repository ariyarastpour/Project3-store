from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,View
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Review
from .forms import ReviewForm
from django.http import JsonResponse
from accounts.models import Profile

class ReviewView(LoginRequiredMixin, CreateView):
    http_method_names = ["post"]
    queryset = Review.objects.filter(status=1)
    form_class = ReviewForm
    login_url = '/shop/products/'

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form.instance.user = profile
        review = form.save()
        messages.success(self.request ,"دیدگاه شما با موفقیت ثبت شد")
        return redirect(
            reverse_lazy("shop:detail", kwargs={"pk":review.product.id})
        )
    
    def form_invalid(self, form):
        for fields, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return redirect(self.request.META.get("HTTP_REFERER"))
    

class LikeView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, review_id):
        review = Review.objects.filter(status=1).get(id=review_id)
        user = request.user

        if review.is_liked_by(user):
            review.likes.remove(user)

        else:
            review.likes.add(user)
            review.dislikes.remove(user)
        
        return JsonResponse({
            'likes': review.totlal_likes,
            'dislikes': review.totlal_dislikes
        })
    
class DislikeView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, review_id):
        review = Review.objects.filter(status=1).get(id=review_id)
        user = request.user

        if review.is_disliked_by(user):
            review.dislikes.remove(user)

        else:
            review.dislikes.add(user)
            review.likes.remove(user)

        return JsonResponse({
            'likes': review.total_likes,
            'dislikes': review.total_dislikes
        })
        

class ReplyReviewView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, review_id):
        parent_review = Review.objects.filter(status=1).get(id=review_id)
        content = request.POST.get('content')

        if content:
            profile = Profile.objects.get(user=request.user)
            reply = Review.objects.create(
                user = profile,
                product = parent_review.product,
                description = content,
                parent = parent_review
            )

            return JsonResponse({
                'success': True,
                'reply_id': reply.id,
                'content': reply.description,
                'username': request.user.email,
                'created_date': reply.created_date.strftime('%Y-%m-%d'),
            })