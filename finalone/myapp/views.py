from django.shortcuts import render,redirect
from django.contrib.auth.models import  User
from .models import UserDetail,Advertise,Category,Location,Favourites,Messages
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import TemplateView, View, DeleteView
from django.http import JsonResponse
from django.conf import settings
from django.http import  HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import stripe
import json
stripe_pub=settings.STRIPE_PUBLISHABLE_KEY
stripe_private=settings.STRIPE_SECRET_KEY

stripe.api_key=stripe_private
# Create your views here.

def home(request):
    data=Advertise.objects.all()
    loc=Location.objects.all()
    catdata = Category.objects.all()
    page=request.GET.get('page',1)
    paginator=Paginator(data,16)
    try:
        data=paginator.page(page)
    except PageNotAnInteger:
        data=paginator.page(1)
    except EmptyPage:
        data=paginator.page(paginator.num_pages)
    return  render(request,'index.html',{'data':data,'catdata': catdata,'loc':loc})

def showcategories(request):
    loc = Location.objects.all()
    catdata = Category.objects.all()
    return render(request, 'header.html', { 'catdata': catdata,'loc':loc})

def inbox(request):
    loc = Location.objects.all()
    catdata = Category.objects.all()
    mdata = Messages.objects.filter(s_id=request.user.id)
    return render(request, 'inbox.html', { 'mdata': mdata,'catdata': catdata,'loc':loc})

def outbox(request):
    loc = Location.objects.all()
    catdata = Category.objects.all()
    mdata = Messages.objects.filter(r_id=request.user.id)
    return render(request, 'outbox.html', { 'mdata': mdata,'catdata': catdata,'loc':loc})

@login_required(login_url='/login/')
def uprofile(request):
    if request.method == 'POST':
        user_info = request.POST.get('user_info')
        user_fname = request.POST.get('user_fname')
        user_lname = request.POST.get('user_lname')
        user_image = request.FILES.get('user_image')
        if user_image:
            user_image = request.FILES.get('user_image')
        else:
            user_image="images/user_images/default.jpg"

        user_city = request.POST.get('user_city')
        user_phone = request.POST.get('user_phone')
        obj = UserDetail.objects.get(user=request.user.id)
        obj.user_info = user_info
        obj.user_fname = user_fname
        obj.user_lname = user_lname
        obj.user_image = user_image
        obj.user_city = user_city
        obj.user_phone = user_phone
        obj.save()
        udata = UserDetail.objects.get(user=request.user)
        loc = Location.objects.all()
        return render(request, 'profile.html', {'u': udata,'catdata':Category.objects.all(),'loc':loc,'success':'Profile updated Sucessfully'})
    else:
        udata = UserDetail.objects.get(user=request.user)
        loc = Location.objects.all()
        return render(request, 'profile.html', {'u': udata,'catdata':Category.objects.all(),'loc':loc})

def register(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email = request.POST.get('email_id')
        password = request.POST.get('password')
        user=User.objects.create_user(username,email,password)
        data=UserDetail(user=user)
        print(username)
        data.save()
        return  redirect('user_login')
    else:

        return  render(request,'register.html',{'catdata':Category.objects.all(),'loc':Location.objects.all()})


def user_login(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user:
            auth_login(request,user)
            return redirect('uprofile')
        else:
            return render(request, 'login.html', {'catdata': Category.objects.all(), 'loc': Location.objects.all(),'error':'Invalid Username / Password'})
    else:
        return  render(request,'login.html',{'catdata':Category.objects.all(),'loc':Location.objects.all()})


@login_required(login_url='/login/')
def post_ad( request ):

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('details')
        contact = request.POST.get('contact')
        price = request.POST.get('price')
        image = request.FILES.get('postimage')
        image1 = request.FILES.get('postimage1')
        image2 = request.FILES.get('postimage2')
        location = request.POST.get('location')
        category = request.POST.get('category')
        object=Advertise(user=request.user.id,title=title,description=description,image=image,image1=image1,image2=image2,location=Location.objects.get(pk=location),contact=contact,price=price,categories=Category.objects.get(pk=category))
        object.save()
        return redirect('mypostedads')
    else:
        return render(request, 'postad.html',{
            'category':Category.objects.all(),
            'location': Location.objects.all(),
            'loc': Location.objects.all(),
            'catdata': Category.objects.all(),
        })

@login_required(login_url='/login/')
def editad(request ,id=None):

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('details')
        contact = request.POST.get('contact')
        price = request.POST.get('price')
        image = request.FILES.get('postimage')
        image1 = request.FILES.get('postimage1')
        image2 = request.FILES.get('postimage2')
        location = request.POST.get('location')
        category = request.POST.get('category')
        addata = Advertise.objects.get(pk=id)
        addata.user=request.user.id
        addata.title=title
        addata.description=description
        addata.image=image
        addata.image1=image1
        addata.image2=image2
        addata.contact=contact
        addata.price=price
        addata.categories=Category.objects.get(pk=category)
        addata.location=Location.objects.get(pk=location)
        addata.save()
        return redirect('mypostedads')
    else:
        addata= Advertise.objects.get(pk=id)
        return render(request, 'editad.html',{
            'category':Category.objects.all(),
            'location': Location.objects.all(),
            'loc': Location.objects.all(),
            'catdata': Category.objects.all(),
            'ad':addata
        })

@login_required(login_url='/login/')
def sendmessage( request,id ):

    if request.method == 'POST':
        addata = Advertise.objects.get(pk=id)
        sid=addata.user
        ad_id=addata.id
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        object=Messages(r_id=User.objects.get(pk=request.user.id),s_id=User.objects.get(pk=sid),message=message,subject=subject,ad_id=Advertise.objects.get(pk=ad_id))
        object.save()
        return redirect('outbox')
    else:
        addata = Advertise.objects.get(pk=id)
        return render(request, 'ad_detail.html', {'ad': addata})

def detail(request,id=None):
    addata=Advertise.objects.get(pk=id)
    relateddata=Advertise.objects.filter(categories=addata.categories)
    return  render(request,'ad_detail.html',{'ad':addata,'relateddata':relateddata,'catdata':Category.objects.all(),'loc':Location.objects.all()})

def payment(request):
    return  render(request,'payment.html',{'key':stripe_pub})


def adbycat(request,id=None):
    resdata=Advertise.objects.filter(categories=id)
    return  render(request,'adbycat.html',{'adcat':resdata,'catdata':Category.objects.all(),'loc':Location.objects.all()})

@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return  redirect('home')

def contact(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        send_mail("foo", "bar", settings.EMAIL_HOST_USER,[ "snehshine@gmail.com"] )
        return render(request, 'contact.html')
    else :
        return  render(request,'contact.html',{'catdata':Category.objects.all(),'loc':Location.objects.all()})

def mypostedads(request):
    print(request.user.id,"id")
    ads = Advertise.objects.filter(user=request.user.id)
    category= Category.objects.all()
    location= Location.objects.all()
    return render(request, 'mypostedads.html', { 'ads': ads,  'category':category,'location':location,'catdata':Category.objects.all(),'loc':Location.objects.all()})


def  deletead( request):
    id1 = request.GET.get('id', None)
    Advertise.objects.get(id=id1).delete()
    data = {
        'deleted': True
    }
    return JsonResponse(data)

def  ad_favourite( request):
    ad_id = request.GET.get('ad_id', None)
    user_id = request.GET.get('user_id', None)

    count = Favourites.objects.filter(ad_id=ad_id, user_id=user_id).count()
    if count == 1:
        obj = Favourites.objects.get(ad_id=ad_id, user_id=user_id).delete()
        data = {
            'result': False
        }
    else:
        obj = Favourites.objects.create(
            ad_id=ad_id,
            user_id=user_id
        )
        data = {
            'result': True
        }

    return JsonResponse(data)
def update_ad(request):
    id1 = request.POST.get('id', None)
    title = request.POST.get('title', None)
    loc = request.POST.get('loc', None)
    price = request.POST.get('price', None)
    print(loc)
    obj = Advertise.objects.get(id=id1)
    obj.title = title
    '''obj.location = Location.objects.get(pk=loc) '''
    obj.location = loc
    obj.price = price
    obj.save()
    ad = {'id':obj.id,'title':obj.title,'loc':obj.location,'price':obj.price}
    data = {
        'ad': ad
    }
    return JsonResponse(data)

@login_required(login_url='/login/')
def change_pass(request):
    if request.method=='POST':
        id=request.user.id;
        data=User.objects.get(pk=id)
        data.set_password(request.POST.get('new_pass1'))
        data.save()
        return render(request, 'change_pass.html', {'catdata': Category.objects.all(), 'loc': Location.objects.all(),'success':'Password Changed Sucessfully'})
    else:
        return  render(request,'change_pass.html',{'catdata':Category.objects.all(),'loc':Location.objects.all()})

def  searchad(request):
    if request.method == 'POST':
        title = request.POST.get('txtsearch')
        if title=="":
            search_items=""
            return render(request, 'searchad.html', {'addata': {},'catdata':Category.objects.all(),'loc':Location.objects.all()})
        elif title:
            search_items = Advertise.objects.filter(title=title)
            return render(request, 'searchad.html', {'addata': search_items,'catdata':Category.objects.all(),'loc':Location.objects.all()})
        else:
            return render(request, 'searchad.html', {'addata': {},'catdata':Category.objects.all(),'loc':Location.objects.all()})
    else:
        return render(request, 'searchad.html', {'addata': {},'catdata':Category.objects.all(),'loc':Location.objects.all()})

def  searchadbyloc(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        if location=="":
            search_items=""
            return render(request, 'searchadbyloc.html', {'addata': {},'catdata':Category.objects.all(),'loc':Location.objects.all()})
        elif location:
            search_items = Advertise.objects.filter(location=location)
            return render(request, 'searchadbyloc.html', {'addata': search_items,'catdata':Category.objects.all(),'loc':Location.objects.all()})
        else:
            return render(request, 'searchadbyloc.html', {'addata': {},'catdata':Category.objects.all(),'loc':Location.objects.all()})
    else:
        return render(request, 'searchadbyloc.html', {'addata': {},'catdata':Category.objects.all(),'loc':Location.objects.all()})

