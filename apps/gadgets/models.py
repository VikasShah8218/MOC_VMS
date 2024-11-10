from django.db import models

class Adam(models.Model):
    ip = models.GenericIPAddressField(null=False, blank=False)
    actuation_port = models.IntegerField(null=False, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'tbl_adam'
        unique_together = ('ip', 'actuation_port')  



class AdamLinkedwith(models.Model):
    client_ip = models.CharField(max_length=50, null=True,blank=True)
    adam = models.ForeignKey(Adam, related_name="adam", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    other = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'tbl_adam_linked_with'
        unique_together = ('client_ip', 'adam')  

    def __str__(self) -> str:
        return f"{self.name} - Client IP: {self.client_ip}"
    


