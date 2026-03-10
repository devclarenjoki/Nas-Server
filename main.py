from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import Config
import uvicorn
from multiprocessing import cpu_count

# Import your route modules (assuming they've been converted to FastAPI routers)
#from routes.auth_routes import router as auth_router
import routes.user_routes as user_routes
from routes.auth_routes import router as auth_router
from routes.settings_routes import router as settings_router
from routes.order_routes import router as order_router
from routes.exchange_routes import router as exchange_router
from routes.mpesa_routes import router as mpesa_router


app = FastAPI(title="Async API Server", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication Dependency (replaces auth_required decorator)
async def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    # Implement your token validation logic here
    # Example: token = auth_header.split(" ")[1]
    # user = await validate_token(token)
    # return user
    return {"user_id": "example"}  # Placeholder

# Include route routers
#app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_routes.router, prefix="/users", tags=["users"], dependencies=[Depends(get_current_user)])

app.include_router(auth_router)
app.include_router(settings_router)
app.include_router(order_router)
app.include_router(exchange_router)
app.include_router(mpesa_router)


# Health Check Endpoint
@app.get("/health", tags=["health"])
async def health_check():
    try:
        # from infrastructure.database import db
        # await db.client.admin.command('ping')
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "disconnected", "error": str(e)}
        )

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

# Run with Uvicorn
if __name__ == "__main__":
    uvicorn.run(
        "main:app",  # Replace "main" with your module name
        #host=Config.HOST,
        host="localhost",
        port=8467,
        #port=Config.PORT,
        workers=cpu_count() * 2 + 1,  # Optimal worker count
        limit_concurrency=1000,       # Max concurrent connections
        timeout_keep_alive=30,        # Keep-alive timeout
        log_level="info",
        reload=Config.DEBUG
    )
