from fastapi_users import FastAPIUsers

from api.dependencies.authentification.backend import authentication_backend
from api.dependencies.authentification.user_manager import get_user_manager
from core.models import User
from core.types.user_id import UserIDType


fastapi_users = FastAPIUsers[User, UserIDType](
    get_user_manager,
    [authentication_backend],
)
