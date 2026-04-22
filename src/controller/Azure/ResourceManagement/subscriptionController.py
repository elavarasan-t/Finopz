from azure.mgmt.subscription import SubscriptionClient


def get_azure_subscription(credential, subscription_id):
    subscription = SubscriptionClient(credential=credential).subscriptions.get(subscription_id=subscription_id)
    return subscription.as_dict()