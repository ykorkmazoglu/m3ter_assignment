import base64
import logging
from pprint import pprint
from typing import Any, Dict

import requests

# Keep module-level logger
logger = logging.getLogger(__name__)

class AuthenticationError(Exception):
    """Custom exception for authentication failures."""
    pass

class M3terApiClient:

    def __init__(self, access_key, api_secret, org_id):

        self.base_url = "https://api.m3ter.com"
        self.ingest_url = "https://ingest.m3ter.com"
        self.token = None
        
        self.access_key = access_key
        self.api_secret = api_secret
        self.org_id = org_id
        

    def authenticate(self) -> None:
        """Authenticate and store access token."""
        auth_url = f"{self.base_url}/oauth/token"
        creds = base64.b64encode(f'{self.access_key}:{self.api_secret}'.encode('ascii')).decode()

        headers = {
            'Authorization': f'Basic {creds}'
        }

        try:
            response = requests.post(auth_url, json={"grant_type": "client_credentials"}, headers=headers)
            response.raise_for_status()
            self.token = response.json()["access_token"]
            logger.info("Authentication successful")
        except requests.exceptions.RequestException as e:
            logger.error(f"Authentication failed: {str(e)}")
            # raise Exception(f"Authentication failed: {e}")
            raise AuthenticationError(f"Authentication failed: {str(e)}") from e
        

    # Task 1 
    def create_product(self, name: str, code: str, **kwargs) -> Dict[str, Any]:
        """
        Creates a product with optional additional fields.
        Required: name, code
        Optional: customFields, version
        """
        if not self.token:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        product_url = f"{self.base_url}/organizations/{self.org_id}/products"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        payload = {"name": name, "code": code, **kwargs}

        try:
            response = requests.post(product_url, headers=headers, json=payload)
            response.raise_for_status()
            logger.info("Product created successfully: %s", response.json())
            return response.json()
        
        except requests.exceptions.RequestException as e:
            status_code = response.status_code if response else "N/A"
            error_content = response.text if response else "No response content"
            logger.error(f"Failed to create product.\nStatus Code: {status_code}\nPayload: {payload}\nResponse: {error_content}\nError: {str(e)}")
            raise Exception(f"Failed to create product: {str(e)}") from e
    

    def create_meter(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a meter with the provided payload.
        The payload must include required fields such as productId, name, code, dataFields, and derivedFields.
        """
        if not self.token:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        meter_url = f"{self.base_url}/organizations/{self.org_id}/meters"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        try:
            # Send the POST request to create a meter
            response = requests.post(meter_url, headers=headers, json=payload)
            response.raise_for_status()
            
            # Log and return the successful response
            logger.info("Meter created successfully: %s", response.json())
            return response.json()

        except requests.RequestException as e:

            status_code = response.status_code if response else "N/A"
            error_content = response.text if response else "No response content"
            # Log error details
            logger.error(f"Failed to create meter.\nStatus Code: {status_code}\nPayload: {payload}\nResponse: {error_content}\nError: {str(e)}")
            # Raise an exception with details
            raise Exception(f"Failed to create meter: {str(e)} (Status Code: {status_code})") from e

    def create_aggregation(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates an aggregation with the provided payload.
        The payload must include required fields such as name, code, rounding, meterId, etc.
        """
        if not self.token:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        aggregation_url = f"{self.base_url}/organizations/{self.org_id}/aggregations"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        try:
            # Send the POST request to create an aggregation
            response = requests.post(aggregation_url, headers=headers, json=payload)
            response.raise_for_status()
            
            # Log and return the successful response
            logger.info("Aggregation created successfully: %s", response.json())
            return response.json()

        except requests.RequestException as e:
            # Handle errors and safely access response attributes
            status_code = response.status_code if response else "N/A"
            error_content = response.text if response else "No response content"
            # Log error details
            logger.error(f"Failed to create aggregation.\nStatus Code: {status_code}\nPayload: {payload}\nResponse: {error_content}\nError: {str(e)}")
            # Raise an exception with details
            raise Exception(f"Failed to create aggregation: {str(e)} (Status Code: {status_code})") from e

    # Task 2
    def create_plan_template(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a plan template with the provided payload.
        The payload must include required fields such as productId, name, currency, and code.
        """
        if not self.token:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        plan_template_url = f"{self.base_url}/organizations/{self.org_id}/plantemplates"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        try:
            # Send the POST request to create a plan template
            response = requests.post(plan_template_url, headers=headers, json=payload)
            response.raise_for_status()

            # Log and return the successful response
            logger.info("Plan template created successfully: %s", response.json())
            return response.json()

        except requests.RequestException as e:

            status_code = response.status_code if response else "N/A"
            error_content = response.text if response else "No response content"

            # Log error details
            logger.error(
                "Failed to create plan template.\n"
                "Status Code: %s\nPayload: %s\nResponse: %s\nError: %s",
                status_code, payload, error_content, str(e)
            )
            
            # Raise an exception with details
            raise Exception(f"Failed to create plan template: {str(e)} (Status Code: {status_code})") from e

    def create_plan(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a plan using the provided payload.
        The payload must include required fields such as planTemplateId, name, and code.
        """
        if not self.token:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        plan_url = f"{self.base_url}/organizations/{self.org_id}/plans"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        try:
            # Send the POST request to create a plan
            response = requests.post(plan_url, headers=headers, json=payload)
            response.raise_for_status()

            # Log and return the successful response
            logger.info("Plan created successfully: %s", response.json())
            return response.json()

        except requests.RequestException as e:

            status_code = response.status_code if response else "N/A"
            error_content = response.text if response else "No response content"

            # Log error details
            logger.error(
                "Failed to create plan.\n"
                "Status Code: %s\nPayload: %s\nResponse: %s\nError: %s",
                status_code, payload, error_content, str(e)
            )

            # Raise an exception with details
            raise Exception(f"Failed to create plan: {str(e)} (Status Code: {status_code})") from e

    def create_pricing(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a pricing configuration using the provided payload.
        The payload must include required fields such as aggregationId, planId, type, and pricingBands.
        """
        if not self.token:
            raise Exception("Not authenticated. Call authenticate() first.")

        pricing_url = f"{self.base_url}/organizations/{self.org_id}/pricings"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        try:
            # Send the POST request to create a pricing configuration
            response = requests.post(pricing_url, headers=headers, json=payload)
            response.raise_for_status()

            # Log and return the successful response
            logger.info("Pricing created successfully: %s", response.json())
            return response.json()

        except requests.RequestException as e:
            status_code = response.status_code if response else "N/A"
            error_content = response.text if response else "No response content"

            # Log error details
            logger.error(
                "Failed to create pricing.\n"
                "Status Code: %s\nPayload: %s\nResponse: %s\nError: %s",
                status_code, payload, error_content, str(e)
            )

            # Raise an exception with details
            raise Exception(f"Failed to create pricing: {str(e)} (Status Code: {status_code})") from e

    # Task 3
    def create_account(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates an account using the provided payload.
        The payload must include required fields such as name and code.
        """
        if not self.token:
            raise Exception("Not authenticated. Call authenticate() first.")

        account_url = f"{self.base_url}/organizations/{self.org_id}/accounts"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        try:
            # Send the POST request to create an account
            response = requests.post(account_url, headers=headers, json=payload)
            response.raise_for_status()

            # Log and return the successful response
            logger.info("Account created successfully: %s", response.json())
            return response.json()

        except requests.RequestException as e:
            status_code = response.status_code if response else "N/A"
            error_content = response.text if response else "No response content"

            # Log error details
            logger.error(
                "Failed to create account.\n"
                "Status Code: %s\nPayload: %s\nResponse: %s\nError: %s",
                status_code, payload, error_content, str(e)
            )

            # Raise an exception with details
            raise Exception(f"Failed to create account: {str(e)} (Status Code: {status_code})") from e

    def create_account_plan(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates an account plan using the provided payload.
        The payload must include required fields such as accountId, planId, startDate.....
        """
        if not self.token:
            raise Exception("Not authenticated. Call authenticate() first.")

        account_plan_url = f"{self.base_url}/organizations/{self.org_id}/accountplans"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        try:
            # Send the POST request to create an account plan
            response = requests.post(account_plan_url, headers=headers, json=payload)
            response.raise_for_status()

            # Log and return the successful response
            logger.info("Account plan created successfully: %s", response.json())
            return response.json()

        except requests.RequestException as e:
            status_code = response.status_code if response else "N/A"
            error_content = response.text if response else "No response content"

            # Log error details
            logger.error(
                "Failed to create account plan.\n"
                "Status Code: %s\nPayload: %s\nResponse: %s\nError: %s",
                status_code, payload, error_content, str(e)
            )

            # Raise an exception with details
            raise Exception(f"Failed to create account plan: {str(e)} (Status Code: {status_code})") from e

    # Task 4
    def ingest_usage(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Submits usage data to the Measurements API.
        The payload must include the 'measurements' field with necessary usage details.
        """
        if not self.token:
            raise Exception("Not authenticated. Call authenticate() first.")

        usage_url = f"{self.ingest_url}/organizations/{self.org_id}/measurements"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        try:
            # Send the POST request to submit usage data
            response = requests.post(usage_url, headers=headers, json=payload)
            response.raise_for_status()

            # Log and return the successful response
            logger.info("Usage data submitted successfully: %s", response.json())
            return response.json()

        except requests.RequestException as e:
            status_code = response.status_code if response else "N/A"
            error_content = response.text if response else "No response content"

            # Log error details
            logger.error(
                "Failed to submit usage data.\n"
                "Status Code: %s\nPayload: %s\nResponse: %s\nError: %s",
                status_code, payload, error_content, str(e)
            )

            # Raise an exception with details
            raise Exception(f"Failed to submit usage data: {str(e)} (Status Code: {status_code})") from e
