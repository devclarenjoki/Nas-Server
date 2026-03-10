# interfaces/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from config import Config
from infrastructure.database import db

from domain.services import UserService
       

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get current authenticated user from JWT token
    """
    try:
        payload = jwt.decode(
            credentials.credentials,
            Config.SECRET_KEY,
            algorithms=[Config.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )

        user = await UserService.get_user_by_phone(user_id)
        
        #user = await db.user.find_one({"_id": user_id})
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
            
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )


async def get_current_admin_user(
    current_user: dict = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Dependency that ensures the current user has admin privileges.
    Checks 'isAdmin' field directly in the JWT token payload.
    """
    try:
        # Decode the token again to access the isAdmin claim
        payload = jwt.decode(
            credentials.credentials,
            Config.SECRET_KEY,
            algorithms=[Config.ALGORITHM]
        )
        
        # Check for isAdmin field in the token payload
        is_admin = payload.get("isAdmin", False)
        
        if not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )
            
        return current_user
        
    except JWTError:
        # This ensures the token is still valid even if we are re-decoding
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

"""
# interfaces/dependencies.py
from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from config import Config
from infrastructure.database import db  # Assuming you have a DB connection

async def get_current_user(request: Request):
    
    #Dependency to get current authenticated user

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Fetch user from database (async)
    user = await db.users.find_one({"_id": user_id})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user
"""
