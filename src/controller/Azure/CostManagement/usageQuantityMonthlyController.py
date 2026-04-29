from utils import AzureUsageQuantity
from utils import DataSetMethods

def get_usage_monthly(scope, credentials, grouping, start_date, end_date, granularity):

    azure_usage = AzureUsageQuantity(
        scope=scope,
        credential=credentials,
        grouping=DataSetMethods.grouping(grouping_term="SubscriptionCost"),
        from_date=start_date,
        to_date=end_date,
        granularity="MONTHLY"
    )

    usage = azure_usage.usageQuantity()

    subscription_id = scope.split('/')[2]

    columns = usage.get("column",[])
    rows = usage.get("row", [])

    id_usage_quantity = columns.index("UsageQuantity")
    id_billing_month = columns.index("BillingMonth")
    id_resource_location = columns.index("ResourceLocation")
    id_rg = columns.index("ResourceGroupName")
    id_res = columns.index("ResourceId")
    id_service_family = columns.index("ServiceFamily")
    id_service_name = columns.index("ServiceName")
    id_meter_cat = columns.index("MeterCategory")
    id_meter_sub = columns.index("MeterSubCategory")
    id_meter = columns.index("Meter")
    id_product = columns.index("Product")
    id_unitofmeasure = columns.index("UnitOfMeasure")

    response = {
        subscription_id : { }
    }

    for row in rows:

        usage_quantity = row[id_usage_quantity]
        billing_month = row[id_billing_month]
        resource_location = row[id_resource_location]
        resource_group = row[id_rg] or f"unknown-rg"
        resource_id = row[id_res] or f"unknown-resource"
        service_family = row[id_service_family]
        service_name = row[id_service_name]
        meter_category = row[id_meter_cat]
        meter_subcategory = row[id_meter_sub]
        meter = row[id_meter]
        product = row[id_product]
        unitofmeasure = row[id_unitofmeasure]

        if resource_group not in response[subscription_id]:
            response[subscription_id][resource_group] = {
                    "resources": []
                    }
  
        response[subscription_id][resource_group]["resources"].append({
            "usage_quantity": usage_quantity,
            "billingMonth": billing_month,
            "resourceLocation": resource_location,
            "resourceId": resource_id,
            "serviceFamily": service_family,
            "serviceName": service_name,
            "meterCategory": meter_category,
            "meterSubCategory": meter_subcategory,
            "meter": meter,
            "product": product,
            "unitofmeasure": unitofmeasure
        })

    return response