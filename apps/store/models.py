from django.db import models
from django.utils.text import slugify

class Store(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name 

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    store = models.ForeignKey(Store, blank=True, null=True, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    handle = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.handle is None:
            self.handle = slugify(self.name)
        else:
            self.handle = slugify(self.handle)

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name