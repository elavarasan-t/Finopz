from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from fastapi.concurrency import run_in_threadpool
from utils import AzureAuth
from src.schema import CostRequest, Credentials
from utils import limiter
from src.controller import get_azure_cost

router = APIRouter(tags=["Azure/CostManagement/Cost"])

@router.post('/cost')
@limiter.limit("50/minute")
async def cost(Credential: Credentials, Data: CostRequest, request: Request, response: Response):
    try:
        azure_auth = AzureAuth(Credential=Credential)
        credentials = azure_auth.authenticate()
        
        cost_response = await run_in_threadpool(
            get_azure_cost, 
            Data.scope, 
            credentials,
            Data.grouping,
            Data.cost_type,
            Data.start_date,
            Data.end_date,
            Data.granularity 
        )

        return { f"{Data.scope.split('/')[2]}": cost_response }
    
    except Exception as error:
        return JSONResponse(
            status_code=500,
            content={"detail": str(error)},
            headers=dict(response.headers)
        )