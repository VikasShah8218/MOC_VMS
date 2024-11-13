# Django Imports
from django.db import models
from apps.accounts.models import User

class Visitor(models.Model):
    class Meta:
        db_table = 'tbl_visitor'

    visitor_type_choice = [("civilian", "Civilian"),]
    gov_id_choices = [('aadhar_card', 'Aadhar_Card')]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    visitor_type = models.CharField(max_length=255,choices=visitor_type_choice,default=visitor_type_choice[0][0])
    address = models.TextField(null=False,blank=True)
    image = models.TextField(null=True,blank=True)
    gov_id_type = models.CharField(max_length=50, choices=gov_id_choices,default=gov_id_choices[0][0])
    gov_id_no = models.CharField(max_length=255, unique=True)
    is_blacklisted = models.BooleanField(default=False)
    is_pass_created = models.BooleanField(default=False)
    phone = models.CharField(max_length=20)
    face_feature = models.BinaryField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_visitors",null=True,blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="updated_visitors",null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    other = models.CharField(max_length=255,null=True,blank=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class VisitorLog(models.Model):
    class Meta:
        db_table = 'tbl_visitor_track'

    CHECKOUT_BY_CHOICES = {
        'by_system': 'By System',
        'by_receptionist': 'By Receptionist',
        'by_admin': 'By Admin',
    }

    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE,related_name="visitor_track",null=True,blank=True)
    visitor_pass = models.ForeignKey('passes.VisitorPass', on_delete=models.CASCADE,related_name="pass_track",null=True,blank=True)
    is_authorized = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class VisitorFaceFeatures(models.Model):
    class Meta:
        db_table = "tbl_visitor_face_features"
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE,related_name="visitor_face_feature",null=True,blank=True)
    feature = models.BinaryField(null=False)
    