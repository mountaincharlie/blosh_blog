from . import views
from django.urls import path

urlpatterns = [
    # adding the BlogList view as the home path
    path('', views.BlogList.as_view(), name='home'),
    # the blog view opens in the blog title specific url (using slug)
    path('<slug:slug>', views.BlogView.as_view(), name='blog_view'),
]
