from domain.services import UserService

class UserUseCase:
    @staticmethod
    async def get_profile(user_id):
        user = await UserService.get_user_by_id(user_id)
        if user:
            return {
                "id": str(user._id),
                "name": user.name,
                "phone":user.phone,
                "country":user.country,
                "isAdmin":user.isAdmin,
                "created_at": user.created_at.isoformat(),

            }, 200
        return {"error": "User not found"}, 404
