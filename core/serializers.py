from rest_framework import serializers
from .models import SuperAdmin, Influencer, Site, Page, Publication, SiteUser, Comment
from django.contrib.auth.hashers import make_password

class SuperAdminSerializer(serializers.ModelSerializer):
    # Champ virtuel pour recevoir le mot de passe en clair lors de la création/mise à jour
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = SuperAdmin
        fields = ['id', 'username', 'email', 'password', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        # On extrait le mot de passe, on le hache, et on le stocke dans password_hash
        password = validated_data.pop('password')
        validated_data['password_hash'] = make_password(password)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.password_hash = make_password(password)
        return super().update(instance, validated_data)


class InfluencerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    # On peut inclure les sites pour voir la liste des sites de l'influenceur (lecture seule)
    sites = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Influencer
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture', 'created_at', 'sites']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password_hash'] = make_password(password)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.password_hash = make_password(password)
        return super().update(instance, validated_data)


class SiteSerializer(serializers.ModelSerializer):
    # Pour afficher le nom du propriétaire au lieu de juste l'ID (optionnel, pratique pour le frontend)
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Site
        fields = ['id', 'name', 'domain_url', 'theme_config', 'created_at', 'owner', 'owner_username']
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
        fields = ['id', 'title', 'category', 'content_text', 'media_assets', 'likes', 'created_at', 'page']
        read_only_fields = ['created_at', 'likes']

class SiteUserSerializer(serializers.ModelSerializer):
    password_hash = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = SiteUser
        fields = ['id', 'username', 'email', 'password_hash', 'avatar_url', 'privilege', 'created_at', 'site']
        read_only_fields = ['created_at']

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'media_url', 'is_approved', 'created_at', 'publication', 'author', 'author_username']
        read_only_fields = ['created_at', 'is_approved'] 
        