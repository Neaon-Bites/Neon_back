from rest_framework import viewsets
from .models import SuperAdmin, Influencer, Site, Page, Publication, SiteUser, Comment
from .serializers import (
    SuperAdminSerializer, InfluencerSerializer, SiteSerializer, 
    PageSerializer, PublicationSerializer, SiteUserSerializer, CommentSerializer
)

class SuperAdminViewSet(viewsets.ModelViewSet):
    """
    CRUD complet pour les Super Admins.
    """
    queryset = SuperAdmin.objects.all().order_by('-created_at')
    serializer_class = SuperAdminSerializer
    filterset_fields = ['username', 'email', 'created_at', 'id']
    


class InfluencerViewSet(viewsets.ModelViewSet):
    """
    CRUD complet pour les Influenceurs.
    """
    queryset = Influencer.objects.all().order_by('-created_at')
    serializer_class = InfluencerSerializer
    filterset_fields = ['username', 'email', 'created_at', 'id']

class SiteViewSet(viewsets.ModelViewSet):
    """
    CRUD complet pour les Sites.
    """
    queryset = Site.objects.all().order_by('-created_at')
    serializer_class = SiteSerializer
    filterset_fields = ['owner', 'name', 'domain_url', 'created_at', 'id']

class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    
    filterset_fields = ['site', 'title', 'slug', 'created_at', 'id']


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    filterset_fields = ['page', 'created_at' , 'category' , 'title' , 'id']

class SiteUserViewSet(viewsets.ModelViewSet):
    queryset = SiteUser.objects.all()
    serializer_class = SiteUserSerializer
    filterset_fields =  ['site', 'username', 'email', 'created_at']
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    filterset_fields = ['site' , 'author', 'publication' , 'is_approved' , 'created_at']