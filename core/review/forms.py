from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["product", "rate", "description"]

        error_messages = {
            "description": {
                "required": "فیلد توضیحات اجباری است",
            },
        }