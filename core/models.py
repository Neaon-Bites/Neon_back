from django.db import models

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime, JSON, Table, Boolean, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Configuration de la base de données SQLite
DATABASE_URL = "sqlite:///cms_influenceurs.db"
engine = create_engine(DATABASE_URL, echo=False) # echo=True pour voir les requêtes SQL
Base = declarative_base()

# --- MODÈLES (CLASSES) ---

class SuperAdmin(Base):
    """
    Administrateur global du CMS.
    A des droits sur tout le système.
    """
    __tablename__ = 'super_admins'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Le SuperAdmin n'a pas forcément de relations directes en FK, 
    # mais il a accès à tout via la logique applicative.

class Influencer(Base):
    """
    L'utilisateur créateur de contenu (Client du CMS).
    Il possède un ou plusieurs sites.
    """
    __tablename__ = 'influencers'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    bio = Column(Text, nullable=True)
    profile_picture = Column(String(255), nullable=True) # Photo de profil (PP)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relation: Un influenceur peut créer plusieurs sites (One-to-Many)
    sites = relationship("Site", back_populates="owner", cascade="all, delete-orphan")

class Site(Base):
    """
    Le site web créé par l'influenceur.
    """
    __tablename__ = 'sites'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    domain_url = Column(String(200), unique=True) # ex: mon-site.cms.com
    theme_config = Column(JSON, nullable=True) # Stocke les couleurs, polices en JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Clé étrangère vers l'influenceur
    owner_id = Column(Integer, ForeignKey('influencers.id'), nullable=False)

    # Relations
    owner = relationship("Influencer", back_populates="sites")
    pages = relationship("Page", back_populates="site", cascade="all, delete-orphan")
    
    # Relation One-to-Many : Un site a plusieurs utilisateurs inscrits spécifiquement
    members = relationship("SiteUser", back_populates="site", cascade="all, delete-orphan")

class Page(Base):
    """
    Une page appartenant à un site (ex: Accueil, Blog, Contact).
    """
    __tablename__ = 'pages'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False) # pour l'URL (ex: /ma-page)
    is_published = Column(Boolean, default=True)
    
    site_id = Column(Integer, ForeignKey('sites.id'), nullable=False)

    # Relations
    site = relationship("Site", back_populates="pages")
    publications = relationship("Publication", back_populates="page", cascade="all, delete-orphan")

class Publication(Base):
    """
    Un post/article contenu dans une page.
    Peut contenir texte, image, vidéo (stocké en JSON ou champs séparés).
    """
    __tablename__ = 'publications'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=True)
    category = Column(String(100), nullable=True) # Catégorie de la publication (ex: Lifestyle, Tech)
    content_text = Column(Text, nullable=True)
    
    # Stockage des liens médias (images, vidéos, sons) sous forme de liste JSON
    # Ex: {"type": "video", "url": "...", "format": "mp4"}
    media_assets = Column(JSON, nullable=True) 
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    page_id = Column(Integer, ForeignKey('pages.id'), nullable=False)

    # Relations
    page = relationship("Page", back_populates="publications")
    comments = relationship("Comment", back_populates="publication", cascade="all, delete-orphan")

class SiteUser(Base):
    """
    L'utilisateur final (le fan/visiteur).
    Il crée un compte spécifique pour UN seul site.
    """
    __tablename__ = 'site_users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    # L'email n'est plus unique globalement, car le même email peut être utilisé sur deux sites différents
    email = Column(String(100), nullable=False) 
    password_hash = Column(String(128), nullable=True) # Nullable si login social
    avatar_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Clé étrangère vers le Site spécifique
    site_id = Column(Integer, ForeignKey('sites.id'), nullable=False)

    # Relations
    comments = relationship("Comment", back_populates="author")
    site = relationship("Site", back_populates="members")

    # Contrainte d'unicité composite : Un email doit être unique au sein d'un même site
    __table_args__ = (
        UniqueConstraint('email', 'site_id', name='uq_site_user_email'),
    )

class Comment(Base):
    """
    Un commentaire laissé par un SiteUser sur une Publication.
    """
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    media_url = Column(String(255), nullable=True) # Possibilité de mettre une image/gif
    created_at = Column(DateTime, default=datetime.utcnow)
    is_approved = Column(Boolean, default=True) # Pour la modération

    publication_id = Column(Integer, ForeignKey('publications.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('site_users.id'), nullable=False)

    # Relations
    publication = relationship("Publication", back_populates="comments")
    author = relationship("SiteUser", back_populates="comments")

# --- CRÉATION DE LA BD ---
def init_db():
    print("Création des tables dans la base de données SQLite...")
    Base.metadata.create_all(engine)
    print("Tables créées avec succès !")

if __name__ == "__main__":
    init_db()
