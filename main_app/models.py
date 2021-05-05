from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
import uuid
from django.utils import timezone
from .handlefile import HandleFile
import os
import sys
import boto3


def content_file_name(instance, filename):
    name, ext = filename.split('.')[:-1], filename.split('.')[-1]
    filename = f'{name}_{instance.uuid}.{ext}'
    return os.path.join('documents', filename)


class Document(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    docfile = models.FileField(upload_to=content_file_name)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)

    def __repr__(self):
        return f"<uuid> {self.uuid}, <path> {self.docfile.name}"

    def in_format(self):
        return HandleFile.in_format(self.docfile)

    def calc_links(self):
        return HandleFile.calc_links(self.docfile, self.uuid)

    def delete(self, *args, **kwargs):
        # Not a DEV-SERVER
        if not (len(sys.argv) > 1 and sys.argv[1] == 'runserver'):
            aws_key = os.environ['AWS_ACCESS_KEY_ID']
            aws_secret = os.environ['AWS_SECRET_ACCESS_KEY']

            bucket_name = 'calc-coord-django-files-bucket'

            session = boto3.Session(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret)

            path_links = f's3://{bucket_name}/documents/links'
            path_pts = f's3://{bucket_name}/documents'

            s3 = session.resource("s3")

            # No links were calculated for the file
            try:
                obj = s3.Object(bucket_name, f'{path_links}/{self.uuid}')
                obj.delete()

            except FileNotFoundError:
                pass

            # no need to check because it is created by default
            obj = s3.Object(bucket_name, f'{path_pts}/{self.docfile.name}_{self.uuid}')
            obj.delete()

        # RUN LOCALLY
        else:
            # No links were calculated for the file
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT, "documents/links", str(f"{self.uuid}.csv")))

            except FileNotFoundError:
                pass

            # no need to check because it is created by default
            os.remove(os.path.join(settings.MEDIA_ROOT, self.docfile.name))

        return super(Document, self).delete(*args, **kwargs)

