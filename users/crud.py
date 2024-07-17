from users.schemas import CreateUser


def create_user(user: CreateUser):
    db_user = user.model_dump()
    return {
        "success": True,
        "user": db_user,
    }
