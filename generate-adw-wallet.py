# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.

import oci
import sys

# Overview of Autonomous Data Warehouse
# See: https://docs.cloud.oracle.com/iaas/Content/Database/Tasks/adbconnecting.htm

# Load the default configuration
config = oci.config.from_file()
autonomous_data_warehouse_id = "ocid1.autonomousdatabase.oc1.phx.abyhqljrsnwgtdyxfdvbraoyqyc7sgysfirwxvmk6o56vtem7p74vkig2h7a"
wallet_password = "M0n3yb0vin3@1"

def generate_wallet(db_client):
    # Create the model and generate the wallet
    # See: https://docs.cloud.oracle.com/iaas/Content/Database/Tasks/adbconnecting.htm
    wallet_generate = oci.database.models.GenerateAutonomousDatabaseWalletDetails()

    wallet_generate.password = wallet_password
    wallet_response = db_client.generate_autonomous_data_warehouse_wallet(
       autonomous_data_warehouse_id,
       generate_autonomous_data_warehouse_wallet_details=wallet_generate,
       retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY)

    


    wallet_id = wallet_response.data
    print("Created Wallet {}".format(wallet_id))
    return wallet_id
    
if __name__ == "__main__":
    # Initialize the client
    db_client = oci.database.DatabaseClient(config)

generate_wallet(db_client)

