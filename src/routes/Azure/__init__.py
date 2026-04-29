from fastapi import APIRouter, Depends

from dependency import validateAPIKEY

from .ResourceManagement import resource, resourceGroup, resourceGroups, resources, subscription, subscriptionResources, subscriptions

from .CostManagement import cost, costDaily, costMonthly, costUsage, costUsageDaily, costUsageMonthly , costUsageV2, costV2, foreCastCost, individualResourceCost, individualResourceGroupCost, individualResourceUsage, individualSubscriptionCost, resourceGroupsCost, resourcesCost, usageQuantity, usageQuantityDaily, usageQuantityMonthly

from .Tenant import tenant

router = APIRouter(dependencies=[Depends(validateAPIKEY.validate_api_key)])

router.include_router(subscriptions.router, prefix='/v1/azure')
router.include_router(subscription.router, prefix='/v1/azure')
router.include_router(subscriptionResources.router, prefix='/v1/azure')
router.include_router(resourceGroup.router, prefix='/v1/azure')
router.include_router(resourceGroups.router, prefix='/v1/azure')
router.include_router(resources.router, prefix='/v1/azure')
router.include_router(resource.router, prefix='/v1/azure')

#router.include_router(cost.router, prefix='/v1/azure')
router.include_router(costV2.router, prefix='/v1/azure')
router.include_router(costDaily.router, prefix='/v1/azure')
router.include_router(costMonthly.router, prefix='/v1/azure')
router.include_router(foreCastCost.router, prefix='/v1/azure')
router.include_router(usageQuantity.router, prefix='/v1/azure')
router.include_router(usageQuantityDaily.router, prefix='/v1/azure')
router.include_router(usageQuantityMonthly.router, prefix='/v1/azure')

#router.include_router(individualSubscriptionCost.router, prefix='/v1/azure')
router.include_router(resourceGroupsCost.router, prefix='/v1/azure')
router.include_router(individualResourceGroupCost.router, prefix='/v1/azure')
router.include_router(resourcesCost.router, prefix='/v1/azure')
router.include_router(individualResourceCost.router, prefix='/v1/azure')
router.include_router(individualResourceUsage.router, prefix='/v1/azure')

#router.include_router(costUsage.router, prefix='/v1/azure')
router.include_router(costUsageV2.router, prefix='/v1/azure')
router.include_router(costUsageDaily.router, prefix='/v1/azure')
router.include_router(costUsageMonthly.router, prefix='/v1/azure')

router.include_router(tenant.router, prefix='/v1/azure')
