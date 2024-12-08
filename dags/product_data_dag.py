from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from airflow.utils.dates import days_ago
import requests
import json

POSTGRES_CONN_ID='postgres_default'
API_CONN_ID='open_product_api'

default_args={
    'owner':'airflow',
    'depends_on_past':False,
    'retries':3,
    'start_date':days_ago(1)
}

## DAG
with DAG(dag_id='product_etl_pipeline',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dags:
    
    @task()
    def extract_product_data():

        # Use HTTP Hook to get connection details from Airflow connection
        http_hook=HttpHook(http_conn_id=API_CONN_ID,method='GET')

        ## Build the API endpoint
        ## https://api.restful-api.dev/objects
        endpoint = "/objects"

        ## Make the request via the HTTP Hook
        response=http_hook.run(endpoint)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch product data: {response.status_code}")
        
    @task()
    def transform_product_data(products_data):
        """Transform the extracted product data."""
        transformed_data = []
        for item in products_data:
            record = {
                "id": item.get("id", None),
                "name": item.get("name", None),
            }
            data_details = item.get("data", {})
            if data_details is None:
                data_details = {}
            
            # Adding all potential keys
            record.update({
                "color": data_details.get("Color", None),
                "capacity": data_details.get("Capacity", None),
                "capacity_gb": data_details.get("Capacity GB", None),
                "price": data_details.get("price", None),
                "generation": data_details.get("Generation", None),
                "year": data_details.get("year", None),
                "strap_colour": data_details.get("Strap Colour", None),
                "case_size": data_details.get("Case Size", None),
                "cpu_model": data_details.get("CPU model", None),
                "hard_disk_size": data_details.get("Hard disk size", None),
                "description": data_details.get("Description", None),
                "screen_size": data_details.get("Screen size", None),
            })
            transformed_data.append(record)
        return transformed_data
           
    @task()
    def load_product_data(transformed_datas):
        """Load transformed data into PostgreSQL."""
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()
        # Create table if it doesn't exist
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS products (
                                    id INT,
                                    name VARCHAR(255),
                                    color VARCHAR(255),
                                    capacity VARCHAR(255),
                                    capacity_gb INT,
                                    price DECIMAL(10, 2),
                                    generation VARCHAR(255),
                                    year INT,
                                    strap_colour VARCHAR(255),
                                    case_size VARCHAR(255),
                                    cpu_model VARCHAR(255),
                                    hard_disk_size VARCHAR(255),
                                    description VARCHAR(255),
                                    screen_size DECIMAL(5, 2)
                                )
            """)

        for transformed_data in transformed_datas:
            
            
            # Insert transformed data into the table
            cursor.execute("""
                                INSERT INTO products (
                                    id, 
                                    name, 
                                    strap_colour, 
                                    case_size, 
                                    color, 
                                    capacity, 
                                    price, 
                                    generation, 
                                    year, 
                                    cpu_model, 
                                    hard_disk_size, 
                                    description, 
                                    screen_size
                                )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
            transformed_data['id'],
            transformed_data['name'],
            transformed_data.get('strap_colour', None),
            transformed_data.get('case_size', None),
            transformed_data.get('color', None),
            transformed_data.get('capacity', None),
            transformed_data.get('price', None),
            transformed_data.get('generation', None),
            transformed_data.get('year', None),
            transformed_data.get('cpu_model', None),
            transformed_data.get('hard_disk_size', None),
            transformed_data.get('description', None),
            transformed_data.get('screen_size', None)
                    ))

        conn.commit()
        cursor.close()

    ## DAG Worflow- ETL Pipeline
    product_data= extract_product_data()
    transformed_data=transform_product_data(product_data)
    load_product_data(transformed_data)

        
    




    

