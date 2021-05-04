import json
import os
import re
import pandas as pd
from mpu import haversine_distance
import sys
import boto3
from smart_open import smart_open


class HandleFile:

    @staticmethod
    def in_format(docfile):
        if docfile.name.split(".")[-1] != 'csv':
            return False
        else:
            file_content = docfile.open('r')
            headers = file_content.readlines()[0].decode()

            if re.search('POINT.*', headers) and re.search('LONG.*', headers) and re.search('LAT.*', headers):
                print("true")
                return True
            return False

    @staticmethod
    def calc_links(docfile, uuid):
        # Not a DEV-SERVER
        if not (len(sys.argv) > 1 and sys.argv[1] == 'runserver'):
            aws_key = os.environ['AWS_ACCESS_KEY_ID']
            aws_secret = os.environ['AWS_SECRET_ACCESS_KEY']

            bucket_name = 'calc-coord-django-files-bucket'
            object_key = docfile.name

            path = f's3://{aws_key}:{aws_secret}@{bucket_name}/{object_key}'

            df = pd.read_csv(smart_open(path))

        else:
            df = pd.read_csv(docfile.path)

        links = []
        for i in range(len(df.index)):
            for j in range(len(df.index) - i - 1):
                links.append((df["POINT"][i], df["POINT"][j + i + 1]))

        links_df = pd.DataFrame(columns=['DISTANCE'], index=pd.MultiIndex.from_tuples(links))
        for idx in links_df.index:
            lat1 = df[df["POINT"] == idx[0]]["LAT"].values[0]
            long1 = df[df["POINT"] == idx[0]]["LONG"].values[0]
            lat2 = df[df["POINT"] == idx[1]]["LAT"].values[0]
            long2 = df[df["POINT"] == idx[1]]["LONG"].values[0]

            try:
                links_df.loc[idx, "DISTANCE"] = haversine_distance((lat1, long1), (lat2, long2))

            except ValueError:
                links_df.loc[idx, "DISTANCE"] = 'N/A'

        if not (len(sys.argv) > 1 and sys.argv[1] == 'runserver'):
            aws_key = os.environ['AWS_ACCESS_KEY_ID']
            aws_secret = os.environ['AWS_SECRET_ACCESS_KEY']

            bucket_name = 'calc-coord-django-files-bucket'
            object_key = docfile.name

            path = f's3://{aws_key}:{aws_secret}@{bucket_name}/{object_key}'

            s3 = boto3.resource(service_name='s3')
            s3.meta.client.upload_file(Filename=path, Bucket='calc-coord-django-files-bucket',
                                       Key=f'links/{uuid}')

        else:
            save_to_path = f"{os.path.split(docfile.path)[0]}/links/{uuid}.csv"
            links_df.to_csv(f"{save_to_path}")

        result = links_df.to_json(orient="index")
        parsed = json.loads(result)
        return parsed
