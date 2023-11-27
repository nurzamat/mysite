from django.db import models
from django.contrib.auth.models import User
from imagekit import ImageSpec
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit, Adjust
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

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
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=50)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100, null=True)
    content = models.CharField(max_length=4096)
    user = models.ForeignKey(User, default='', related_name='posts', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='category_posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.IntegerField(default=0, null=True)
    hitcount = models.IntegerField(default=0, null=True)
    type = models.IntegerField(default=0, null=True)  # post type or category type
    # statusChangeDate = models.DateTimeField('change date')
    # actionType = models.IntegerField(default=0)
    # phone = models.CharField(max_length=30)
    # location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Image(models.Model):
    reindex_related = ('post',)
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    original_image = ProcessedImageField(upload_to='post_images',
                                         default='',
                                         processors=[ResizeToFit(640, 640)],
                                         format='JPEG',
                                         options={'quality': 75})
    image_main_page = ImageSpecField(source='original_image',
                                     processors=[ResizeToFill(225, 180),
                                                 Adjust(contrast=1.2, sharpness=1.1)],
                                     format='JPEG',
                                     options={'quality': 60})
    image_post_page = ImageSpecField(source='original_image',
                                     processors=[ResizeToFit(640, 640),
                                                 Adjust(contrast=1.2, sharpness=1.1)],
                                     format='JPEG',
                                     options={'quality': 75})


def identicon_url(source, size):
        return '/identicon/image/' + source + '.png?w=' + size + '&h=' + size


class Thumbnail(ImageSpec):
    processors = [ResizeToFill(30, 30), Adjust(contrast=1.2, sharpness=1.1)]
    format = 'JPEG'
    options = {'quality': 80}


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)


class UserProfile(models.Model):
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
    displayed_name = models.CharField(max_length=60, default='', blank=True)
    avatar_original_image = ProcessedImageField(upload_to='avatars',
                                                default='',
                                                processors=[ResizeToFit(480, 480)],
                                                format='JPEG',
                                                blank=True,
                                                options={'quality': 75})
    profile_image = ProcessedImageField(upload_to='profile',
                                        default='',
                                        processors=[ResizeToFill(300, 300)],
                                        format='JPEG',
                                        blank=True,
                                        options={'quality': 60})

    def avatar_30(self):
        if self.avatar_original_image:
            avatar = Thumbnail(source=self.avatar_original_image)
            return '/media/' + avatar.cachefile_name
        else:
            #set 10px less size since 5px padding. See settings for PYDENTICON_PADDING
            return identicon_url(self.user.username, '30')

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.IntegerField(default=0)  #0-bucket 1-order 2-done 3-canceled
    creation_date = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return str(self.pk)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    sum = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return str(self.pk)


class ChatRoom(models.Model):
    name = models.CharField(max_length=200)
    create_at = models.DateTimeField('date created')

    def __str__(self):
        return self.name


class Chat(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    idUser1 = models.IntegerField(default=0)
    idUser2 = models.IntegerField(default=0)
    isActive1 = models.BooleanField(default=1)
    isActive2 = models.BooleanField(default=1)
    deleted_at1 = models.DateTimeField(blank=True)
    deleted_at2 = models.DateTimeField(blank=True)
    created_at = models.DateTimeField('date created')


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField
    created_at = models.DateTimeField('date created')


# RECEIVERS
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        Token.objects.get_or_create(user=instance)


# Delete image files on image instance deletion.
@receiver(post_delete, sender=Image)
def image_post_delete_handler(sender, **kwargs):
    image = kwargs['instance']
    storage, path = image.original_image.storage, image.original_image.path
    storage.delete(path)


# Create API token on user creation.
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)
