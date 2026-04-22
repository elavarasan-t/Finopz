1. mkdir myapp
2. cd myapp
3. python -m venv .venv
4. .venv\Scripts\Activate.ps1
5. pip install fastapi uvicorn
6. fastapi deploy

packages needs to be installed:

1. pip install dotenv - accessing .env files
2. pip install azure-core
3. pip install azure-identity - ClientSecretCreddentials
4. pip install azure-mgmt-subscription - SubscriptionClient
5. pip install azure-mgmt-resource - ResourceManagementClient
6. pip install azure-mgmt-resourceGraph - ResourceGraphClient
7. pip install azure-mgmt-costmanagement - CostManagementClient
8. pip install msgraph-sdk - fro getting tenant data
9. pip install fastapi-limiter - limits the api requests 
10. pip install pycryptodome - aes encrytion and decryption

Grouping inputs:
1. None
2. ResourceGroup
3. ResourceId
4. ServiceFamily
5. MeterCategory
6. MeterSubCategory
7. Meter
8. Product
9. Location
10. PricingModel
11. RGS - Resource group with service name
12. RGRID  - Resource grooup with resource id
13. RIDMC - resource Id with meter MeterCategory
14. Service - resource id with service family and meter category
15. RGRIDS - resource group with resource id and service name
16. ServiceName

maximam grouping limit 15

Cost Type:
1. ActualCost
2. Usage
3. AmortizedCost

Granularity 
1. NONE
2. DAILY
3. MONTHLY

Aggregation:
1. PreTaxCost
2. PreTaxCostUSD
3. Cost
4. CostUSD
5. UsageQuantity

overall forcastCost = cost + forecastCost 




