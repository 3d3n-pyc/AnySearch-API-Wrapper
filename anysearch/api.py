from .utils import Utils
from .data import INFO, PatchNote, Server, KeyTier, KeyStatus
from datetime import datetime
import requests


class API(object):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.base_url = "http://154.51.39.143:19180/"

    def __repr__(self) -> str:
        return f"<API key={self.api_key[:4]}...>"
    
    def __str__(self) -> str:
        return f"<API key={self.api_key[:4]}...>"
    
    def _time_to_timestamp(self, time: str) -> int:
        return int(datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ').timestamp())
    
    def key_status(self) -> KeyStatus:
        """Obtenir le statut de la clé

        Returns:
            KeyStatus: Statut de la clé
        """        
        url: str = Utils.combine_url_with_endpoint(self.base_url, "api/key")
        response = requests.get(url, params={"key": self.api_key})
        if response.status_code == 200:
            data = response.json()
            tier: dict = data['tier']
            return KeyStatus(KeyTier(*tier.values()), self._time_to_timestamp(data['expires']) if data['expires'] else None)
        if response.status_code == 404:
            data = response.json()
            tier: dict = data['tier']
            return KeyStatus(KeyTier(*tier.values()), None)
        return None

    def info(self) -> INFO:
        """Obtenir les informations du serveur

        Returns:
            INFO: Informations du serveur
        """
        url: str = Utils.combine_url_with_endpoint(self.base_url, "info")
        response = requests.get(url)
        if response.status_code == 200:
            data: dict = response.json()['data']
            return INFO(*data.values())
        return None
    
    def patchnotes(self) -> list[PatchNote]:
        """Obtenir les notes de patch

        Returns:
            list[PatchNote]: Liste des notes de patch
        """
        url: str = Utils.combine_url_with_endpoint(self.base_url, "patchnotes")
        response = requests.get(url)
        if response.status_code == 200:
            data: list[dict] = response.json()['data']
            return [PatchNote(*patchnote.values()) for patchnote in data]
        return None
    
    def search(self, name: str) -> list[Server]:
        """Rechercher un utilisateur par nom

        Args:
            name (str): Nom de l'utilisateur à rechercher

        Returns:
            list[Server]: Liste des IPs liées à l'utilisateur
        """
        url: str = Utils.combine_url_with_endpoint(self.base_url, "api/name")
        response = requests.get(url, params={"value": name, "key": self.api_key})
        if response.status_code == 200:
            data: dict = response.json()['data']
            return [Server(server, data[server]) for server in data.keys() if len(data[server]) > 0]
        if response.status_code == 404:
            return []
        return None
    
    def lookup(self, ip: str) -> list[Server]:
        """Obtenir les utilisateurs liés à une adresse IP

        Args:
            ip (str): Adresse IP à rechercher

        Returns:
            list[Server]: Liste des utilisateurs liés à l'adresse IP
        """
        url: str = Utils.combine_url_with_endpoint(self.base_url, "api/ip")
        response = requests.get(url, params={"value": ip, "key": self.api_key})
        if response.status_code == 200:
            data: dict = response.json()['data']
            return [Server(server, data[server]) for server in data.keys() if len(data[server]) > 0]
        if response.status_code == 404:
            return []
        return None