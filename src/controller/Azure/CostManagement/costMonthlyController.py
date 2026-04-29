from utils import AzureCostManagement
from utils import DataSetMethods

def get_cost_monthly(scope, credential, grouping, cost_type, start_date, end_date, granularity):

    azure_cost = AzureCostManagement(
                scope=scope,
                credential=credential,
                grouping=DataSetMethods.grouping(grouping_term="SubscriptionCost"),
                cost_type=cost_type,
                from_date=start_date,
                to_date=end_date,
                granularity="MONTHLY"
            )
    
    cost = azure_cost.costManagement()
    
    subscription_id = scope.split('/')[2]

    columns = cost.get("column",[])

    id_pretaxcost = columns.index("PreTaxCost")
    id_pretaxcost_usd = columns.index("PreTaxCostUSD")
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
    id_pricingmodel = columns.index("PricingModel")
    id_charge_type = columns.index("ChargeType")
    id_currency = columns.index("Currency")

    #total_cost = sum(row[id_pretaxcost] for row in cost.get("row", []))
    #total_cost_usd = sum(row[id_pretaxcost_usd] for row in cost.get("row", []))

    response = {
        subscription_id : {
            #"subscription_total_cost" : round(total_cost, 2),
            #"subscription_total_cost_USD" : round(total_cost_usd, 2) 
        }
    }

    for row in cost.get("row", []):

        pretaxcost = row[id_pretaxcost]
        pretaxcost_usd = row[id_pretaxcost_usd]
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
        pricingmodel = row[id_pricingmodel]
        charge_type = row[id_charge_type]
        currency = row[id_currency]

        if resource_group not in response[subscription_id]:
            response[subscription_id][resource_group] = {
                    "resources": []
                    }
  
        response[subscription_id][resource_group]["resources"].append({
            "pretaxcost" : pretaxcost,
            "currency": currency,
            "pretaxcostUSD": pretaxcost_usd,
            "billingMonth": billing_month,
            "resourceLocation": resource_location,
            "resourceId": resource_id,
            "serviceFamily": service_family,
            "serviceName": service_name,
            "meterCategory": meter_category,
            "meterSubCategory": meter_subcategory,
            "meter": meter,
            "product": product,
            "unitofmeasure": unitofmeasure,
            "pricingmodel": pricingmodel,
            "charge_type": charge_type
        })

    return response