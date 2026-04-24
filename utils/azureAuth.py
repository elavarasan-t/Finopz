from azure.identity import ClientSecretCredential
from fastapi import HTTPException
from src.schema import Credentials

class AzureAuth:

    def __init__(self, Credential: Credentials):
        self.tenant_id = Credential.azure_tenant_id
        self.client_id = Credential.azure_client_id
        self.client_secret = Credential.azure_client_secret

    def authenticate(self):
        try:
            credential = ClientSecretCredential(tenant_id=self.tenant_id, client_id=self.client_id, client_secret=self.client_secret)
            return credential 
    
        except Exception as error:
            raise HTTPException(status_code=500,detail=f"Authentication Failed : {error} ")

