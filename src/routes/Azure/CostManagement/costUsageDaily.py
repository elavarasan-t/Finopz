from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from fastapi.concurrency import run_in_threadpool
from utils import authenticate
from src.schema import CostRequest, Credentials
from utils import limiter
from src.controller import get_azure_cost_usage_daily

router = APIRouter(tags=["Azure/CostManagement/CostUsage"])

@router.post('/costUsageDaily')
@limiter.limit("50/minute")
async def cost(Credential: Credentials, Data: CostRequest, request: Request, response: Response):
    try:
        credential = authenticate(Credential=Credential)
        
        cost_response = await run_in_threadpool(
            get_azure_cost_usage_daily, 
            Data.scope, 
            credential,
            Data.grouping,
            Data.cost_type,
            Data.start_date,
            Data.end_date,
            Data.granularity 
        )

        return cost_response
    
    except Exception as error:
        return JSONResponse(
            status_code=500,
            content={"detail": str(error)},
            headers=dict(response.headers)
        )

