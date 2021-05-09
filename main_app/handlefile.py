import json
import os
import re
from io import StringIO
import pandas as pd
from mpu import haversine_distance
import sys
import boto3
from smart_open import smart_open
import random as r


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
        links_exist = False

        # Not a DEV-SERVER
        if not (len(sys.argv) > 1 and sys.argv[1] == 'runserver'):
            aws_key = os.environ['AWS_ACCESS_KEY_ID']
            aws_secret = os.environ['AWS_SECRET_ACCESS_KEY']

            bucket_name = 'calc-coord-django-files-bucket'
            object_key = os.path.split(docfile.name)[-1]

            pts_path = f's3://{aws_key}:{aws_secret}@{bucket_name}/documents/{object_key}'
            links_path = f's3://{aws_key}:{aws_secret}@{bucket_name}/documents/links/{uuid}.csv'

            df = pd.read_csv(smart_open(pts_path))

            # try:
            #     links_df = pd.read_csv(smart_open(links_path), index_col=[0, 1])
            #     links_df.fillna('N/A', inplace=True)
            #     links_exist = True
            #
            # except FileNotFoundError:
            #     links_exist = False

        else:
            df = pd.read_csv(docfile.path)

            if os.path.isfile(f'{os.path.split(docfile.path)[0]}/links/{uuid}.csv'):
                # no need to calculate links again
                print("LINKS EXISTS")
                links_exist = True
                links_df = pd.read_csv(f'{os.path.split(docfile.path)[0]}/links/{uuid}.csv', index_col=[0, 1, 2])
                links_df.fillna('N/A', inplace=True)

        if not links_exist:
            links = []
            for i in range(len(df.index)):
                for j in range(len(df.index) - i - 1):
                    # random will handle end-case of non-unique point column (index)
                    links.append((r.random(), df["POINT"][i], df["POINT"][j + i + 1]))

            links_df = pd.DataFrame(columns=['DISTANCE'], index=pd.MultiIndex.from_tuples(links))
            for idx in links_df.index:
                lat1 = df[df["POINT"] == idx[1]]["LAT"].values[0]
                long1 = df[df["POINT"] == idx[1]]["LONG"].values[0]
                lat2 = df[df["POINT"] == idx[2]]["LAT"].values[0]
                long2 = df[df["POINT"] == idx[2]]["LONG"].values[0]

                try:
                    links_df.loc[idx, "DISTANCE"] = haversine_distance((lat1, long1), (lat2, long2))

                except ValueError:
                    links_df.loc[idx, "DISTANCE"] = 'N/A'

            if not (len(sys.argv) > 1 and sys.argv[1] == 'runserver'):
                bucket_name = 'calc-coord-django-files-bucket'
                object_key = uuid

                csv_buffer = StringIO()
                links_df.to_csv(csv_buffer, compression='gzip')
                print(links_df)

                s3_resource = boto3.resource('s3')
                s3_resource.Object(bucket_name, f'documents/links/{uuid}.csv').put(Body=csv_buffer.getvalue())

            else:
                print(links_df.index)
                save_to_path = f"{os.path.split(docfile.path)[0]}/links/{uuid}.csv"
                links_df.to_csv(f"{save_to_path}")

        # hadn't we called the random method - in non-unique index a value error would have been raised
        result = links_df.to_json(orient="index")
        parsed = json.loads(result)
        return parsed

    @staticmethod
    def get_links_url_by_uuid(docfile, uuid):
        aws_key = os.environ['AWS_ACCESS_KEY_ID']
        aws_secret = os.environ['AWS_SECRET_ACCESS_KEY']

        bucket_name = 'calc-coord-django-files-bucket'

        s3 = boto3.client('s3', aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)

        s3.download_file(bucket_name, f'documents/links/{uuid}.csv', f'/Users/username/Desktop/links_{uuid}.csv')