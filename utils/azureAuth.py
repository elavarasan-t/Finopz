import os
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from .aesDecryption import DecryptAES
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from src.schema import Credentials

class AzureAuth:

    load_dotenv()

    DECRYPT_KEY = os.getenv("AES_KEY")

    def __init__(self, Credential: Credentials):
        self.tenant_id = Credential.azure_tenant_id
        self.client_id = Credential.azure_client_id
        self.client_secret = Credential.azure_client_secret

    def authenticate(self):

        try:
            azure_tenant = DecryptAES(self.tenant_id, self.DECRYPT_KEY).decrypt_aes()
            azure_client_id = DecryptAES(self.client_id, self.DECRYPT_KEY).decrypt_aes()
            azure_client_secret = DecryptAES(self.client_secret, self.DECRYPT_KEY).decrypt_aes()

            credential = ClientSecretCredential(tenant_id=azure_tenant, client_id=azure_client_id, client_secret=azure_client_secret)

            return credential 
    
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success":False,
                    "message":"Invalid Credential",
                    "status_code": status.HTTP_401_UNAUTHORIZED
                }
            )
