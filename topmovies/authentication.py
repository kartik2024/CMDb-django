from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrPhoneBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if '@' in username:
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(profile__phone=username)  # assuming phone is in a related Profile model
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def user_can_authenticate(self, user):
        return user.is_active

    def get_user(self, user_id):  # ✅ Add this
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
