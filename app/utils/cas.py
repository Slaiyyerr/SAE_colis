"""Client CAS pour l'authentification universitaire.

CAS (Central Authentication Service) est le systeme SSO de l'universite.
Ce module gere :
- La generation des URLs de login/logout
- La validation des tickets CAS
- Le parsing de la reponse XML du CAS

Flux CAS :
1. Redirection vers CAS avec URL de callback
2. L'utilisateur s'authentifie sur le CAS
3. CAS redirige vers notre callback avec un ticket
4. On valide le ticket aupres du CAS
5. Le CAS renvoie les infos de l'utilisateur (email, etc.)
"""

import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlencode


class CASClient:
    """Client pour communiquer avec le serveur CAS."""
    
    def __init__(self):
        self.server_url = None  # URL du serveur CAS
        self.service_url = None  # URL de callback de notre app
    
    def init_app(self, app):
        """Initialise les URLs depuis la config Flask."""
        self.server_url = app.config.get('CAS_SERVER', 'https://cas.univ-paris13.fr/cas')
        self.service_url = app.config.get('APP_URL', 'http://localhost:5000') + '/auth/cas/callback'
    
    @property
    def login_url(self):
        """URL de connexion CAS (avec notre service en parametre)."""
        return f"{self.server_url}/login?{urlencode({'service': self.service_url})}"
    
    @property
    def logout_url(self):
        """URL de deconnexion CAS."""
        return f"{self.server_url}/logout?{urlencode({'service': self.service_url.replace('/auth/cas/callback', '')})}"
    
    def validate_ticket(self, ticket):
        """Valide un ticket CAS aupres du serveur.
        
        Args:
            ticket: Le ticket recu dans l'URL de callback (ST-xxxxx)
        
        Returns:
            dict avec 'username' et 'attributes', ou None si invalide
        """
        try:
            # Appel au endpoint de validation du CAS
            response = requests.get(
                f"{self.server_url}/serviceValidate",
                params={'service': self.service_url, 'ticket': ticket},
                timeout=10
            )
            response.raise_for_status()
        except requests.RequestException:
            return None
        
        return self._parse_response(response.text)
    
    def _parse_response(self, xml_response):
        """Parse la reponse XML du CAS.
        
        Exemple de reponse CAS reussie :
        <cas:serviceResponse>
          <cas:authenticationSuccess>
            <cas:user>jdupont</cas:user>
            <cas:attributes>
              <cas:mail>jean.dupont@univ-paris13.fr</cas:mail>
            </cas:attributes>
          </cas:authenticationSuccess>
        </cas:serviceResponse>
        """
        try:
            ns = {'cas': 'http://www.yale.edu/tp/cas'}  # Namespace CAS
            root = ET.fromstring(xml_response)
            
            # Chercher le bloc authenticationSuccess
            success = root.find('.//cas:authenticationSuccess', ns)
            if success is None:
                return None
            
            # Extraire le username
            user_elem = success.find('cas:user', ns)
            if user_elem is None:
                return None
            
            # Extraire les attributs (mail, displayName, etc.)
            attributes = {}
            attrs_elem = success.find('cas:attributes', ns)
            if attrs_elem is not None:
                for attr in attrs_elem:
                    tag = attr.tag.replace('{http://www.yale.edu/tp/cas}', '')
                    attributes[tag] = attr.text
            
            return {'username': user_elem.text, 'attributes': attributes}
        except ET.ParseError:
            return None


# Instance globale utilisee par AuthController
cas_client = CASClient()
