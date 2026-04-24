from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from fastapi.concurrency import run_in_threadpool
from utils import AzureAuth
from src.schema import SubscriptionRequest, Credentials
from utils import limiter
from src.controller import get_azure_subscription

router = APIRouter(tags=["Azure/Inventory"])

@router.post('/subscription')
@limiter.limit("50/minute")
async def subscription_data(Credential: Credentials, Data: SubscriptionRequest, request: Request, response: Response):
    try:
        azure_auth = AzureAuth(Credential=Credential)
        credentials = azure_auth.authenticate()
        response_body = await run_in_threadpool(get_azure_subscription, credentials, Data.subscription_id)   
        return { "response":  response_body }
    
    except Exception as error:
        return JSONResponse(
            status_code=500,
            content={"detail": str(error)},
            headers=dict(response.headers)
        )
        