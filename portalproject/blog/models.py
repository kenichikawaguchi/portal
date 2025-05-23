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

from markdownx.models import MarkdownxField
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify

from django.db.models.query import QuerySet
from django.db.models import Count, Case, IntegerField, When


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
                if current.photo == None or previous.photo != current.photo:
                    if previous.photo_small:
                        os.remove(previous.photo_small.path)
                    os.remove(previous.photo.path)
                    try:
                        os.rmdir(os.path.dirname(previous.photo.path))
                    except OSError as e:
                        pass
                    try:
                        os.rmdir(os.path.dirname(previous.photo_small.path))
                    except OSError as e:
                        pass
            if previous.photo2:
                if current.photo2 == None or previous.photo2 != current.photo2:
                    if previous.photo2_small:
                        os.remove(previous.photo2_small.path)
                    os.remove(previous.photo2.path)
                    try:
                        os.rmdir(os.path.dirname(previous.photo2.path))
                    except OSError as e:
                        pass
                    try:
                        os.rmdir(os.path.dirname(previous.photo2_small.path))
                    except OSError as e:
                        pass
            if previous.photo3:
                if current.photo3 == None or previous.photo3 != current.photo3:
                    if previous.photo3_small:
                        os.remove(previous.photo3_small.path)
                    os.remove(previous.photo3.path)
                    try:
                        os.rmdir(os.path.dirname(previous.photo3.path))
                    except OSError as e:
                        pass
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


class Category(models.Model):
    owner = models.ForeignKey(CustomUser, verbose_name="Owner", on_delete=models.PROTECT)
    name = models.CharField('Category', max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"],
                name="category_unique"
            )
        ]

    def __str__(self):
        return f'{self.owner} {self.name}'


class BlogPost(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="Author", on_delete=models.PROTECT)
    title = models.CharField(verbose_name="Title", max_length=200)
    category = models.ForeignKey(Category, verbose_name="Category", null=True, blank=True, on_delete=models.PROTECT)
    # content = models.TextField(verbose_name="Content")
    content = MarkdownxField(verbose_name="Content")
    is_public = models.BooleanField('public content?', default=True)
    only_friends = models.BooleanField('only-friends content?', default=False)
    photo = models.ImageField(verbose_name="Photo", upload_to=rename_image, blank=True, null=True)
    photo2 = models.ImageField(verbose_name="Photo2", upload_to=rename_image, blank=True, null=True)
    photo3 = models.ImageField(verbose_name="Photo3", upload_to=rename_image, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated at", auto_now=True)

    photo_small = ImageSpecField(source="photo", processors=[processors.Transpose(), ResizeToFill(200, 200)], format="JPEG")
    photo2_small = ImageSpecField(source="photo2", processors=[processors.Transpose(), ResizeToFill(200, 200)], format="JPEG")
    photo3_small = ImageSpecField(source="photo3", processors=[processors.Transpose(), ResizeToFill(200, 200)], format="JPEG")

    @staticmethod
    def with_state(user_id: int) -> QuerySet:
        return BlogPost.objects.annotate(
            like_cnt=Count('likes_on_blogposts'),
            liked_by_me = Case(
                When(id__in=Like.objects.filter(user_id=user_id).values('blogpost_id'),
                    then=1),
                default=0,
                output_field=IntegerField()
            )
        )

    def my_categories(self, user_id):
        return Category.objects.filter(owner_id=user_id).values('category_id')

    def get_text_markdownx(self):
        return mark_safe(markdownify(self.content))

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

    def is_correct_category(self):
        return self.user == self.category.owner


class Comment(models.Model):
    text = MarkdownxField(verbose_name="Comment", blank=False)
    commenter = models.ForeignKey(CustomUser, verbose_name="Commenter", on_delete=models.CASCADE)
    comment_to = models.ForeignKey(BlogPost, verbose_name="Blog Post", related_name="comments", on_delete=models.CASCADE, blank=True, null=True)
    reply_to = models.ForeignKey('self', related_name="replies", on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated at", auto_now=True)

    def get_text_markdownx(self):
        return mark_safe(markdownify(self.text))

    class Meta:
        db_table = "comments"

    def __str__(self):
        return f'{self.pk} {self.text[:15] } *BY* {self.commenter} *TO* {self.comment_to}'


class Like(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="User", on_delete=models.CASCADE)
    blogpost = models.ForeignKey(BlogPost, verbose_name="Blog Post", related_name="likes_on_blogposts", on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, verbose_name="Comment", related_name="likes_on_comments", on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated at", auto_now=True)

    class Meta:
        db_table = "likes"
        constraints = [
            models.UniqueConstraint(
                fields=['blogpost_id', 'user_id'],
                name='blogpost_user_unique'
            ),
            models.UniqueConstraint(
                fields=['comment_id', 'user_id'],
                name='comment_user_unique'
            ),
        ]

    def __str__(self):
        return f'{self.pk} {self.user} {self.blogpost} {self.comment}'


class Tag(models.Model):
    name = models.CharField(verbose_name="Tag", max_length=32)
    blogposts = models.ManyToManyField(BlogPost, related_name="tags",
                                                related_query_name='tag')

    class Meta:
        db_table = "tags"

    def __str__(self):
        return f'{self.pk} {self.name}'


class ClientIP(models.Model):
    ip = models.CharField(verbose_name="IP Address", max_length=32)
    city = models.CharField(verbose_name="City", blank=True, null=True, max_length=32)
    country_code = models.CharField(verbose_name="Country Code", blank=True, null=True, max_length=32)
    country_name = models.CharField(verbose_name="Country Name", blank=True, null=True, max_length=32)
    page = models.CharField(verbose_name="Access Page", max_length=511)
    user = models.ForeignKey(CustomUser, verbose_name="User", blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)

    def __str__(self):
        return f'{self.pk} {self.ip} {self.city} {self.page} {self.user} {self.created_at}'


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
