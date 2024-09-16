
from django.shortcuts import render, redirect,get_object_or_404
from .forms import ProductForm
from .models import Product

def create_product_view(request):
    context={}
    form=ProductForm(request.POST or None)
    if form.is_valid():
        obj=form.save(commit=False)
        if request.user.is_authenticated:
            obj.user=request.user
            obj.save()
            return redirect('/products/create/')
        form.add_error(None,"you must be  loggded in to enter products ")
    context['form']=form
    return render (request,'products/create.html',context)

def product_list_view(request):
    object_list=Product.objects.all()
    return render(request,"products/list.html",{"object_list":object_list})


def product_detail_view(request,handle=None):
    obj=get_object_or_404(Product,handle=handle)
    is_owner=False
    if request.user.is_authenticated:
       is_owner=obj.user==request.user
    context={"object":obj}
    if is_owner:
        form=ProductForm(request.POST or None,instance=obj)
        if form.is_valid():
            obj=form.save(commit=False)
            # if request.user.is_authenticated:
            #     obj.user=request.user
            obj.save()
            # return redirect('/products/create/')
            # form.add_error(None,"you must be  loggded in to enter products ")
        context['form']=form
    return render (request,'products/detail.html',context)