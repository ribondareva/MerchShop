from fastapi_users.authentication import AuthenticationBackend

from api.dependencies.authentification.strategy import get_jwt_strategy

from core.authentication.transport import bearer_transport


authentication_backend = AuthenticationBackend(
    # name="access-tokens-db",
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
