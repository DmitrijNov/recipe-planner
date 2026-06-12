from fastapi import Request


async def custom_middleware(request: Request, call_next):
    # for future use
    response = await call_next(request)
    return response
