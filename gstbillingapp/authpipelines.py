from .models import UserProfile
from .models import BillingProfile


def create_profile(backend, user, response, *args, **kwargs):
    print("===>", user)
    if UserProfile.objects.filter(user=user).exists():
        pass
    else:
        new_user_profile = UserProfile(user=user)
        new_user_profile.save()
        new_billing_profile = BillingProfile(user=user)
        new_billing_profile.save()
