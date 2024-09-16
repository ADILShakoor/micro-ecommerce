from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone

# Create your models here.
PROTECTED_MEDIA_ROOT= settings.PROTECTED_MEDIA_ROOT
protected_storage = FileSystemStorage(location=str(PROTECTED_MEDIA_ROOT))

class Product(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='products/',blank=True,null=True)
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

    def get_absolute_url(self):
        return f"/products/{self.handle}/"


def handel_product_attachment_upload(instance,filename):
    return f"products/{instance.product.handle}/attachements/{filename}"

class ProductAttachment(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    file= models.FileField(upload_to=handel_product_attachment_upload,storage=protected_storage)
    # handle=models.SlugField(unique=True)
    is_free=models.BooleanField(default=False)
    active=models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)
