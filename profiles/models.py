from django.contrib.auth.models import User
from django.db import models
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
import hashlib


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'user_profile'

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False


    def profile_image_url(self):
        fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')

        if len(fb_uid):
            return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)

        # return "http://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.user.email).hexdigest())

        return "http://www.gravatar.com/avatar/{0}?s={1}".format(hashlib.md5(self.user.email.encode('UTF-8')).hexdigest(),40)

    User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

    #profile_username = User.username
    #profile_firstname = User.first_name
    #profile_lastname = User.last_name
    #profile_datejoined = User.date_joined
    #profile_email = User.email
    #profile_lastloging = User.last_login
    #profile_id = User.id
    #profile_isactive = User.is_active
    #profile_img_url=profile_image_url(user)
    #profile_account_verified = account_verified(user)


# Create your models here.
