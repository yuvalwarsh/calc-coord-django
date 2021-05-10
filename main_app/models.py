from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
import uuid
from django.utils import timezone
from .handlefile import HandleFile
import os
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
        return HandleFile.calc_links(self.docfile, str(self.uuid))

    def delete(self, *args, **kwargs):
        bucket_name = os.environ['AWS_STORAGE_BUCKET_NAME']
        s3_resource = boto3.client("s3")

        # No links were calculated for the file
        try:
            s3_resource.delete_object(Bucket=bucket_name, Key=f'documents/links/{str(self.uuid)}.csv')

        except FileNotFoundError:
            pass

        # django-cleanup will delete the pts file
        return super(Document, self).delete(*args, **kwargs)