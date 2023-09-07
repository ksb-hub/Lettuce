from django.db import models
from aspectapp.models import Product

class ComparisonResult(models.Model):
    product1 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comparisons_as_product1')
    product2 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comparisons_as_product2')
    aspect = models.CharField(max_length=20)
    recommendation = models.TextField()

    def __str__(self):
        return f"{self.product1} vs {self.product2} - {self.aspect}"