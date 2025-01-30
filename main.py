import logging
from pprint import pprint

import yaml

import config
from m3ter_client.api_client import AuthenticationError, M3terApiClient

# Configure logging only in main.py
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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
    pass


if __name__ == "__main__":

    task1()
    



# from m3ter_client.config import load_config
# Example usage
# if __name__ == "__main__":
#     try:
#         settings = load_config()
#         print(settings)
#         # print(type(settings))
#     except RuntimeError as e:
#         print(e)