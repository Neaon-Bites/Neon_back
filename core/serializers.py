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
        fields = '__all__'

class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = '__all__'
        read_only_fields = ['created_at']

class SiteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteUser
        fields = '__all__'
        read_only_fields = ['created_at']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['created_at', 'is_approved']