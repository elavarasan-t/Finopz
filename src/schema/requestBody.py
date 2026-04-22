from pydantic import BaseModel
from datetime import  timezone, datetime
import calendar
from typing import Optional

today = datetime.now(timezone.utc).date()
start_date = today.replace(day=1) 
last_day = calendar.monthrange(today.year, today.month)[1]
end_date = today.replace(day=last_day)

class SubscriptionRequest(BaseModel):
    subscription_id: str 

class ResourceGroupIdRequest(BaseModel):
    resource_group_id: str

class ResourceIdRequest(BaseModel):
    resource_id: str

class CostRequest(BaseModel):
    scope: str 
    cost_type: Optional[str] = "ActualCost"
    start_date: Optional[str] = start_date 
    end_date: Optional[str] = end_date 
    granularity: Optional[str] = "None" 
    grouping: Optional[str] = "None"

class Credentials(BaseModel):
    AZURE_TENANT_ID : str
    AZURE_CLIENT_ID : str
    AZURE_CLIENT_SECRET : str
    