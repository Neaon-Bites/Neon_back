from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SuperAdminViewSet, InfluencerViewSet, SiteViewSet, 
    PageViewSet, PublicationViewSet, SiteUserViewSet, CommentViewSet, SiteConfigView, SitePublishView, SiteExportView
)

router = DefaultRouter()
router.register(r'super-admins', SuperAdminViewSet)
router.register(r'influencers', InfluencerViewSet)
router.register(r'sites', SiteViewSet)
router.register(r'pages', PageViewSet)
router.register(r'publications', PublicationViewSet)
router.register(r'site-users', SiteUserViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
 # Endpoints spécifiques pour le CMS Frontend
    path('cms/api/site-config/', SiteConfigView.as_view(), name='site-config'),
    path('cms/api/publish/', SitePublishView.as_view(), name='site-publish'),
    path('cms/api/export/', SiteExportView.as_view(), name='site-export'),
]