import os
from azure.identity import ClientSecretCredential
from fastapi import HTTPException
from src.schema import Credentials

def authenticate(Credential: Credentials):
    try:
        credential = ClientSecretCredential(tenant_id=Credential.AZURE_TENANT_ID, client_id=Credential.AZURE_CLIENT_ID, client_secret=Credential.AZURE_CLIENT_SECRET)
        return credential 
    
    except Exception as error:
        raise HTTPException(status_code=500,detail="Authentication Failed")

""" 

from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")

def authenticate():
    try:
        credential = ClientSecretCredential(tenant_id=TENANT_ID, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        return credential 
    
    except Exception as error:
        raise HTTPException(status_code=500,detail="Authentication Failed") 

"""
