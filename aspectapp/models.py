# aspectapp/models.py

from django.db import models

class Product(models.Model):
    productName = models.CharField(max_length=200)
    productReview = models.TextField()
    mallProductUrl = models.TextField()

    def __str__(self):
        return self.productName