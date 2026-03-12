from django.db import models

# Use your ORIGINAL Booking model (keep existing data)
class Booking(models.Model):
    first_name = models.CharField(max_length=200)    
    last_name = models.CharField(max_length=200)
    guest_number = models.IntegerField()
    comment = models.CharField(max_length=1000)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

# Menu model
class Menu(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', null=True, blank=True)

    def __str__(self):
        return self.name