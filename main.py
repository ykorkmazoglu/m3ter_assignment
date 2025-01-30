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
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_pricing_payload(mock_data):
    # This function gets aggregation M3ter ids from mock_data
    # and adds them to the payload of pricing
    # it avoids manual work
    # it is called in task1()

    # Extract the Aggregations and Pricings
    aggregations = mock_data["Aggregation"]
    pricings = mock_data["Pricing"]

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


def generate_random_timestamp(start_ts: str, end_ts: str) -> str:
    # Generates a random timestamp between start_ts and end_ts date strings.

    start = datetime.strptime(start_ts, "%Y-%m-%dT%H:%M:%S.%fZ")
    end = datetime.strptime(end_ts, "%Y-%m-%dT%H:%M:%S.%fZ")
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    ts = (start + timedelta(seconds=random_seconds)
          ).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return ts


def generate_measurements_payload(meter_code: str, account_code: str, start_ts: str, end_ts: str, size: int) -> Dict[str, Any]:
    # Generates a payload with a list of random measurements.
    # manually update measure memory_consumption_api_x and xecution_time_api_x with the correct aggregation names
    # this function will generate below values for each measurement:
    #   - a random uid
    #   - a random integer for memory consumption between 1 and 100
    #   - a random integer for execution time between 1000 and 5000
    #   - a random timestamp in December 2024

    measurements = []
    for _ in range(size):
        measurement = {
            "uid": str(uuid.uuid4()),
            "meter": meter_code,
            "account": account_code,
            "ts": generate_random_timestamp(start_ts, end_ts),
            # update aggregation codes suffix before you run
            "measure": {
                # update this before running task4
                "memory_consumption_api_3": random.randint(1, 100),
                # update this before running task4
                "execution_time_api_3": random.randint(1000, 5000)
            }
        }
        measurements.append(measurement)

    return {"measurements": measurements}


def task1() -> None:
    # This function needs mock_data.yaml file
    # It creates below  entities:
    #
    # Product: AWS Lambda API X
    # Meter: Compute and Requests Meter API X
    # Aggregations:
    #     - Duration Aggregation API X
    #     - Total Number of Requests API X

    try:
        # Load mock data
        with open("mock_data.yaml", "r") as file:
            mock_data = yaml.safe_load(file)

        # Initialize client
        client = M3terApiClient(access_key=config.access_key,
                                api_secret=config.api_secret, org_id=config.org_id)

        # Authenticate
        client.authenticate()

        # Create Product
        product_name = mock_data["Product"]["name"]
        product_code = mock_data["Product"]["code"]
        # Make create product request
        product_response = client.create_product(
            name=product_name, code=product_code)
        product_id = product_response.get("id")
        # Save m3ter product id for other requests: create_meter
        mock_data["Product"]["id"] = product_id

        # Create Meter
        mock_data["Meter"]["productId"] = mock_data["Product"]["id"]
        meter_payload = mock_data["Meter"]
        # Make create meter request
        meter_response = client.create_meter(payload=meter_payload)
        meter_id = meter_response.get("id")
        # Save m3ter meter id for other requests: create_aggregations
        mock_data["Meter"]["id"] = meter_id

        # Create 2 Aggregations required in the task
        aggregations = mock_data["Aggregation"]
        for aggregation_payload in aggregations:
            # add meterId to aggregation payload
            aggregation_payload["meterId"] = meter_id
            aggregation_response = client.create_aggregation(
                aggregation_payload)
            aggregation_id = aggregation_response.get("id")
            aggregation_payload["id"] = aggregation_id

        # After M3ter entities are created, mock data is updated with M3ter ids
        # and saved in this new yaml file for task 2: mock_data_after_task1.yaml
        with open("mock_data_after_task1.yaml", "w") as file:
            yaml.safe_dump(
                mock_data, file, default_flow_style=False, sort_keys=False)

    except AuthenticationError as auth_err:
        logger.error("Authentication Error: %s", auth_err)
    except Exception as e:
        logger.error("Error: %s", e)


def task2() -> None:
    # This function needs mock_data_after_task1.yaml file
    # It needs to be run after task1
    # It creates below  entities:
    #
    # Plan Template: Lambda Template API X
    # Plan: Lambda Plan API X
    # Pricing

    try:
        # Load mock data
        with open("mock_data_after_task1.yaml", "r") as file:
            mock_data = yaml.safe_load(file)

        # Initialize client
        client = M3terApiClient(access_key=config.access_key,
                                api_secret=config.api_secret, org_id=config.org_id)

        # Authenticate
        client.authenticate()

        # Create PlanTemplate
        mock_data["PlanTemplate"]["productId"] = mock_data["Product"]["id"]
        plan_template_payload = mock_data["PlanTemplate"]
        # Make create plan template request
        plan_template_response = client.create_plan_template(
            payload=plan_template_payload)
        # Save m3ter planTemplate id for other requests
        plan_template_id = plan_template_response.get("id")
        mock_data["PlanTemplate"]["id"] = plan_template_id

        # Create Plan
        mock_data["Plan"]["planTemplateId"] = mock_data["PlanTemplate"]["id"]
        plan_payload = mock_data["Plan"]
        plan_response = client.create_plan(payload=plan_payload)
        # Save m3ter plan id for other requests
        plan_id = plan_response.get("id")
        mock_data["Plan"]["id"] = plan_id

        # Create Pricing
        # Generate Pricing Payload
        create_pricing_payload(mock_data)

        # Create 2 pricing components of the plan required in the task
        pricings = mock_data["Pricing"]
        for pricing_payload in pricings:

            pricing_payload["planId"] = plan_id
            pricing_response = client.create_pricing(pricing_payload)
            pricing_id = pricing_response.get("id")
            pricing_payload["id"] = pricing_id

        # After M3ter entities are created, mock data is updated with M3ter ids
        # and saved in this new yaml file for task 3: mock_data_after_task2.yaml
        with open("mock_data_after_task2.yaml", "w") as file:
            yaml.safe_dump(
                mock_data, file, default_flow_style=False, sort_keys=False)

    except AuthenticationError as auth_err:
        logger.error("Authentication Error: %s", auth_err)
    except Exception as e:
        logger.error("Error: %s", e)


def task3() -> None:
    # This function needs mock_data_after_task2.yaml file
    # It needs to be run after task2
    # It creates below  entities:
    #
    # Account:
    #   - Mickey Mouse Inc API X
    #   - Donald Duck Ltd API X
    #   - Pluto LLP API X
    # AccountPlan (see attached plans for each account in the UI)

    try:
        # Load mock data
        with open("mock_data_after_task2.yaml", "r") as file:
            mock_data = yaml.safe_load(file)

        # Initialize client
        client = M3terApiClient(access_key=config.access_key,
                                api_secret=config.api_secret, org_id=config.org_id)
        # Authenticate
        client.authenticate()

        # Create Accounts and AccountPlans
        # Extract the list of accounts from mock_data
        accounts = mock_data["Account"]
        # add plan id to the account plan payload
        mock_data["AccountPlan"]["planId"] = mock_data["Plan"]["id"]
        account_plan_payload = mock_data["AccountPlan"]

        for account_payload in accounts:
            # make account request
            account_response = client.create_account(account_payload)
            account_id = account_response.get("id")
            account_payload["id"] = account_id
            # make account plan request
            account_plan_payload["accountId"] = account_id
            client.create_account_plan(account_plan_payload)

        # After M3ter entities are created, mock data is updated with M3ter ids
        # and saved in this new yaml file: mock_data_after_task3.yaml
        with open("mock_data_after_task3.yaml", "w") as file:
            yaml.safe_dump(
                mock_data, file, default_flow_style=False, sort_keys=False)

    except AuthenticationError as auth_err:
        logger.error("Authentication Error: %s", auth_err)
    except Exception as e:
        logger.error("Error: %s", e)


def task4() -> None:
    # This function needs mock_data_after_task3.yaml file
    # It needs to be run after task3
    # It ingests usage data. It generates any number of usage events (measurements) with random values
    # Usage timestamps are created for December.

    # Before ingesting usage in task4, go to the function generate_measurements_payload above
    # and update the aggregation names (keys) in measure field:
    # memory_consumption_api_x, execution_time_api_x

    try:
        # Load mock data
        with open("mock_data_after_task3.yaml", "r") as file:
            mock_data = yaml.safe_load(file)

        # Initialize client
        client = M3terApiClient(access_key=config.access_key,
                                api_secret=config.api_secret, org_id=config.org_id)
        # Authenticate
        client.authenticate()

        # for random usage timestamps. ts will be between below two dates
        start_ts = "2024-12-01T00:00:00.000Z"
        end_ts = "2024-12-31T20:00:00.000Z"

        # fields to be used in measurements payload
        meter_code = mock_data["Meter"]["code"]
        accounts = mock_data["Account"]

        # Generating random single measurement and ingesting for each account
        size = 1
        for account in accounts:
            account_code = account["code"]
            measurements = generate_measurements_payload(
                meter_code, account_code, start_ts, end_ts, size)
            client.ingest_usage(payload=measurements)

        # Generating random 120 measurements and ingesting for each account
        size = 120
        for account in accounts:
            account_code = account["code"]
            measurements = generate_measurements_payload(
                meter_code, account_code, start_ts, end_ts, size)
            client.ingest_usage(payload=measurements)

    except AuthenticationError as auth_err:
        logger.error("Authentication Error: %s", auth_err)
    except Exception as e:
        logger.error("Error: %s", e)


if __name__ == "__main__":

    # update mock_data.yaml if needed before you run task1
    # to verify changes run each task at a in below order
    # see READ.md

    # task1()
    # task2()
    # task3()

    # Before ingesting usage in task4, go to the function generate_measurements_payload above
    # and update the aggregation names (keys) in measure field:
    # memory_consumption_api_x, execution_time_api_x
    task4()
