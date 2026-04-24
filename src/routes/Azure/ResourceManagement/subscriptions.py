from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from fastapi.concurrency import run_in_threadpool
from src.schema import Credentials
from src.controller import get_azure_subscriptions
from utils import AzureAuth
from utils import limiter

router = APIRouter(tags=["Azure/Inventory"])

@router.post('/subscriptions')
@limiter.limit("50/minute")
async def list_subscriptions(
    Credential: Credentials,
    request: Request,
    response: Response
):
    try:

        azure_auth = AzureAuth(Credential=Credential)
        credentials = azure_auth.authenticate()
        response_body = await run_in_threadpool(get_azure_subscriptions, credentials)

        return {
            "response" : response_body
        }
    
    except Exception as error:
        return JSONResponse(
            status_code=500,
            content={"detail": str(error)},
            headers=dict(response.headers)
        )
    