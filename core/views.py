from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F
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

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            influencer = Influencer.objects.get(email=email)
            
            if influencer.password_hash == password:
                return Response({
                    "status": "success",
                    "message": "Connexion réussie",
                    "user": {
                        "id": influencer.id,
                        "username": influencer.username,
                        "email": influencer.email,
                        "profile_picture": influencer.profile_picture
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Mot de passe incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Influencer.DoesNotExist:
            return Response({"error": "Aucun compte trouvé avec cet email"}, status=status.HTTP_404_NOT_FOUND)

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

    @action(detail=True, methods=['post'], url_path='like')
    def like(self, request, pk=None):
        publication = self.get_object()
        publication.likes = F('likes') + 1
        publication.save()
        
        publication.refresh_from_db()
        
        return Response({
            "status": "liked",
            "likes_count": publication.likes
        }, status=status.HTTP_200_OK)

class SiteUserViewSet(viewsets.ModelViewSet):
    queryset = SiteUser.objects.all()
    serializer_class = SiteUserSerializer
    filterset_fields =  ['site', 'username', 'email', 'created_at']
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    filterset_fields = ['site' , 'author', 'publication' , 'is_approved' , 'created_at']