import config
from aiohttp import ClientSession
import logging

logger = logging.getLogger(__name__)

class Ad:
    
    @staticmethod
    async def get_ads():
        async with ClientSession() as session:
            async with session.get(config.API_BASE_URL + config.API_ENDPOINTS['get_ads']) as response:
                logger.info(f'GET {config.API_BASE_URL + config.API_ENDPOINTS["get_ads"]}')
                logger.info(f'Response status: {response.status}')
                if response.status == 404 or response.status == 500:
                    return None
                logger.info(f'Response body: {await response.text()}')
                return await response.json()
            
    @staticmethod
    async def get_ad(id):
        async with ClientSession() as session:
            async with session.get(config.API_BASE_URL + config.API_ENDPOINTS['get_ads'] +  str(id) + '/') as response:
                logger.info(f'GET {config.API_BASE_URL + config.API_ENDPOINTS["get_ads"]}')
                logger.info(f'Response status: {response.status}')
                if response.status == 404 or response.status == 500:
                    return None
                logger.info(f'Response body: {await response.text()}')
                return await response.json()
            
    @staticmethod
    async def post_ad(data):
        async with ClientSession() as session:
            async with session.post(config.API_BASE_URL + config.API_ENDPOINTS['get_ads'], json=data) as response:
                logger.info(f'POST {config.API_BASE_URL + config.API_ENDPOINTS["get_ads"]}')
                logger.info(f'Response status: {response.status}')
                if response.status == 404 or response.status == 500:
                    return None
                logger.info(f'Response body: {await response.text()}')
                return await response.json()

    @staticmethod            
    async def put_ad(id, data):
        async with ClientSession() as session:
            async with session.put(config.API_BASE_URL + config.API_ENDPOINTS['get_ads'] + str(id) + '/', json=data) as response:
                logger.info(f'PUT {config.API_BASE_URL + config.API_ENDPOINTS["get_ads"]}')
                logger.info(f'Response status: {response.status}')
                if response.status == 404 or response.status == 500:
                    return None
                logger.info(f'Response body: {await response.text()}')
                return await response.json()
            
    @staticmethod
    async def delete_ad(id):
        async with ClientSession() as session:
            async with session.delete(config.API_BASE_URL + config.API_ENDPOINTS['get_ads'] + str(id) + '/') as response:
                logger.info(f'DELETE {config.API_BASE_URL + config.API_ENDPOINTS["get_ads"]}')
                logger.info(f'Response status: {response.status}')
                if response.status == 404 or response.status == 500:
                    return None
                logger.info(f'Response body: {await response.text()}')
                return await response.json()
