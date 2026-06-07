import datetime
import logging

from fastapi import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


async def add_header(request: Request, call_next) -> Response:
    dt_request = datetime.datetime.now().isoformat()
    logger.info(f'request received at {dt_request}')
    request.state.dt_request = dt_request

    response = await call_next(request)
    response.headers['X-Request-Time'] = dt_request
    return response
