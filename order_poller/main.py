import asyncio
import httpx
import logging
from fastapi import FastAPI, BackgroundTasks
import os

app = FastAPI(title='Service_poller', version='1.0.0')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ORDER_SERVICE_URL = os.getenv('ORDER_SERVICE_URL', 'localhost:8001')
OZON_MP_SERVICE_URL = os.getenv('OZON_MP_SERVICE_URL', 'localhost:8002')
INVENTORY_SERVICE_URL = os.getenv('INVENTORY_SERVICE_URL', 'localhost:8003')


@app.post('/sync-all')
async def sync_all(bg_tasks: BackgroundTasks):
    """Sync all marketplaces"""
    bg_tasks.add_task(sync_all_marketplaces)
    return {'message': 'Full sync started'}


@app.post('/sync-ozon')
async def sync_ozon(bg_tasks: BackgroundTasks):
    """Sync only OZON"""
    bg_tasks.add_task(sync_ozon_orders)
    return {'message': 'OZON sync started'}


async def sync_all_marketplaces():
    """Sync all marketplaces"""
    tasks = [
        sync_ozon_orders
    ]

    await asyncio.gather(*tasks, return_exceptions=True)


async def sync_ozon_orders():
    """Sync OZON orders"""
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(f'{OZON_MP_SERVICE_URL}/sync-orders')
            if response.status_code == 200:
                logger.info('Vse ok')
            else:
                logger.info(f'Ne vse ok: {response.text}')
    except httpx.TimeoutException:
        logger.error(f'Sync Timeout')
    except httpx.RequestError as e:
        logger.error(f'RequestError: {e}')
    except Exception as e:
        logger.error(f'Не известная ошибка: {e}')


@app.get('/health')
async def health_check():
    return {'status': 'health', 'service': 'service-poller'}


@app.on_event('startup')
async def startup_event():
    """Start background tasks on startup"""
    asyncio.create_task(periodic_sync())


async def periodic_sync():
    while True:
        await asyncio.sleep(600)
        await sync_all_marketplaces()
