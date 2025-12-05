import os
import shutil
import zipfile
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F
from .models import SuperAdmin, Influencer, Site, Page, Publication, SiteUser, Comment
from .serializers import (
    SuperAdminSerializer, InfluencerSerializer, SiteSerializer, 
    PageSerializer, PublicationSerializer, SiteUserSerializer, CommentSerializer
)
try:
    from .utils import StaticSiteGenerator
except Exception:
    # Fall back to absolute import to satisfy some editors/linters that
    # cannot resolve the relative import; keep the relative import for runtime.
    from core.utils import StaticSiteGenerator

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
    filterset_fields = ['owner', 'name', 'domain_url', 'created_at', 'privilege', 'id']

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


# ==========================================
# NOUVELLES VUES POUR LA GESTION CONFIG JSON
# ==========================================

class BaseSiteView(views.APIView):
    """ Helper pour récupérer le site ciblé """
    def get_site(self, request):
        # STRATÉGIE: On regarde si site_id est dans les params, 
        # sinon on prend le premier site de la base (pour le test/démo)
        # Dans la réalité: on utiliserait request.user.sites.first()
        site_id = request.query_params.get('site_id') or request.data.get('site_id')
        
        if site_id:
            return get_object_or_404(Site, id=site_id)
        
        # Fallback pour démo: dernier site créé
        site = Site.objects.last()
        if not site:
            raise Exception("Aucun site trouvé. Créez un site d'abord.")
        return site

class SiteConfigView(BaseSiteView):
    """
    Gère GET et POST pour /cms/api/site-config/
    """
    def get(self, request):
        try:
            site = self.get_site(request)
            return Response({
                "id": site.id,
                "config": site.config,
                "published_at": site.published_at,
                "updated_at": site.updated_at
            })
        except Exception as e:
            return Response({"error": str(e)}, status=404)

    def post(self, request):
        try:
            site = self.get_site(request)
            new_config = request.data.get('config')
            
            if not new_config:
                return Response({"error": "Config manquante"}, status=400)

            # Mise à jour du JSON
            site.config = new_config
            site.save() # updated_at se met à jour auto

            return Response({
                "id": site.id,
                "config": site.config,
                "published_at": site.published_at,
                "updated_at": site.updated_at
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class SitePublishView(BaseSiteView):
    """
    Gère POST /cms/api/publish/
    Génère les fichiers physiques et met à jour published_at
    """
    def post(self, request):
        try:
            site = self.get_site(request)
            
            # 1. Appel au générateur (utils.py)
            generator = StaticSiteGenerator(site)
            result = generator.generate()

            # 2. Update DB
            site.published_at = timezone.now()
            site.save()

            return Response({
                "status": "published",
                "url": result['public_url'],
                "files": {
                    "html": result['html'],
                    "css": result['css'],
                    "js": result['js']
                },
                "published_at": site.published_at
            })
            
        except Exception as e:
            return Response({"error": f"Erreur de publication: {str(e)}"}, status=500)

class SiteExportView(BaseSiteView):
    """
    Gère GET /cms/api/export/
    Zippe le dossier généré et renvoie le fichier
    """
    def get(self, request):
        try:
            site = self.get_site(request)
            
            if not site.published_at:
                return Response({"error": "Site not published yet"}, status=400)
                
            generator = StaticSiteGenerator(site)
            source_dir = generator.output_dir
            
            # Création du ZIP en mémoire ou temp
            zip_filename = f"{site.name}_export"
            zip_path = os.path.join(settings.MEDIA_ROOT, 'temp', zip_filename)
            
            # S'assurer que le dossier temp existe
            os.makedirs(os.path.dirname(zip_path), exist_ok=True)
            
            shutil.make_archive(zip_path, 'zip', source_dir)
            
            # Servir le fichier
            zip_file = open(f"{zip_path}.zip", 'rb')
            return FileResponse(zip_file, as_attachment=True, filename=f"{zip_filename}.zip")

        except Exception as e:
            return Response({"error": str(e)}, status=500)