from django.db import models
from django.contrib.auth.models import User
import uuid

class Profile(models.Model):
    """
    Extend User with moar information.
    """
    user = models.OneToOneField(User, related_name='s2g_profile')
    s2g_email = models.EmailField(null=True)

    def save(self, *args, **kwargs):
        """
        On save, if this object doesn't have a proper s2g_email, we generate
        one randomly.
        """
        if self.s2g_email is None:
            generated_okay = False

            while not generated_okay:
                u = str(uuid.uuid4())[-8:]        # 8 random chars
                email = "s2g_%s" % u

                if not Profile.objects.filter(s2g_email=email).exists():
                    self.s2g_email = email
                    generated_okay = True

        return super(Profile, self).save(*args, **kwargs)

# http://stackoverflow.com/questions/13460426/get-user-profile-in-django
# http://stackoverflow.com/a/10575330/402605 (don't create superuser during syncdb)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

models.signals.post_save.connect(create_user_profile, sender=User)