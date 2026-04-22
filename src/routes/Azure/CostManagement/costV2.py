from fastapi import APIRouter, Request, Response
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
from utils import authenticate
from src.schema import CostRequest, Credentials
from utils import limiter
from src.controller import get_azure_cost_v2

router = APIRouter(tags=["Azure/CostManagement/Cost"])

@router.post('/cost')
@limiter.limit("50/minute")
async def cost(Credential: Credentials, Data: CostRequest, request: Request, response: Response):
    
    try:
        credential = authenticate(Credential=Credential)
        
        cost_response = await run_in_threadpool(
            get_azure_cost_v2, 
            Data.scope, 
            credential,
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