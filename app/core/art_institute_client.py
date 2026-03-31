import httpx

from config import settings


class ArtInstituteClient:

    def __init__(self):
        self.base_url = settings.ART_INSTITUTE_API_URL
        self.client = httpx.Client(timeout=10.0)

    def search_artworks(self, query: str, limit: int = 10) -> dict:
        url = f"{self.base_url}/artworks/search"
        params = {
            "q": query,
            "limit": limit,
            "fields": "id,title,artist_display,place_of_origin,date_display,medium_display"
        }

        response = self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_artwork(self, artwork_id: int) -> dict | None:
        url = f"{self.base_url}/artworks/{artwork_id}"
        params = {
            "fields": "id,title,artist_display,place_of_origin,date_display,medium_display"
        }

        try:
            response = self.client.get(url, params=params)
            response.raise_for_status()
            return response.json().get("data")
        except httpx.HTTPStatusError:
            return None

    def validate_artwork_exists(self, artwork_id: int) -> bool:
        return self.get_artwork(artwork_id) is not None

    def close(self):
        self.client.close()


art_client = ArtInstituteClient()