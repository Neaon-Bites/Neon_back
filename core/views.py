import os
import shutil
import zipfile
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, views
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
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


# --- NOUVELLES VUES (CMS & Génération) ---

class BaseSiteView(views.APIView):
    """Helper pour récupérer le site ciblé (Pour démo: prend le dernier créé si pas d'ID)"""
    def get_site(self, request):
        # 1. Chercher d'abord dans l'URL (plus sûr, ne déclenche pas le parsing JSON)
        site_id = request.query_params.get('site_id')
        
        # 2. Si non trouvé, essayer de lire le body JSON
        if not site_id:
            try:
                # Vérifie si data existe pour éviter JSON parse error sur body vide
                if request.data:
                    site_id = request.data.get('site_id')
            except ParseError:
                # Si le body est mal formé, on ignore et on continue (fallback sur dernier site)
                pass
        
        if site_id:
            return get_object_or_404(Site, id=site_id)
        
        # Fallback Demo: Dernier site créé
        site = Site.objects.last()
        if not site:
            # On lève une exception spécifique pour être catchée plus haut
            raise ValueError("Aucun site trouvé en base de données. Veuillez créer un site via l'admin ou l'API.")
        return site

class SiteConfigView(BaseSiteView):
    """
    GET: Récupère la config JSON du site.
    POST: Met à jour la config JSON (Sauvegarde brouillon).
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
        except ValueError as e:
             return Response({"error": str(e)}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def post(self, request):
        try:
            # Sécurité : Vérifier si le body est vide avant tout
            if not request.data:
                 return Response({"error": "Le corps de la requête (JSON) est vide."}, status=400)

            site = self.get_site(request)
            
            # On accepte soit "config" directement, soit tout le body
            new_config = request.data.get('config', request.data)
            
            site.config = new_config
            site.save()

            return Response({
                "id": site.id,
                "config": site.config,
                "updated_at": site.updated_at
            })
        except ParseError:
             return Response({"error": "JSON invalide envoyé."}, status=400)
        except Exception as e:
            return Response({"error": f"Erreur update: {str(e)}"}, status=500)

class SitePublishView(BaseSiteView):
    """
    POST: Génère les fichiers HTML/CSS/JS physiques.
    """
    def post(self, request):
        try:
            site = self.get_site(request)
            generator = StaticSiteGenerator(site)
            result = generator.generate()

            site.published_at = timezone.now()
            site.save()

            return Response({
                "status": "published",
                "url": result['public_url'],
                "files": result
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class SiteExportView(BaseSiteView):
    """
    GET: Télécharge le site sous format ZIP.
    """
    def get(self, request):
        try:
            site = self.get_site(request)
            if not site.published_at:
                return Response({"error": "Site non publié. Publiez-le d'abord."}, status=400)
                
            generator = StaticSiteGenerator(site)
            
            # Création du ZIP
            zip_filename = f"{site.name}_export"
            zip_path = os.path.join(settings.MEDIA_ROOT, 'temp', zip_filename)
            os.makedirs(os.path.dirname(zip_path), exist_ok=True)
            
            shutil.make_archive(zip_path, 'zip', generator.output_dir)
            
            zip_file = open(f"{zip_path}.zip", 'rb')
            return FileResponse(zip_file, as_attachment=True, filename=f"{zip_filename}.zip")

        except Exception as e:
            return Response({"error": str(e)}, status=500)