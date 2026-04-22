from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from fastapi.concurrency import run_in_threadpool
from utils import authenticate
from src.schema import CostRequest, Credentials
from utils import limiter
from src.controller import get_resources_groups_cost

router = APIRouter(tags=["Azure/CostManagement/Cost"])

@router.post('/resourceGroupsCost')
@limiter.limit("50/minute")
async def resourceGroupsCost(Credential: Credentials, Data: CostRequest, request: Request, response: Response):

    try:

        credential = authenticate(Credential=Credential) 

        cost_response = await run_in_threadpool(
            get_resources_groups_cost,
            Data.scope, 
            credential,
            Data.grouping,
            Data.cost_type,
            Data.start_date,
            Data.end_date,
            Data.granularity
        )
    
        return { "response": cost_response }
                
    except Exception as error:
        return JSONResponse(
            status_code=500,
            content={"detail": str(error)},
            headers=dict(response.headers)
        )
        