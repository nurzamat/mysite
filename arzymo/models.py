from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import datetime
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from imagekit import ImageSpec
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit, Adjust
from rest_framework.authtoken.models import Token


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    phone_code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=50)
    region = models.ForeignKey(Region)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    password_hash = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=40, null=True)
    api_key = models.CharField(max_length=50, null=True)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(null=True)
    gcm_registration_id = models.TextField
    profile_image = ProcessedImageField(upload_to='profile',
                                        processors=[ResizeToFill(300, 300)],
                                        format='JPEG',
                                        options={'quality': 60})

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=4096)
    created_at = models.DateTimeField('date created')
    status = models.IntegerField(default=0)
    statusChangeDate = models.DateTimeField('change date')
    category = models.ForeignKey(Category)
    hitcount = models.IntegerField(default=0)
    user = models.ForeignKey(User)
    type = models.IntegerField(default=0) #post type or category type
    actionType = models.IntegerField(default=0)
    phone = models.CharField(max_length=30)
    location = models.ForeignKey(Location)

    def __str__(self):
        return self.title


class AutoPost(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, parent_link=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_currency = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        self.post.save()
        super().save(*args, **kwargs)


class DatingPost(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, parent_link=True)
    sex = models.BooleanField(default=0)
    birth_year = models.DateField(blank=True)

    def save(self, *args, **kwargs):
        self.post.save()
        super().save(*args, **kwargs)


class Image(models.Model):
    image = ProcessedImageField(upload_to='post_image',
                                processors=[ResizeToFill(300, 300)],
                                format='JPEG',
                                options={'quality': 60})
    post = models.ForeignKey(Post)


class Like(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)


class ChatRoom(models.Model):
    name = models.CharField(max_length=200)
    create_at = models.DateTimeField('date created')

    def __str__(self):
        return self.name


class Chat(models.Model):
    post = models.ForeignKey(Post)
    idUser1 = models.IntegerField(default=0)
    idUser2 = models.IntegerField(default=0)
    isActive1 = models.BooleanField(default=1)
    isActive2 = models.BooleanField(default=1)
    deleted_at1 = models.DateTimeField(blank=True)
    deleted_at2 = models.DateTimeField(blank=True)
    created_at = models.DateTimeField('date created')


class Message(models.Model):
    chat = models.ForeignKey(Chat)
    owner = models.ForeignKey(User)
    message = models.TextField
    created_at = models.DateTimeField('date created')


# RECEIVERS
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Token.objects.get_or_create(user=instance)


"""@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
"""


# Delete image files on image instance deletion.
@receiver(post_delete, sender=Image)
def image_post_delete_handler(sender, **kwargs):
    image = kwargs['instance']
    storage, path = image.original_image.storage, image.original_image.path
    storage.delete(path)
