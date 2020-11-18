from django.db import models

# Create your models here.
class users(models.Model):
    name=models.CharField(max_length=150,null=False)
    mobile_no=models.CharField(max_length=20,primary_key=True)
    ldap_email=models.CharField(max_length=60,null=True)
    ldap_pass=models.CharField(max_length=250,null=True)
    cse_email = models.CharField(max_length=60,null=True)
    cse_email_pass = models.CharField(max_length=250,null=True)
    moodle_id = models.CharField(max_length=60,null=True)
    moodle_pass = models.CharField(max_length=250,null=True)

    def __str__(self):
        return self.name

