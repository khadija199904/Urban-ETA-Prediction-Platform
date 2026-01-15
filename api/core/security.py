from passlib.context import CryptContext
from fastapi import Header 
from jose import jwt 
from api.core.config import SECRET_KEY
from fastapi import HTTPException




#------------Password-------------------------

# On configure l'outil qui va crypter les mots de passe
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)


# veification de password hashing
def verify_password_hash(normal_password, hashed_password):
        return pwd_context.verify(normal_password, hashed_password)




#-----------------------Token----------------

def create_token (user) :
    payload = { "Username" : user.username}
    token = jwt.encode(payload,key=SECRET_KEY)
    return token



# verificatin de token crée en login
def verify_token(token : str = Header()):
  try:
      token_decoded = jwt.decode(token=token,key=SECRET_KEY)
      return token_decoded
  except :
      #  GESTION TOKEN MANQUANT
      raise HTTPException(status_code=401,detail="Token d'authentification manquant")