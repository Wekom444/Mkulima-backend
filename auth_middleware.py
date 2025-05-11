# backend/middleware/auth_middleware.py

from fastapi import Request, HTTPException
from fastapi.routing import APIRoute

class AuthenticatedRoute(APIRoute):
    def get_route_handler(self):
        original = super().get_route_handler()
        async def custom_handler(request: Request):
            token = request.headers.get("Authorization")
            if not token or token != f"Bearer {os.getenv('API_TOKEN')}":
                raise HTTPException(401, "Unauthorized")
            return await original(request)
        return custom_handler
