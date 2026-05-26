from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class expense(models.Model):
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    category=models.CharField(max_length=20)
    description=models.TextField(blank=True,null=True)
    date=models.DateField()
    owner=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="expenses"
    )

    def __str__(self):
        return self.category
class income(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.owner.username}->{self.amount}"