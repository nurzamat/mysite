from rest_framework import serializers, pagination
from azat.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name', 'code', 'phone_code')


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('name', 'country')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('name', 'region')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ('user', 'name', 'phone', 'api_key', 'status', 'created_at', 'gcm_registration_id', 'profile_image')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'original_image')


# Category posts
class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    user = UserSerializer()
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created_at', 'status', 'category',
                  'hitcount', 'user', 'type', 'price', 'images')


class OrderItemSerializer(serializers.ModelSerializer):
    post = PostSerializer()

    class Meta:
        model = OrderItem
        fields = ('order', 'post', 'amount', 'sum')


class OrderItemAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('order', 'post', 'amount', 'sum')


class OrderSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    #order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'total', 'status', 'creation_date')
