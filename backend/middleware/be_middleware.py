# import time
# from fastapi import Request

# from backend.logging.config import logger


# async def log_requests(request: Request, call_next):

#     start_time = time.perf_counter()

#     response = await call_next(request)

#     duration_ms = round(
#         (time.perf_counter() - start_time) * 1000,
#         2,
#     )

#     logger.info(
#         "Request completed",
#         extra={
#             "method": request.method,
#             "path": request.url.path,
#             "status_code": response.status_code,
#             "duration_ms": duration_ms,
#         },
#     )

#     return response