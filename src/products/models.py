import pathlib
import stripe
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from cfehome.env import config



STRIPE_SECRIT_KEY=config("STRIPE_SECRIT_KEY",default=None)
stripe.api_key=STRIPE_SECRIT_KEY

# Create your models here.
PROTECTED_MEDIA_ROOT= settings.PROTECTED_MEDIA_ROOT
protected_storage = FileSystemStorage(location=str(PROTECTED_MEDIA_ROOT))

class Product(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    strip_product_id=models.CharField(max_length=220,blank=True,null=True)
    image=models.ImageField(upload_to='products/',blank=True,null=True)
    name=models.CharField(max_length=120)
    handle=models.SlugField(unique=True)
    price=models.DecimalField(max_digits=10,decimal_places=2,default=9.99)
    og_price=models.DecimalField(max_digits=10,decimal_places=2,default=9.99)
    stripe_price =models.IntegerField(default=999)
    stripe_price_id=models.CharField(max_length=220,blank=True,null=True)
    price_changed_stamp=models.DateTimeField(auto_now=False,auto_now_add=False,blank=True,null=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)

    @property
    def display_name(self):
        return self.name
    @property
    def display_price(self):
        return self.price

    def __str__(self) -> str:
        return self.display_name
    
    def save(self,*args,**kwargs):
        if self.name:
            stripe_product_r=stripe.Product.create(name=self.name)
            self.strip_product_id=stripe_product_r.id
        if not self.stripe_price_id:
            stripe_price_obj=stripe.Price.create(
                product=self.strip_product_id,
                unit_amount=self.stripe_price,
                currency='usd'
             )
            self.stripe_price_id=stripe_price_obj.id

        if self.price !=self.og_price:
            # price change
            self.og_price=self.price
            # triggger an API request for the price
            self.stripe_price=int(self.price*100)
            if self.strip_product_id:
                stripe_price_obj=stripe.Price.create(
                product=self.strip_product_id,
                unit_amount=self.stripe_price,
                currency='usd'
             )
                self.stripe_price_id=stripe_price_obj.id
            self.price_changed_stamp=timezone.now()
        super().save(*args,**kwargs)

    def get_absolute_url(self):
       return reverse("products:detail", kwargs={"handle":self.handle})
        # return f"/products/{self.handle}/"
    def get_manage_url(self):
       return reverse("products:manage", kwargs={"handle":self.handle})


def handel_product_attachment_upload(instance,filename):
    return f"products/{instance.product.handle}/attachements/{filename}"

class ProductAttachment(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    file= models.FileField(upload_to=handel_product_attachment_upload,storage=protected_storage)
    name=models.CharField(max_length=120,null=True,blank=True)
    # handle=models.SlugField(unique=True)
    is_free=models.BooleanField(default=False)
    active=models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)

    def save(self,*args,**kwargs):
        if not self.name:
            self.name=pathlib.Path(self.file.name).name  #stem, suffix for extention get
        super().save(*args,**kwargs)
    
    @property
    def display_name(self):
        return self.name or pathlib.Path(self.file.name).name 
    
    def get_download_url(self):
        return reverse("products:download", kwargs={"handle":self.product.handle, "pk":self.pk})
