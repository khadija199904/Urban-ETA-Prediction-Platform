from api.core.security import get_password_hash
from api.models.users import USERS
from api.schemas.user_schema import UserRegister

def create_user (user_data : UserRegister):
    hashed_password = get_password_hash(user_data.password)
    new_user = USERS(username=user_data.username,password_hash=hashed_password)
    return new_user 