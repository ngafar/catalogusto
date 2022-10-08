from django.db import models
from django.utils.text import slugify

class Store(models.Model):
    name = models.CharField(max_length=255)
    currency = models.CharField(max_length=3, default='usd')
    stripe_secret_key = models.CharField(max_length=55)
    
    def save(self, *args, **kwargs):
        self.currency = lower(self.currency)
        super(Store, self).save(*args, **kwargs)

    def __str__(self):
        return self.name 

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    variants = models.ManyToManyField('Variant', blank=True, related_name='product_variants')
    store = models.ForeignKey(Store, blank=True, null=True, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    handle = models.CharField(max_length=255, blank=True, null=True)
    stripe_prod_id = models.CharField(max_length=55, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.handle is None:
            self.handle = slugify(self.name)
        else:
            self.handle = slugify(self.handle)

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Variant(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    stripe_prod_id = models.CharField(max_length=55, blank=True, null=True)

    def __str__(self):
        return self.name