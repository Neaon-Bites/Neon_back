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