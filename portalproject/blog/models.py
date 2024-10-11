from django.db import models
from django.urls import reverse
from accounts.models import CustomUser
from uuid import uuid4
import os


def rename_image(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(path, filename)
    return wrapper


class BlogPost(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="Author", on_delete=models.PROTECT)
    title = models.CharField(verbose_name="Title", max_length=200)
    content = models.TextField(verbose_name="Content")
    photo = models.ImageField(verbose_name="Photo", upload_to=rename_image(''), blank=True, null=True)
    photo2 = models.ImageField(verbose_name="Photo2", upload_to=rename_image(''), blank=True, null=True)
    photo3 = models.ImageField(verbose_name="Photo3", upload_to=rename_image(''), blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated at", auto_now=True)

    class Meta:
        db_table = "blogposts"

    def __str__(self):
        return f'{self.pk} {self.title}'

    def is_updated(self):
        delta_updated_at_created_at = self.updated_at - self.created_at
        if delta_updated_at_created_at.seconds < 1:
            return False
        return True

    def get_absolute_url(self):
        return reverse("blog:blog_detail", kwargs={"pk": self.pk})

class Comment(models.Model):
    text = models.TextField(verbose_name="Comment", blank=False)
    commenter = models.ForeignKey(CustomUser, verbose_name="Commenter", on_delete=models.CASCADE)
    comment_to = models.ForeignKey(BlogPost, verbose_name="Blog Post", on_delete=models.CASCADE)

    class Meta:
        db_table = "comments"

    def __str__(self):
        return f'{self.pk} {self.title}'


class Tag(models.Model):
    name = models.CharField(verbose_name="Tag", max_length=32)
    blogposts = models.ManyToManyField(BlogPost, related_name="tags",
                                                related_query_name='tag')

    class Meta:
        db_table = "tags"

    def __str__(self):
        return f'{self.pk} {self.name}'
