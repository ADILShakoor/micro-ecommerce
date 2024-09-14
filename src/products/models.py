from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.


class Product(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    name=models.CharField(max_length=120)
    handle=models.SlugField(unique=True)
    price=models.DecimalField(max_digits=10,decimal_places=2,default=9.99)
    og_price=models.DecimalField(max_digits=10,decimal_places=2,default=9.99)
    # strip_price_id=
    # stripe_price =models.IntegerField(default=999)
    price_changed_stamp=models.DateTimeField(auto_now=False,auto_now_add=False,blank=True,null=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)


    def save(self,*args,**kwargs):
        if self.price !=self.og_price:
            # price change
            self.og_price=self.price
            # triggger an API request for the price
            self.stripe_price=int(self.price*100)
            self.price_changed_stamp=timezone.now()
        super().save(*args,**kwargs)

