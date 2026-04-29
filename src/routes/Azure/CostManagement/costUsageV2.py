from fastapi import APIRouter, Request, Response, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.concurrency import run_in_threadpool
from utils import AzureAuth
from src.schema import CostRequest, Credentials
from utils import limiter
from src.controller import get_azure_cost_usage_v2

router = APIRouter(tags=["Azure/CostManagement/CostUsage"])

@router.post('/costUsage')
@limiter.limit("50/minute")
async def cost_usage(Credential: Credentials, Data: CostRequest, request: Request, response: Response):
    try:
        azure_auth = AzureAuth(Credential=Credential)
        credentials = azure_auth.authenticate()
        data = []
        cost_response = await run_in_threadpool(
            get_azure_cost_usage_v2, 
            Data.scope, 
            credentials,
            Data.grouping,
            Data.cost_type,
            Data.start_date,
            Data.end_date,
            Data.granularity 
        )

        data.append(cost_response)

        return {
            "success": True, 
            "status_code": status.HTTP_200_OK,
            "data": data,
            "errors": None
        }
    
    except HTTPException as exc:
        raise exc
    
    except Exception as error:
        return JSONResponse(
            status_code=500,
            content={"detail": str(error)},
            headers=dict(response.headers)
        )

