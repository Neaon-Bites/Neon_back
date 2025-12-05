from django.db import models
from django.utils import timezone


class SuperAdmin(models.Model):
    """
    Administrateur global du CMS.
    """
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'super_admins'
        verbose_name = 'Super Admin'
        verbose_name_plural = 'Super Admins'

    def __str__(self):
        return self.username


class Influencer(models.Model):
    """
    L'utilisateur créateur de contenu (Client du CMS).
    """
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=128)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'influencers'
        verbose_name = 'Influenceur'

    def __str__(self):
        return self.username


class Site(models.Model):
    """
    Le site web créé par l'influenceur.
    """
    name = models.CharField(max_length=100)
    domain_url = models.CharField(max_length=200, unique=True)
    
    theme_config = models.JSONField(blank=True, null=True) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    owner = models.ForeignKey(
        Influencer, 
        on_delete=models.CASCADE, 
        related_name="sites" # Correspond au back_populates="sites"
    )

    class Meta:
        db_table = 'sites'

    def __str__(self):
        return self.name


class Page(models.Model):
    """
    Une page appartenant à un site.
    """
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    is_published = models.BooleanField(default=True)
    
    site = models.ForeignKey(
        Site, 
        on_delete=models.CASCADE, 
        related_name="pages"
    )

    class Meta:
        db_table = 'pages'
        unique_together = ('site', 'slug')

    def __str__(self):
        return f"{self.title} ({self.site.name})"


class Publication(models.Model):
    """
    Un post/article contenu dans une page.
    """
    title = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    content_text = models.TextField(blank=True, null=True)
    
    media_assets = models.JSONField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    page = models.ForeignKey(
        Page, 
        on_delete=models.CASCADE, 
        related_name="publications"
    )

    class Meta:
        db_table = 'publications'

    def __str__(self):
        return self.title if self.title else f"Publication {self.id}"


class SiteUser(models.Model):
    """
    L'utilisateur final (le fan/visiteur).
    """
    # Définition des choix pour le privilège
    class Privilege(models.TextChoices):
        STANDARD = 'standard', 'Standard'
        PREMIUM = 'premium', 'Premium'

    username = models.CharField(max_length=50)
    email = models.CharField(max_length=100) 
    password_hash = models.CharField(max_length=128, blank=True, null=True)
    avatar_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

 # Nouvel attribut privilège avec valeur par défaut
    privilege = models.CharField(
        max_length=10,
        choices=Privilege.choices,
        default=Privilege.STANDARD
    )

    site = models.ForeignKey(
        Site, 
        on_delete=models.CASCADE, 
        related_name="members"
    )

    class Meta:
        db_table = 'site_users'
        constraints = [
            models.UniqueConstraint(fields=['email', 'site'], name='uq_site_user_email')
        ]

    def __str__(self):
        return f"{self.username} on {self.site.name}"


class Comment(models.Model):
    """
    Un commentaire laissé par un SiteUser sur une Publication.
    """
    content = models.TextField()
    media_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    publication = models.ForeignKey(
        Publication, 
        on_delete=models.CASCADE, 
        related_name="comments"
    )
    author = models.ForeignKey(
        SiteUser, 
        on_delete=models.CASCADE, 
        related_name="comments"
    )

    class Meta:
        db_table = 'comments'

    def __str__(self):
        return f"Comment {self.id} by {self.author.username}"