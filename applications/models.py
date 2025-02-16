from django.db import models
from django.contrib.auth.models import User
from organizations.models import Organization

# Create your models here.
class OrganizationApplication(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, default=None)
    message = models.TextField(blank=True, default="")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.organization.name}" 