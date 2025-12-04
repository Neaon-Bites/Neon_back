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


class InfluencerViewSet(viewsets.ModelViewSet):
    """
    CRUD complet pour les Influenceurs.
    """
    queryset = Influencer.objects.all().order_by('-created_at')
    serializer_class = InfluencerSerializer


class SiteViewSet(viewsets.ModelViewSet):
    """
    CRUD complet pour les Sites.
    """
    queryset = Site.objects.all().order_by('-created_at')
    serializer_class = SiteSerializer

class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer

class SiteUserViewSet(viewsets.ModelViewSet):
    queryset = SiteUser.objects.all()
    serializer_class = SiteUserSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer