from django.db import  models

class SaleDetailManager(models.Manager):
    def saleDetails(self, venta_id):
        return self.filter(
            sale__id=venta_id
        ).order_by('count', 'product__name')