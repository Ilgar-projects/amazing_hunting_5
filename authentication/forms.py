from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class SignUpForm(UserCreationForm):
    """Простая регистрация: username + email + password."""

    email = forms.EmailField(required=True, label="Email")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if not email:
            raise forms.ValidationError("Email обязателен.")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
        return email
