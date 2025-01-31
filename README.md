
### **Instructions**

1. **Install Requirements**  
   Run the following command to install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

2. **Update Mock Data**  
   Navigate to the `mock_data.yaml` file and update the suffix for any lines marked with `#update` (e.g., `API 2`, `api_2`). This is to ensure unique names for each run.
   The suffix is set to "API 6". You can do the first run without updating this file.

3. ** API Credentials**  
   In `config.py`, you'll find `access_key`, `api_secret`, and `org_id`.
   This file will be provided in the email. Make sure it is in the root directory.


---

### **Task Instructions**

#### **Task 1: Product, Meter, and Aggregations Setup**
- In `main.py`, run **Task 1** by uncommenting its section and commenting out other tasks.
- After execution, a new YAML file (`mock_data_after_task1.yaml`) will be created.
- Verify the following entities in the UI:

  - **Product**: AWS Lambda API X  
  - **Meter**: Compute and Requests Meter API X  
  - **Aggregations**:
    - Duration Aggregation API X  
    - Total Number of Requests API X  

---

#### **Task 2: Plan and Pricing Setup**
- In `main.py`, run **Task 2**, commenting out other tasks.
- After execution, a new YAML file (`mock_data_after_task2.yaml`) will be created.
- Verify the following entities in the UI.  
 
  - **Plan Template**: Lambda Template API X  
  - **Plan**: Lambda Plan API X  
  - **Pricing**: (In UI, go to **Pricing Editor** > Choose Product: **AWS Lambda API X** > Add Plans > Check **Lambda Plan API X** > **Confirm**)

---

#### **Task 3: Account and AccountPlan Setup**
- In `main.py`, run **Task 3**, commenting out other tasks.
- After execution, a new YAML file (`mock_data_after_task3.yaml`) will be created.
- Verify the following entities in the UI:  

  **AccountPlans** start date is set to **2024/12/01**, allowing December invoices to be generated on January 1 (in arrears).

  - **Account**:
    - Mickey Mouse Inc API X  
    - Donald Duck Ltd API X  
    - Pluto LLP API X  
  - **AccountPlan**: In UI, see Attached Plans at Account view  

---

#### **Task 4: Ingest Usage Data**
- **Important**: Before running Task 4, go to the `generate_measurements_payload` function in `main.py` and update the aggregation names (keys) in the `measure` field:
  - `memory_consumption_api_x`
  - `execution_time_api_x`

- **Task 4 Overview**:
  - This task generates a payload with a list of random measurements, including:
    - A random **uid**
    - A random integer for **memory consumption** between **1** and **100**
    - A random integer for **execution time** between **1000** and **5000**
    - A random timestamp within **December 2024**

- Once function generate_measurements_payload updated, run **Task 4** by commenting out other tasks.
  
- In the UI, go to **Metering > Usage Data Explorer**:
  - Choose **Last 90 days** for the Time Period.
  - Select the correct **Meter** and click **Perform Query** to see the usage.

- **Task 4 Process**:
  - The script ingests a single measurement for each account first.
  - It then ingests **120 measurements** in one call.  
    > You can modify the number of measurements by adjusting the payload size.

---

#### **Task 5: Billing and Invoice Generation**
- Run **Billing** in the UI to generate and view invoices.
- Invoice Date: 01 / 01 / 2025. Usage is posted for December

---

