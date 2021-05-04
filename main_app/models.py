from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
import uuid
from django.utils import timezone
from .handlefile import HandleFile
import os


def content_file_name(instance, filename):
    name, ext = filename.split('.')[:-1], filename.split('.')[-1]
    filename = f'{name}_{instance.uuid}.{ext}
    return os.path.join('documents', filename)

class Document(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    docfile = models.FileField(upload_to=content_file_name)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)

    def __repr__(self):
        return f"<uuid> {self.uuid}"

    def in_format(self):
        return HandleFile.in_format(self.docfile)

    def calc_links(self):
        return HandleFile.calc_links(self.docfile, self.uuid)

    def delete(self, *args, **kwargs):
        # No links were calculated for the file
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, "documents/links", str(f"{self.uuid}.csv")))

        except FileNotFoundError:
            pass

        # no need to check because it is created by default
        os.remove(os.path.join(settings.MEDIA_ROOT, self.docfile.name))

        return super(Document, self).delete(*args, **kwargs)
