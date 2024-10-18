from django.conf import settings
from django.db import models
from django.urls import reverse
from accounts.models import CustomUser
from uuid import uuid4
import os
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
from imagekit import processors

from django.db.models.signals import post_delete
from django.dispatch import receiver


def delete_previous_file(function):
    def wrapper(*args, **kwargs):
        self = args[0]
        result = BlogPost.objects.filter(pk=self.pk)
        previous = result[0] if len(result) else None

        result = function(*args, **kwargs)

        result = BlogPost.objects.filter(pk=self.pk)
        current = result[0] if len(result) else None

        if previous:
            if previous.photo:
                print("previous.photo.name:{}".format(previous.photo.name))
                print("previous.photo_small.name:{}".format(previous.photo_small.name))
                print("previous.photo.path_dirname:{}".format(os.path.dirname(previous.photo.path)))
                print("previous.photo_small.path_dirname:{}".format(os.path.dirname(previous.photo_small.path)))
                print("previous.photo.path:{}".format(previous.photo.path))
                print("previous.photo_small.path:{}".format(previous.photo_small.path))

                if current.photo == None or previous.photo != current.photo:
                    os.remove(previous.photo.path)
                    os.remove(previous.photo_small.path)
                    try:
                        os.rmdir(os.path.dirname(previous.photo_small.path))
                    except OSError as e:
                        pass
            if previous.photo2:
                if current.photo2 == None or previous.photo2 != current.photo2:
                    os.remove(previous.photo2.path)
                    os.remove(previous.photo2_small.path)
                    try:
                        os.rmdir(os.path.dirname(previous.photo2_small.path))
                    except OSError as e:
                        pass
            if previous.photo3:
                if current.photo3 == None or previous.photo3 != current.photo3:
                    os.remove(previous.photo3.path)
                    os.remove(previous.photo3_small.path)
                    try:
                        os.rmdir(os.path.dirname(previous.photo3_small.path))
                    except OSError as e:
                        pass

        return result
    return wrapper


def rename_image(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return filename


class BlogPost(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="Author", on_delete=models.PROTECT)
    title = models.CharField(verbose_name="Title", max_length=200)
    content = models.TextField(verbose_name="Content")
    photo = models.ImageField(verbose_name="Photo", upload_to=rename_image, blank=True, null=True)
    photo2 = models.ImageField(verbose_name="Photo2", upload_to=rename_image, blank=True, null=True)
    photo3 = models.ImageField(verbose_name="Photo3", upload_to=rename_image, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated at", auto_now=True)

    photo_small = ImageSpecField(source="photo", processors=[processors.Transpose(), ResizeToFill(200, 200)], format="JPEG")
    photo2_small = ImageSpecField(source="photo2", processors=[processors.Transpose(), ResizeToFill(200, 200)], format="JPEG")
    photo3_small = ImageSpecField(source="photo3", processors=[processors.Transpose(), ResizeToFill(200, 200)], format="JPEG")

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

    @delete_previous_file
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(BlogPost, self).save()


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


@receiver(post_delete,sender=BlogPost)
def delete_photo(sender, instance, **kwargs):
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)

    if instance.photo_small:
        if os.path.isfile(instance.photo_small.path):
            os.remove(instance.photo_small.path)
            try:
                os.rmdir(os.path.dirname(instance.photo_small.path))
            except OSError as e:
                pass

    if instance.photo2:
        if os.path.isfile(instance.photo2.path):
            os.remove(instance.photo2.path)

    if instance.photo2_small:
        if os.path.isfile(instance.photo2_small.path):
            os.remove(instance.photo2_small.path)
            try:
                os.rmdir(os.path.dirname(instance.photo2_small.path))
            except OSError as e:
                pass

    if instance.photo3:
        if os.path.isfile(instance.photo3.path):
            os.remove(instance.photo3.path)

    if instance.photo3_small:
        if os.path.isfile(instance.photo3_small.path):
            os.remove(instance.photo3_small.path)
            try:
                os.rmdir(os.path.dirname(instance.photo3_small.path))
            except OSError as e:
                pass
