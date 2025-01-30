import copy
import logging
import random
import uuid
from datetime import datetime, timedelta
from pprint import pprint
from typing import Any, Dict

import yaml

import config
from m3ter_client.api_client import AuthenticationError, M3terApiClient

# Configure logging only in main.py
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_pricing_payload(catalog):
    # Extract the Aggregations and Pricings
    aggregations = catalog["Aggregation"]
    pricings = catalog["Pricing"]

    # Create a keyword-based mapping from aggregation names to their IDs
    aggregation_map = {}
    for agg in aggregations:
        if "Requests" in agg["name"]:
            aggregation_map["Requests"] = agg["id"]
        elif "Duration" in agg["name"]:
            aggregation_map["Duration"] = agg["id"]
   

    # Map the IDs to the pricing description fields
    for pricing in pricings:
        description = pricing["description"]
        
        # Update the aggregationId based on the description keyword
        pricing["aggregationId"] = aggregation_map.get(description)

def generate_random_timestamp(start: str, end: str) -> str:
    """
    Generates a random timestamp between the given start and end date strings.
    """
    start = datetime.strptime("2024-12-01T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
    end = datetime.strptime("2024-12-31T20:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    ts = (start + timedelta(seconds=random_seconds)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return ts

def generate_measurements_payload(meter_code: str, account_code: str, start_ts: str, end_ts: str, size: int) -> Dict[str, Any]:
    """
    Generates a payload with a list of random measurements.
    
    Parameters:
    - size (int): The number of measurement objects to generate.
    
    Returns:
    - Dict[str, Any]: A payload with a list of random measurements.
    """
    measurements = []
    for _ in range(size):
        measurement = {
            "uid": str(uuid.uuid4()),
            "meter": meter_code,
            "account": account_code,
            "ts": generate_random_timestamp(start_ts, end_ts),
            # update aggregation codes suffix before you run
            "measure": {
                "memory_consumption_api_2": random.randint(1, 100),
                "execution_time_api_2": random.randint(1000, 5000)
            }
        }
        measurements.append(measurement)

    return {"measurements": measurements}


def task1 () -> None:
    try:
        # Load catalog data
        with open("catalog.yaml", "r") as file:
            catalog = yaml.safe_load(file)        
        
        # Initialize client
        client = M3terApiClient(access_key=config.access_key, api_secret=config.api_secret, org_id=config.org_id)

        # Authenticate
        client.authenticate()

        # Create Product
        product_name = catalog["Product"]["name"]
        product_code = catalog["Product"]["code"]
        
        # product_response = client.create_product(name=product_name, code=product_code)
        # product_id = product_response.get("id")
        product_id = 'b0e80927-aba4-422a-a710-24cd4fd3ac2b'  #api 2
        # product_id = '2b46eef6-ed58-4047-b1d4-c03849ceb83c'  #api 3
        catalog["Product"]["id"] = product_id

        # Create Meter
        catalog["Meter"]["productId"] = catalog["Product"]["id"]
        meter_payload = catalog["Meter"]
        # meter_response = client.create_meter(payload = meter_payload)
        # meter_id = meter_response.get("id")
        meter_id = '4998c4fa-ffbd-4595-b56c-1cd4b010b632'
        catalog["Meter"]["id"] = meter_id

        # Create Aggregations
        aggregations = catalog["Aggregation"]
        for aggregation_payload in aggregations:

            aggregation_payload["meterId"] = meter_id
            # aggregation_response = client.create_aggregation(aggregation_payload)
            # aggregation_id = aggregation_response.get("id")
            # aggregation_payload["id"] = aggregation_id
            
            # pprint(aggregation_response)
            # print('\n\n')

        pprint(catalog)
        print('\n\n')


        with open("catalog_after_task1.yaml", "w") as file:
            yaml.safe_dump(catalog, file, default_flow_style=False, sort_keys=False)

    except AuthenticationError as auth_err:
        logger.error("Authentication Error: %s", auth_err)
    except Exception as e:
        logger.error("Error: %s", e)

def task2() -> None:
    try:
        # Load catalog data
        with open("catalog_after_task1.yaml", "r") as file:
            catalog = yaml.safe_load(file)        
        
        # Initialize client
        client = M3terApiClient(access_key=config.access_key, api_secret=config.api_secret, org_id=config.org_id)

        # Authenticate
        client.authenticate()

        # Create PlanTemplate
        catalog["PlanTemplate"]["productId"] = catalog["Product"]["id"]
        plan_template_payload = catalog["PlanTemplate"]
        # plan_template_response = client.create_plan_template(payload = plan_template_payload)
        # plan_template_id = plan_template_response.get("id")
        plan_template_id = 'ad7856cf-c600-4d17-8fd3-20fc223eca11'
        catalog["PlanTemplate"]["id"] = plan_template_id

        # Create Plan
        catalog["Plan"]["planTemplateId"] = catalog["PlanTemplate"]["id"]
        plan_payload = catalog["Plan"]
        # plan_response = client.create_plan(payload = plan_payload)
        # plan_id = plan_response.get("id")
        plan_id = '87bda8f7-347d-4b2e-98c0-e4bc960087df'
        catalog["Plan"]["id"] = plan_id
        

        # Create Pricing
        create_pricing_payload(catalog)
        pricings = catalog["Pricing"]
        for pricing_payload in pricings:

            pricing_payload["planId"] = plan_id
            pricing_response = client.create_pricing(pricing_payload)
            pricing_id = pricing_response.get("id")
            pricing_payload["id"] = pricing_id
            
            # pprint(aggregation_response)
        print('\n\n')

        
        pprint(catalog["Pricing"])
        print('\n\n')

        with open("catalog_after_task2.yaml", "w") as file:
            yaml.safe_dump(catalog, file, default_flow_style=False, sort_keys=False)



    except AuthenticationError as auth_err:
        logger.error("Authentication Error: %s", auth_err)
    except Exception as e:
        logger.error("Error: %s", e)

def task3() -> None:
    try:
        # Load catalog data
        with open("catalog_after_task2.yaml", "r") as file:
            catalog = yaml.safe_load(file)
        
        # Initialize client
        client = M3terApiClient(access_key=config.access_key, api_secret=config.api_secret, org_id=config.org_id)
        # Authenticate
        client.authenticate()

        # Create Accounts and AccountPlans
        # Extract the list of customers from the YAML
        accounts = catalog["Account"]
        catalog["AccountPlan"]["planId"] = catalog["Plan"]["id"]
        account_plan_payload = catalog["AccountPlan"]

        for account_payload in accounts:
            # create account request
            account_response = client.create_account(account_payload)
            account_id = account_response.get("id")
            account_payload["id"] = account_id
            # create account plan request
            account_plan_payload["accountId"] = account_id
            client.create_account_plan(account_plan_payload)

        with open("catalog_after_task3.yaml", "w") as file:
            yaml.safe_dump(catalog, file, default_flow_style=False, sort_keys=False)

        print('\n\n')
        pprint(accounts)
        print('\n\n')

    except AuthenticationError as auth_err:
        logger.error("Authentication Error: %s", auth_err)
    except Exception as e:
        logger.error("Error: %s", e)

def task4() -> None:
    try:
        # Load catalog data
        with open("catalog_after_task3.yaml", "r") as file:
            catalog = yaml.safe_load(file)
        
        # Initialize client
        client = M3terApiClient(access_key=config.access_key, api_secret=config.api_secret, org_id=config.org_id)
        # Authenticate
        client.authenticate()


        start_ts = "2024-12-01T00:00:00.000Z"
        end_ts = "2024-12-31T20:00:00.000Z"
        meter_code = catalog["Meter"]["code"]
        accounts = catalog["Account"]
        
        size=120
        for account in accounts:
            account_code = account["code"]
            measurements = generate_measurements_payload(meter_code, account_code, start_ts, end_ts, size)
            client.ingest_usage(payload=measurements)


        # account_code = catalog["Meter"]["code"]
        # memory_consumption_aggregation_code = catalog["Meter"]["code"]
        # execution_time_aggregation_code = catalog["Meter"]["code"]

        # "2024-12-01T00:00:00.000Z", "2024-12-31T20:00:00.000Z"
        # pprint()


        # # Create Accounts and AccountPlans
        # # Extract the list of customers from the YAML
        
        # catalog["AccountPlan"]["planId"] = catalog["Plan"]["id"]
        # account_plan_payload = catalog["AccountPlan"]

       



        # with open("catalog_after_task3.yaml", "w") as file:
        #     yaml.safe_dump(catalog, file, default_flow_style=False, sort_keys=False)

        # print('\n\n')
        # pprint(accounts)
        # print('\n\n')

    except AuthenticationError as auth_err:
        logger.error("Authentication Error: %s", auth_err)
    except Exception as e:
        logger.error("Error: %s", e)


if __name__ == "__main__":

    # task1()
    # task2()
    # task3()
    task4()
    