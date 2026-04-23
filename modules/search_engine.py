import requests
import logging
from urllib.parse import quote

logger = logging.getLogger(__name__)

class NaverPlaceSearchEngine:
    def __init__(self):
        import os
        self.client_id = os.environ.get('NAVER_CLIENT_ID')
        self.client_secret = os.environ.get('NAVER_CLIENT_SECRET')
        self.base_url = "https://openapi.naver.com/v1/search/local.json"

    def search_place_rank(self, keyword, place_name):
        try:
            headers = {
                "X-Naver-Client-Id": self.client_id,
                "X-Naver-Client-Secret": self.client_secret
            }
            params = {
                "query": keyword,
                "display": 100,
                "start": 1,
                "sort": "random"
            }
            response = requests.get(
                self.base_url,
                headers=headers,
                params=params
            )
            if response.status_code != 200:
                logger.error(f"API 오류: {response.status_code}")
                return None

            items = response.json().get('items', [])
            for i, item in enumerate(items):
                title = item.get('title', '').replace('<b>', '').replace('</b>', '')
                if place_name in title:
                    return {
                        'rank': i + 1,
                        'title': title,
                        'address': item.get('address', ''),
                        'category': item.get('category', ''),
                        'telephone': item.get('telephone', ''),
                        'total': len(items)
                    }
            return {'rank': -1, 'total': len(items)}

        except Exception as e:
            logger.error(f"검색 오류: {e}")
            return None
