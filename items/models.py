from django.db import models


class SaleProduct(models.Model):
    def __init__(self, link, name, price, price_on_sale, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name=name
        self.link=link
        self.price=price
        self.price_on_sale=price_on_sale

    link = models.URLField(primary_key=True,max_length=200)
    name = models.CharField(max_length=80)
    price = models.CharField(max_length=8)
    price_on_sale = models.CharField(max_length=8)

    def __str__(self):
        return self.link, self.name, self.price, self.price_on_sale




