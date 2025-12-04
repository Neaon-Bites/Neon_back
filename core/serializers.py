from rest_framework import serializers
from .models import SuperAdmin, Influencer, Site, Page, Publication, SiteUser, Comment

class SuperAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperAdmin
        fields = '__all__'

class InfluencerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Influencer
        fields = '__all__'
        read_only_fields = ['created_at']

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'
        read_only_fields = ['created_at']

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'title', 'slug', 'is_published', 'created_at', 'site']
        read_only_fields = ['created_at']

class PublicationSerializer(serializers.ModelSerializer):
    media_assets = serializers.JSONField(required=False, allow_null=True)

    class Meta:
        model = Publication
        fields = ['id', 'title', 'category', 'content_text', 'media_assets', 'created_at', 'page']
        read_only_fields = ['created_at']

class SiteUserSerializer(serializers.ModelSerializer):
    password_hash = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = SiteUser
        fields = ['id', 'username', 'email', 'password_hash', 'avatar_url', 'created_at', 'site']
        read_only_fields = ['created_at']

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'media_url', 'is_approved', 'created_at', 'publication', 'author', 'author_username']
        read_only_fields = ['created_at', 'is_approved'] 
        