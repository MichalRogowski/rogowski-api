import os
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


class Authenticator:
    security = HTTPBasic()

    @staticmethod
    def confirm_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
        env_variables = dict(os.environ)
        correct_username = secrets.compare_digest(
            credentials.username, env_variables["USERNAME"]
        )
        correct_password = secrets.compare_digest(
            credentials.password, env_variables["PASSWORD"]
        )
        if not (correct_username and correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
        return credentials.username
