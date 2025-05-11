# backend/main.py

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

# Internal routers
from routes import (
    auth,
    products,
    orders,
    subscription,
    analytics,
    api_routes,
    mpesa,
    airtel,
    graphql,
    billing,       # ✅ New import
    farm_records
)
from utils.security import get_current_user

app = FastAPI(
    title="AgroConnect Platform",
    description="A scalable digital platform for farmers, customers, and government analytics.",
    version="1.0.0"
)

# CORS setup - adjust origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"], dependencies=[Depends(get_current_user)])
app.include_router(subscription.router, prefix="/subscription", tags=["Subscriptions"], dependencies=[Depends(get_current_user)])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(api_routes.router, prefix="/api", tags=["External Services"])
app.include_router(mpesa.router, prefix="/mpesa", tags=["M-Pesa"], dependencies=[Depends(get_current_user)])
app.include_router(airtel.router, prefix="/airtel", tags=["Airtel"], dependencies=[Depends(get_current_user)])
app.include_router(graphql.router)
app.include_router(billing.router, prefix="/billing", tags=["Billing"], dependencies=[Depends(get_current_user)])  # ✅ Added
app.include_router(farm_records.router, prefix="/api/farm", tags=["Farm Records"], dependencies=[Depends(get_current_user)])
