from django.db import models
from django.dispatch import receiver
from django_project.main_app.models import Document


@receiver(models.signals.post_delete, sender=Document)
def remove_file_from_s3(sender, instance, using, **kwargs):
    instance.docfile.delete(save=False)