"""vendreviex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('register/',views.register,name='register'),
    path('payment/',views.payment,name='payment'),
    path('change_pass/',views.change_pass,name='change_pass'),
    path('login/',views.user_login,name='user_login'),
    path('postad/',views.post_ad,name='user_ad'),
    path('detail/<int:id>/', views.detail, name='ad_detail'),
    path('sendmessage/<int:id>/', views.sendmessage, name='sendmessage'),
    path('adbycat/<int:id>/', views.adbycat, name='adbycat'),
    path('editad/<int:id>/', views.editad, name='editad'),
    path('logout/', views.user_logout, name='user_logout'),
    path('inbox/', views.inbox, name='inbox'),
    path('outbox/', views.outbox, name='outbox'),
    path('contact/', views.contact, name='contact'),
    path('myads/', views.mypostedads, name='mypostedads'),
    path('myads/delete/', views.deletead, name='ad_delete'),
    path('myads/update/', views.update_ad, name='ad_update'),
    path('favourite/', views.ad_favourite, name='ad_favourite'),
    path('uprofile/', views.uprofile, name='uprofile'),
    path('searchad/', views.searchad, name='searchad'),
    path('searchadbyloc/', views.searchadbyloc, name='searchadbyloc'),

]
