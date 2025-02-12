from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from uuid import uuid4
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit import processors
import os

from markdownx.models import MarkdownxField
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify

from django.db.models import Prefetch
from django.db.models.expressions import RawSQL


def delete_previous_file(function):
    def wrapper(*args, **kwargs):
        self = args[0]
        result = CustomUser.objects.filter(pk=self.pk)
        previous = result[0] if len(result) else None

        result = function(*args, **kwargs)

        result = CustomUser.objects.filter(pk=self.pk)
        current = result[0] if len(result) else None

        if previous:
            if previous.icon:
                if current.icon == None or previous.icon != current.icon:
                    if previous.icon_small:
                        os.remove(previous.icon_small.path)
                    os.remove(previous.icon.path)
                    try:
                        os.rmdir(os.path.dirname(previous.icon.path))
                    except OSError as e:
                        pass
                    try:
                        os.rmdir(os.path.dirname(previous.icon_small.path))
                    except OSError as e:
                        pass

        return result
    return wrapper


def rename_image(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return filename


class CustomUser(AbstractUser):
    ''' Extended Uer Model '''
    introduction = MarkdownxField(verbose_name="Introduction", default="")
    icon = models.ImageField(verbose_name="Icon", upload_to=rename_image, blank=True, null=True)
    icon_small = ImageSpecField(source="icon", processors=[processors.Transpose(), ResizeToFill(200, 200)], format='JPEG')

    class Meta:
        verbose_name_plural = 'CustomUser'

    def friends(self):
        friends = CustomUser.objects.filter(id__in=RawSQL('SELECT connect_A.follower_id FROM accounts_connection as connect_A INNER JOIN accounts_connection as connect_B on connect_A.follower_id = connect_B.following_id WHERE connect_A.following_id = ' + str(self.id) + ' AND connect_B.follower_id = ' + str(self.id), []))

        return friends

    def get_text_markdownx(self):
        return mark_safe(markdownify(self.introduction))

    @delete_previous_file
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(CustomUser, self).save()


class Connection(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(self.follower.username, self.following.username)

