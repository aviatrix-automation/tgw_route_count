# TGW Route Count
  Python script that returns the total route cout of an AWS TGW. This script was initially forked from AWS own [repository](https://github.com/aws-samples/how-to-monitor-tgw-route-limits-using-serverless-architecture).

## Prerequisites
  * This script requires Boto3 to be installed.
  * The admin running the script should have read permissions to the TGW in question, as well as write access to a S3 bucket in the same region.

## How-to:
1. Clone this repository to your local directory:
   ```
   git clone https://github.com/aviatrix-automation/tgw_route_count.git
   cd tgw_route_count
   ```

2. Initialize a Python virtual environment and install Boto3:
   ```
   python3 -m venv tgw_route_count_venv
   source tgw_route_count_venv/bin/activate
   pip install boto3
   ```

3. Export the necessary variables and the AWS temporary credentials:
   ```
   export tgw_region="us-east-1"
   export tgw_id="tgw-01234567890"
   export s3_bucket="the-super-bucket" << it has to be in the same region

   export AWS_ACCESS_KEY_ID="ABCDEFGHWWWW"
   export AWS_SECRET_ACCESS_KEY="GoQwed12345!@#$"
   export AWS_SESSION_TOKEN="IQoJb3JpZ2luX2VjEGkaCXVzLXdlc3QtMiJHMEUCIQDw4iAjzx+"
   ```

4. Run the script and check the result:
   ```
   python ./tgw_route_count.py
   ```

## Observations:
  This script sole purpose is to check the TGW total rout count, for more information regarding the status of other TGW quota metrics, please check in the Aviatrix Controller or contact our support.
