from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name =models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Lawyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE )
    category=models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    fee= models.DecimalField(max_digits=8, decimal_places=2)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.category}"
    

class Slot(models.Model):
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    start= models.DateTimeField()
    end = models.DateTimeField()
    booked = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.lawyer.user.username}  | {self.start}"
    
class  Appointment(models.Model):
    STATUS= [
        ('booked', 'Booked'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    lawyer=models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS, default='booked')
    notes = models.TextField(blank=True, null=True)
    fee_charged = models.DecimalField(max_digits=8, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.username} → {self.lawyer.user.username} on {self.slot.start}"
     