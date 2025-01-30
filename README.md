README


first activate virtual env
install requirements
go to mock_data.yaml file to update the suffix of lines that has #update next to them (such as API 2, api_2).


config.py has access_key, api_secret and org_id. This is not the correct practice for production environment but it is ok for this assignment in sandbox. There are proper ways of doing it such as using environment variables

Run task1 in main.py, comment out other tasks. Observe new yaml file created: mock_data_after_task1.yaml
also check UI for below entities

    # Product: AWS Lambda API X
    # Meter: Compute and Requests Meter API X
    # Aggregations:
    #     - Duration Aggregation API X
    #     - Total Number of Requests API X


Run task2 in main.py, comment out other tasks. Observe new yaml file created: mock_data_after_task2.yaml
also check UI for below entities. 
For Pricing, in the UI go to Pricing Editor > Choose Product: AWS Lambda API X > Add Plans > Check Lambda Plan API X > Confirm

    # Plan Template: Lambda Template API X
    # Plan: Lambda Plan API X
    # Pricing (For Pricing, go to Pricing Editor > Choose Product: AWS Lambda API X > Add Plans > Check Lambda Plan API X > Confirm)


Run task3 in main.py, comment out other tasks. Observe new yaml file created: mock_data_after_task3.yaml
also check UI for below entities. 
AccountPlans start date are set to 2024/12/1 so that December Invoices can be generated for Jan 1 (in arrears)

    # Account:
    #   - Mickey Mouse Inc API X
    #   - Donald Duck Ltd API X
    #   - Pluto LLP API X
    # AccountPlan (see attached plans for each account) 


Important: Before running task4 to ingest usage, go to the function "generate_measurements_payload" in main.py to update the aggregation names (keys) in measure field: memory_consumption_api_x, execution_time_api_x

Task 4 Generates a payload with a list of random measurements with below values.
    #   - a random uid
    #   - a random integer for memory consumption between 1 and 100
    #   - a random integer for execution time between 1000 and 5000
    #   - a random timestamp in December 2024

Once above is done, run task4 in main.py, comment out other tasks. In UI, go to Metering > Usage Data Explorer. Choose Last 90 days for Time Period and
under Meters, choose the correct Meter. Then run Perform Query to see the usage.
Task4 ingests single measurement for each account first then ingests 120 measurements in one call. You can change the size of the measurements.

Task 5: Run Billing in UI to see invoices.



