from datetime import timedelta
from domain.services import UserService
from infrastructure.auth import verify_pin, create_access_token, verify_token
from config import Config

class AuthUseCase:
    @staticmethod
    async def register(name,phone, country, pin,isAdmin):
        # if await UserService.get_user_by_username(username):
        #     return {"error": "Username already exists"}, 400

        if await UserService.get_user_by_phone(phone):
            return {"error": "Phone Number already exists"}, 400
        

        user_id =await UserService.create_user(name,phone,country,pin,isAdmin)
        return {"message": "User created successfully", "user_id": str(user_id)}, 201
    
    @staticmethod
    async def login(phone, pin):
        user = await UserService.get_user_by_phone(phone)
        if not user or not verify_pin(pin, user.pinHash):
            return {"error": "Invalid credentials"}, 401
        
        access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.phone,"isAdmin":user.isAdmin}, expires_delta=access_token_expires
        )
        
        return {
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": Config.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }, 200
    
    @staticmethod
    async def verify_token(token):
        return verify_token(token)
