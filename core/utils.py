import os
import shutil
from django.conf import settings
from django.utils.text import slugify

class StaticSiteGenerator:
    """
    Classe utilitaire pour transformer la configuration JSON d'un site
    en fichiers HTML/CSS/JS réels.
    """
    def __init__(self, site_obj):
        self.site = site_obj
        self.config = site_obj.config
        # Utilise le nom du site pour créer un dossier unique (ex: "mon-super-site")
        self.site_slug = slugify(site_obj.name)
        
        # Chemin physique où les fichiers seront créés (ex: /media/generated_sites/mon-super-site/)
        self.output_dir = os.path.join(settings.MEDIA_ROOT, 'generated_sites', self.site_slug)
        
        # URL publique pour accéder aux fichiers (ex: http://localhost:8000/media/generated_sites/mon-super-site/)
        self.media_url_base = f"{settings.MEDIA_URL}generated_sites/{self.site_slug}/"

    def generate(self):
        """
        Méthode principale appelée par la vue.
        Orchestre la création de tout le site.
        """
        # 1. Créer ou vider le dossier de destination
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir)

        # 2. Générer les fichiers statiques globaux
        self._generate_css()
        self._generate_js()

        # 3. Générer chaque page HTML définie dans le JSON
        pages_config = self.config.get('pages', [])
        generated_files = []

        # Construction du menu de navigation (utilisé sur toutes les pages)
        nav_html = self._build_navbar(pages_config)

        for page in pages_config:
            # Détermine le nom du fichier (index.html pour l'accueil, sinon nom-page.html)
            filename = "index.html" if page.get('type') == 'home' else f"{slugify(page.get('name'))}.html"
            file_path = os.path.join(self.output_dir, filename)
            
            # Génère le contenu HTML complet de la page
            content_html = self._render_page_content(page, nav_html)
            
            # Écrit le fichier sur le disque
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content_html)
            
            generated_files.append(file_path)

        # Retourne les chemins pour la réponse API
        return {
            "html": os.path.join(self.output_dir, "index.html"),
            "css": os.path.join(self.output_dir, "style.css"),
            "js": os.path.join(self.output_dir, "main.js"),
            "public_url": f"{self.media_url_base}index.html"
        }

    def _generate_css(self):
        """Création du fichier style.css"""
        # Vous pouvez enrichir ce CSS avec les couleurs de la config (self.config.get('theme'))
        css_content = """
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; line-height: 1.6; color: #333; }
        .navbar { background: #222; color: #fff; padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; }
        .navbar a { color: #fff; text-decoration: none; margin-left: 1.5rem; font-weight: 500; }
        .navbar .brand { font-size: 1.2rem; font-weight: bold; display: flex; align-items: center; gap: 10px; }
        
        .hero { background-size: cover; background-position: center; color: white; padding: 6rem 2rem; text-align: center; background-color: #555; position: relative; }
        .hero::after { content: ''; position: absolute; top:0; left:0; right:0; bottom:0; background: rgba(0,0,0,0.4); z-index: 1; }
        .hero > * { position: relative; z-index: 2; }
        .hero h1 { font-size: 3rem; margin-bottom: 0.5rem; }
        
        .section { padding: 4rem 2rem; max-width: 1200px; margin: 0 auto; }
        .text-section { font-size: 1.1rem; }
        
        .product-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem; }
        .product-card { border: 1px solid #eee; border-radius: 8px; padding: 1rem; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05); transition: transform 0.2s; }
        .product-card:hover { transform: translateY(-5px); }
        .product-card img { max-width: 100%; height: 200px; object-fit: contain; margin-bottom: 1rem; }
        .product-card h3 { margin: 0.5rem 0; font-size: 1.2rem; }
        .product-price { color: #007bff; font-weight: bold; font-size: 1.1rem; }
        
        form { max-width: 600px; margin: 0 auto; }
        .form-group { margin-bottom: 1.5rem; }
        .form-group label { display: block; margin-bottom: 0.5rem; font-weight: 600; }
        .form-group input, .form-group textarea { width: 100%; padding: 0.8rem; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        button { background: #007bff; color: white; border: none; padding: 0.8rem 2rem; border-radius: 4px; cursor: pointer; font-size: 1rem; }
        button:hover { background: #0056b3; }
        """
        with open(os.path.join(self.output_dir, 'style.css'), 'w', encoding='utf-8') as f:
            f.write(css_content)

    def _generate_js(self):
        """Création du fichier main.js"""
        js_content = """
        console.log('Site généré chargé avec succès');
        
        document.addEventListener('DOMContentLoaded', () => {
            // Exemple d'interaction : gestionnaire simple de formulaire
            const forms = document.querySelectorAll('form');
            forms.forEach(form => {
                form.addEventListener('submit', (e) => {
                    e.preventDefault();
                    // Ici on pourrait faire un vrai appel API pour envoyer le message
                    alert('Merci ! Votre message a été simulé (Frontend statique).');
                    form.reset();
                });
            });
        });
        """
        with open(os.path.join(self.output_dir, 'main.js'), 'w', encoding='utf-8') as f:
            f.write(js_content)

    def _build_navbar(self, pages):
        """Génère le HTML de la barre de navigation"""
        links = ""
        for p in pages:
            # Lien vers le fichier HTML correct
            filename = "index.html" if p.get('type') == 'home' else f"{slugify(p.get('name'))}.html"
            links += f'<a href="{filename}">{p.get("name")}</a>'
        
        site_name = self.config.get('siteName', 'My Site')
        logo = self.config.get('logo')
        
        # Si un logo est présent (base64 ou url), on l'affiche
        logo_html = f'<img src="{logo}" height="30" style="border-radius:50%;" />' if logo else ''
        
        return f"""
        <nav class="navbar">
            <div class="brand">{logo_html} <span>{site_name}</span></div>
            <div class="links">{links}</div>
        </nav>
        """

    def _render_page_content(self, page_config, nav_html):
        """Assemble le HTML final d'une page"""
        
        # 1. Génération du contenu des sections
        sections_html = ""
        for section in page_config.get('sections', []):
            stype = section.get('type')
            content = section.get('content', {})
            
            if stype == 'hero':
                # Gestion image de fond
                bg_style = ""
                if content.get('bgImage'):
                    bg_style = f"background-image: url('{content.get('bgImage')}');"
                
                sections_html += f"""
                <section class="hero" style="{bg_style}">
                    <h1>{content.get('title')}</h1>
                    <p>{content.get('subtitle')}</p>
                </section>
                """
                
            elif stype == 'text':
                # Conversion des sauts de ligne en <br>
                text_content = content.get('text', '').replace('\n', '<br>')
                sections_html += f"""
                <section class="section text-section">
                    <p>{text_content}</p>
                </section>
                """
                
            elif stype == 'image':
                sections_html += f"""
                <section class="section" style="text-align:center;">
                    <img src="{content.get('src')}" style="max-width:100%; border-radius:8px;" />
                </section>
                """
                
            elif stype == 'products':
                products_list = ""
                for prod in content.get('products', []):
                    img = f'<img src="{prod.get("image")}" />' if prod.get("image") else ''
                    products_list += f"""
                    <div class="product-card">
                        {img}
                        <h3>{prod.get('title')}</h3>
                        <p class="product-price">{prod.get('price')}</p>
                        <p>{prod.get('description')}</p>
                    </div>
                    """
                sections_html += f"""
                <section class="section">
                    <h2 style="text-align:center; margin-bottom:2rem;">Nos Produits</h2>
                    <div class="product-grid">{products_list}</div>
                </section>
                """
            
            elif stype == 'form':
                sections_html += f"""
                <section class="section">
                    <form>
                        <h3 style="margin-bottom:1.5rem; text-align:center;">Contactez-nous</h3>
                        <div class="form-group">
                            <label>{content.get('emailLabel', 'Email')}</label>
                            <input type="email" required placeholder="exemple@email.com">
                        </div>
                        <div class="form-group">
                            <label>{content.get('messageLabel', 'Message')}</label>
                            <textarea rows="5" required></textarea>
                        </div>
                        <div style="text-align:center;">
                            <button type="submit">{content.get('buttonText', 'Envoyer')}</button>
                        </div>
                    </form>
                </section>
                """

        # 2. Gestion du Mode Crise (Maintenance)
        crisis = self.config.get('crisisMode', {})
        if crisis.get('enabled'):
            return f"""
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Maintenance - {self.config.get('siteName')}</title>
                <style>
                    body {{ font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: #f8f9fa; color: #333; }}
                    .container {{ text-align: center; padding: 2rem; background: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                    h1 {{ color: #e74c3c; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>⚠️ {crisis.get('title')}</h1>
                    <p>{crisis.get('message')}</p>
                </div>
            </body>
            </html>
            """

        # 3. Assemblage final de la page
        return f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{page_config.get('name')} - {self.config.get('siteName')}</title>
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
            {nav_html}
            {sections_html}
            <script src="main.js"></script>
        </body>
        </html>
        """