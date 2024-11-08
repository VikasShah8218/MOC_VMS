from django.db import models
from apps.accounts.models import User
from apps.visitor.models import Visitor

class VisitorPass(models.Model):
    class Meta:
        db_table = 'tbl_passes'

    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE,related_name="visitor",null=False,blank=False)
    valid_until = models.DateTimeField(null=False)
    pass_number = models.IntegerField(unique=True,blank=False)
    visiting_purpose = models.TextField(null=False,blank=True)
    whom_to_visit = models.CharField(max_length=255, null=False,blank=True)
    visiting_department = models.CharField(max_length=255, null=False,blank=True)
    pass_note = models.CharField(max_length=255, null=False,blank=True)
    is_cancelled = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_passes",null=True,blank=True)
    updated_by = models.ForeignKey(User, related_name="updated_passes", on_delete=models.CASCADE,null=True,blank=True)


    def __str__(self) -> str:
        return f"{self.visitor}"
