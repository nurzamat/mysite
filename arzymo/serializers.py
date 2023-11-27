from rest_framework import serializers, pagination
from arzymo.models import *


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField('get_children')

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')

    def get_children(context):
        return context.get_children


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
        fields = ('username', 'email', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'name', 'phone', 'api_key', 'status', 'created_at', 'gcm_registration_id', 'profile_image')


# Category posts
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created_at', 'status', 'category', 'hitcount', 'user', 'type',
                  'actionType', 'phone', 'location')


class AutoPostSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)

    class Meta:
        model = AutoPost
        fields = ('price', 'price_currency', 'post')


class DatingPostSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)

    class Meta:
        model = DatingPost
        fields = ('sex', 'birth_year', 'post')

