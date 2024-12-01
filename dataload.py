def save_to_snowflake(table_name, data):
    """
    Save data to Snowflake. Replace with actual Snowflake insert logic.
    """
    import snowflake.connector

    # Snowflake connection parameters (replace with your details)
    conn_params = {
        'user': 'your_username',
        'password': 'your_password',
        'account': 'your_account',
        'database': 'your_database',
        'schema': 'your_schema'
    }

    try:
        # Connect to Snowflake
        conn = snowflake.connector.connect(**conn_params)
        cursor = conn.cursor()

        # Generate insert query based on table name
        if table_name == "product_info":
            query = """
                INSERT INTO product_info (
                    product_name, version, launch_date, status,
                    product_properties, retirement_date, description,
                    risks, additional_properties, documentation_url,
                    repository_url, metrics_dashboard
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        elif table_name == "business_value":
            query = """
                INSERT INTO business_value (
                    decision_making, monetization, time_savings,
                    reporting, processes, collaboration, documentation_audits
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        elif table_name == "product_owners":
            query = """
                INSERT INTO product_owners (
                    name, zid, email, type, valid_from, valid_to
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """
        elif table_name == "snowflake_data_sources":
            query = """
                INSERT INTO snowflake_data_sources (
                    database_name, schema_name, table_name, data_type,
                    valid_from, valid_to
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """
        elif table_name == "other_data_sources":
            query = """
                INSERT INTO other_data_sources (
                    dataset_name, dataset_description, data_type,
                    dataset_type, valid_from, valid_to
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """
        elif table_name == "platforms":
            query = """
                INSERT INTO platforms (
                    platform_name, platform_description, valid_from, valid_to
                ) VALUES (%s, %s, %s, %s)
            """
        else:
            raise ValueError(f"Unknown table: {table_name}")

        # Execute insert query for each row of data
        for record in data:
            cursor.execute(query, tuple(record.values()))

        # Commit transaction
        conn.commit()
        return "Success"
    except Exception as e:
        print(f"Error saving to {table_name}: {e}")
        return "Failed"
    finally:
        cursor.close()
        conn.close()


# Example data for testing the function
data_store = {
    "product_info": {
        "product_name": "Test Product",
        "version": "1.0",
        "launch_date": "2023-01-01",
        "status": "Active",
        "product_properties": "AI, GUI",
        "retirement_date": "9999-12-31",
        "description": "Sample description",
        "risks": "Sample risks",
        "additional_properties": "Sample additional properties",
        "documentation_url": "http://example.com/doc",
        "repository_url": "http://example.com/repo",
        "metrics_dashboard": "http://example.com/dashboard",
    },
    "business_value": {
        "decision_making": 8,
        "monetization": 9,
        "time_savings": 7,
        "reporting": 6,
        "processes": 5,
        "collaboration": 9,
        "documentation_audits": 8,
    },
    "product_owners": [
        {
            "name": "John Doe",
            "zid": "123456",
            "email": "john.doe@xyz.com",
            "type": "Owner",
            "valid_from": "2023-01-01",
            "valid_to": "9999-12-31",
        }
    ],
    "snowflake_data_sources": [
        {
            "database_name": "DB1",
            "schema_name": "SCHEMA1",
            "table_name": "TABLE1",
            "data_type": "Source",
            "valid_from": "2023-01-01",
            "valid_to": "9999-12-31",
        }
    ],
    "other_data_sources": [
        {
            "dataset_name": "Dataset1",
            "dataset_description": "Sample dataset",
            "data_type": "Source",
            "dataset_type": "Source",
            "valid_from": "2023-01-01",
            "valid_to": "9999-12-31",
        }
    ],
    "platforms": [
        {
            "platform_name": "Platform1",
            "platform_description": "Sample platform",
            "valid_from": "2023-01-01",
            "valid_to": "9999-12-31",
        }
    ],
}

# Call save_to_snowflake for each table
for table, data in data_store.items():
    if isinstance(data, list):  # Handle list data for subforms
        save_to_snowflake(table, data)
    elif isinstance(data, dict):  # Handle single record data
        save_to_snowflake(table, [data])
