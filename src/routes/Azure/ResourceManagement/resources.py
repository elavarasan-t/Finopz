from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from fastapi.concurrency import run_in_threadpool
from utils import AzureAuth
from src.schema import ResourceGroupIdRequest, Credentials
from utils import limiter
from src.controller import get_azure_resources

router = APIRouter(tags=["Azure/Inventory"])

@router.post('/resources')
@limiter.limit("50/minute")
async def list_resources(Credential: Credentials, Data: ResourceGroupIdRequest, request: Request, response: Response):
    try:
        azure_auth = AzureAuth(Credential=Credential)
        credentials = azure_auth.authenticate()
        resource_response = await run_in_threadpool(get_azure_resources, credentials, Data.resource_group_id)
        
        return { "response": resource_response }
    
    except Exception as error:
        return JSONResponse(
            status_code=500,
            content={"detail": str(error)},
            headers=dict(response.headers)
        ) 