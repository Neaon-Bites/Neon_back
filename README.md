# Neon_back
## documentation api
Documentation de l'API CMS

Cette documentation détaille les endpoints disponibles, le format des requêtes attendues et des exemples de réponses JSON pour chaque ressource de l'API.

URL de base (locale) : http://localhost:8000/api/

1. Super Admins (/super-admins/)

Rôle : Gestion des administrateurs globaux de la plateforme.

Endpoints

GET /super-admins/ : Liste tous les super admins.

POST /super-admins/ : Créer un super admin.

GET /super-admins/{id}/ : Détails d'un admin.

PUT /super-admins/{id}/ : Mise à jour complète.

PATCH /super-admins/{id}/ : Mise à jour partielle.

DELETE /super-admins/{id}/ : Supprimer un admin.

Exemple de Création (POST)

Corps de la requête (JSON) :

{
    "username": "admin_master",
    "email": "admin@cms.com",
    "password": "securePassword123" 
}


(Note : Le champ password est utilisé pour générer password_hash mais n'est jamais retourné).

Exemple de Réponse (GET / JSON)

{
    "id": 1,
    "username": "admin_master",
    "email": "admin@cms.com",
    "created_at": "2023-10-27T10:00:00Z"
}


2. Influenceurs (/influencers/)

Rôle : Gestion des clients créateurs de contenu.

Endpoints standards (CRUD)

GET /influencers/

POST /influencers/

... (idem standard)

Exemple de Création (POST)

Corps de la requête (JSON) :

{
    "username": "travel_blogger",
    "email": "contact@travel.com",
    "password": "pass",
    "bio": "Explorateur du monde",
    "profile_picture": "[http://img.url/avatar.jpg](http://img.url/avatar.jpg)"
}


Exemple de Réponse (GET / JSON)

{
    "id": 5,
    "username": "travel_blogger",
    "email": "contact@travel.com",
    "bio": "Explorateur du monde",
    "profile_picture": "[http://img.url/avatar.jpg](http://img.url/avatar.jpg)",
    "created_at": "2023-10-27T11:30:00Z",
    "sites": [1, 4] 
}


3. Sites (/sites/)

Rôle : Gestion des sites web créés par les influenceurs.

Endpoints standards (CRUD)

GET /sites/

POST /sites/

...

Exemple de Création (POST)

Corps de la requête (JSON) :

{
    "name": "Mon Blog Voyage",
    "domain_url": "voyage.moncms.com",
    "theme_config": {"color": "blue", "layout": "grid"},
    "owner": 5
}


Exemple de Réponse (GET / JSON)

{
    "id": 10,
    "name": "Mon Blog Voyage",
    "domain_url": "voyage.moncms.com",
    "theme_config": {
        "color": "blue",
        "layout": "grid"
    },
    "created_at": "2023-10-28T09:15:00Z",
    "owner": 5,
    "owner_username": "travel_blogger"
}


4. Pages (/pages/)

Rôle : Gestion des pages individuelles rattachées à un site.

Endpoints standards (CRUD)

GET /pages/

POST /pages/

...

Exemple de Création (POST)

Corps de la requête (JSON) :

{
    "title": "Mes Destinations",
    "slug": "mes-destinations",
    "is_published": true,
    "site": 10
}


Exemple de Réponse (GET / JSON)

{
    "id": 42,
    "title": "Mes Destinations",
    "slug": "mes-destinations",
    "is_published": true,
    "site": 10
}


5. Publications (/publications/)

Rôle : Gestion des articles/posts dans une page.

Endpoints

CRUD Standard (/publications/, /publications/{id}/)

Action Spéciale : POST /publications/{id}/like/

Exemple de Création (POST)

Corps de la requête (JSON) :

{
    "title": "Voyage au Japon",
    "category": "Asie",
    "content_text": "C'était magnifique...",
    "media_assets": {"cover": "img.jpg"},
    "page": 42
}


Exemple de Réponse (GET / JSON)

{
    "id": 101,
    "title": "Voyage au Japon",
    "category": "Asie",
    "content_text": "C'était magnifique...",
    "media_assets": {"cover": "img.jpg"},
    "likes": 0,
    "created_at": "2023-10-29T14:00:00Z",
    "page": 42
}


Action : Liker une publication

Requête : POST /publications/101/like/

Corps : (Vide)
Réponse :

{
    "status": "liked",
    "likes_count": 1
}


6. Utilisateurs du Site / Fans (/site-users/)

Rôle : Gestion des utilisateurs finaux inscrits sur un site spécifique.

Endpoints standards (CRUD)

GET /site-users/

POST /site-users/

...

Exemple de Création (POST)

Corps de la requête (JSON) :

{
    "username": "fan_numero_1",
    "email": "fan@gmail.com",
    "password": "fanpassword",
    "privilege": "premium",
    "site": 10
}


Exemple de Réponse (GET / JSON)

{
    "id": 500,
    "username": "fan_numero_1",
    "email": "fan@gmail.com",
    "avatar_url": null,
    "privilege": "premium",
    "site": 10,
    "site_name": "Mon Blog Voyage",
    "created_at": "2023-11-01T10:00:00Z"
}


7. Commentaires (/comments/)

Rôle : Gestion des commentaires des utilisateurs sur les publications.

Endpoints standards (CRUD)

GET /comments/

POST /comments/

...

Exemple de Création (POST)

Corps de la requête (JSON) :

{
    "content": "Super article !",
    "publication": 101,
    "author": 500
}


Exemple de Réponse (GET / JSON)

{
    "id": 88,
    "content": "Super article !",
    "media_url": null,
    "is_approved": true,
    "created_at": "2023-11-01T10:05:00Z",
    "publication": 101,
    "author": 500
}
