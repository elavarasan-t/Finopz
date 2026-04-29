from fastapi import APIRouter, Request, Response, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.concurrency import run_in_threadpool
from utils import AzureAuth
from src.schema import CostRequest, Credentials
from utils import limiter
from src.controller import get_usage_monthly

router = APIRouter(tags=["Azure/CostManagement/Usage"])

@router.post('/usageMonthly')
@limiter.limit("50/minute")
async def usage_monthly(Credential: Credentials, Data: CostRequest, request: Request, response: Response):
    try:
        azure_auth = AzureAuth(Credential=Credential)
        credentials = azure_auth.authenticate()
        data = []
        usage_response = await run_in_threadpool(
            get_usage_monthly,
            Data.scope,
            credentials,
            Data.grouping,
            Data.start_date,
            Data.end_date,
            Data.granularity
        )

        data.append(usage_response)

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