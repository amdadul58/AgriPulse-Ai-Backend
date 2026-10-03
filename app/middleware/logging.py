from fastapi import Request
import time
import logging
logger = logging.getLogger(__name__)
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    logger.info(f'{request.method} {request.url.path} - {response.status_code} - {time.time()-start:.2f}s')
    return response
