from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class HashPassword:
    def create_hash(self, password:str):
        return pwd_context.hash(password)


    def verify_hash(self, unhashed_password, hashed_password:str) -> bool:
        return pwd_context.verify(unhashed_password, hashed_password)