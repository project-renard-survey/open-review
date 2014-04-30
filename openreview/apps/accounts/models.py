from django.contrib.auth.models import AbstractUser
from openreview.apps.main.models.review import bulk_delete
from django.db import models


class User(AbstractUser):
    """Copies properties of default User model. Defining it ourselves
    adds the ability to add/change properties later on without too much
    hassle."""

    title = models.CharField(max_length=20, null=True, blank=True)
    university = models.CharField(max_length=100, null=True, blank=True)
    votes_public = models.BooleanField(default=False)

    def delete(self, delete_reviews=False):
        if delete_reviews:
            bulk_delete(self.reviews.all())
        else:
            self.reviews.all().update(poster=None, anonymous=True)
        super().delete()

    def full_name(self):
        name = "{first} {last}".format(first=self.first_name, last=self.last_name) if \
            self.first_name and self.last_name else "{{}}".format(self.username)
        title = " ({title}, {university})".format(title=self.title, university = self.university) if \
            self.title and self.university else ""
        return name+title

