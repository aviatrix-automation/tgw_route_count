# This script was initially forked from:
# https://github.com/aws-samples/how-to-monitor-tgw-route-limits-using-serverless-architecture

# USAGE:
# First make sure boto3 is installed.
# Then just export these three variables as environmental before running the script.
#
# export tgw_region="us-east-1"
# export tgw_id="tgw-01234567890"
# export s3_bucket="the-super-bucket" << it has to be in the same region
#
# export AWS_ACCESS_KEY_ID="ABCDEFGHWWWW"
# export AWS_SECRET_ACCESS_KEY="GoQwed12345!@#$"
# export AWS_SESSION_TOKEN="IQoJb3JpZ2luX2VjEGkaCXVzLXdlc3QtMiJHMEUCIQDw4iAjzx+"


import boto3
import json
import os
import sys
from datetime import datetime

# Initializing boto3 clients used in this function.
tgw_region =  os.environ['tgw_region']
tgw_id = os.environ['tgw_id']
s3_bucket = os.environ['s3_bucket']
ec2 = boto3.client('ec2', region_name = tgw_region )
s3 = boto3.client('s3', region_name = tgw_region )
count = [ ]


def main():

    # Getting all the TGW route tables in the account.
    print ("\n >>", datetime.now(), ": Getting all the route tables from the TGW", tgw_id + ":\n")
    response_1 = ec2.describe_transit_gateway_route_tables(
            Filters = [
                {
                    'Name': 'transit-gateway-id',
                    'Values': [ tgw_id ]
                    }
                ],
    )
    print ( datetime.now(), ": ",  response_1)

    # Exist if TGW does not exist or not found.
    if (len (response_1['TransitGatewayRouteTables']) == 0):
        print ("\n >>", datetime.now(), ": The selected TGW was not found or does not exist.\n")
        sys.exit()

    # Exporting all the routes to the S3 bucket specified earlier in the code. The json output files will be
    # stored in /VPCTransitGateway/TransitGatewayRouteTables/ folder.
    print ("\n >>", datetime.now(), ": Exporting all the routes to the S3 bucket", s3_bucket + ":\n")
    for i in range (len (response_1['TransitGatewayRouteTables'])):
        response_2 = ec2.export_transit_gateway_routes(
            TransitGatewayRouteTableId = response_1['TransitGatewayRouteTables'][i]['TransitGatewayRouteTableId'],
            S3Bucket = s3_bucket
            )
        print ( datetime.now(), ": ",  response_2)

    # Extracting json file name with path from output of route export API call.
        object_name_split = response_2['S3Location'].split("//")
        objects_path = object_name_split[1].split("/")
        object = objects_path[1] + "/" + objects_path[2] + "/" + objects_path[3]

    # Downloading json file to /tmp to be processed by Lambda function.
        s3.download_file(s3_bucket, object, './tgw_rts.json')

    # Extracting the columns calculate total number of routes, regardless of status or next-hop.
        with open('./tgw_rts.json') as f:
            records = json.load(f)
            count.append(len(records['routes']))

    # Deleting all S3 objects that were created by the script.
    all_objects = objects_path[1] + "/" + objects_path[2] + "/"
    print ("\n >>", datetime.now(), ": Deleting all objects from the path " + all_objects + " of the S3 bucket " + s3_bucket + ":\n")
    response_3 = s3.list_objects_v2(Bucket = s3_bucket, Prefix = all_objects)
    for file in response_3['Contents']:
        s3.delete_object(Bucket = s3_bucket, Key = file['Key'])
        print( datetime.now(), ": Deleting " + file['Key'])
    os.remove('./tgw_rts.json')

    # Print the grand total.
    print ("\n >>", datetime.now(), ": The TGW " + tgw_id + " (located in " + tgw_region + ") total route count is: ", sum(count), "<< \n")

if __name__ == "__main__":
    main()
