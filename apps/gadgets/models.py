# Django Imports
from django.db import models

class Adam(models.Model):
    ip = models.GenericIPAddressField(null=False, blank=False)
    actuation_port = models.IntegerField(null=False, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'tbl_adam'
        unique_together = ('ip', 'actuation_port')  
