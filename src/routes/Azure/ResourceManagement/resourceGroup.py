from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from fastapi.concurrency import run_in_threadpool
from utils import authenticate
from src.schema import ResourceGroupIdRequest, Credentials
from utils import limiter
from src.controller import get_azure_resource_group

router = APIRouter(tags=["Azure/Inventory"])

@router.post('/resourceGroup')
@limiter.limit("50/minute")
async def resource_group(Credential: Credentials, Data: ResourceGroupIdRequest, request: Request, response: Response):
    try:
        credentials = authenticate(Credential=Credential)
        response = await run_in_threadpool(get_azure_resource_group, credentials, Data.resource_group_id)
        
        return { "response": response }
    
    except Exception as error:
        return JSONResponse(
            status_code=500,
            content={"detail": str(error)},
            headers=dict(response.headers)
        )