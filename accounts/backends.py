# accounts/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

Customer = get_user_model()

class PhoneBackend(ModelBackend):
    """
    Authenticate using phone number and password.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        phone = username  # 'username' from form will now be phone
        try:
            user = Customer.objects.get(phone=phone)
            if user.check_password(password):
                return user
        except Customer.DoesNotExist:
            return None
