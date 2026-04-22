from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from fastapi.concurrency import run_in_threadpool
from utils import authenticate
from src.schema import CostRequest, Credentials
from utils import limiter
from src.controller import get_individual_resource_usage

router = APIRouter(tags=["Azure/CostManagement/Usage"])

@router.post('/individualResourceUsage')
@limiter.limit("50/minute")
async def individualResourceUsage(Credential: Credentials, Data: CostRequest, request: Request, response: Response):
    try:
        credential = authenticate(Credential=Credential)
        
        usage_response = await run_in_threadpool(
            get_individual_resource_usage, 
            Data.scope, 
            credential,
            Data.grouping,
            Data.start_date,
            Data.end_date,
            Data.granularity
        )

        return usage_response
    
    except Exception as error:
        return JSONResponse(
            status_code=500,
            content={"detail": str(error)},
            headers=dict(response.headers)
        )
                