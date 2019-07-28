from django.urls import path, include
from profiles_api import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
router.register('profile', views.UserProfileViewSet)#No need base_name here since framework can deduce from model used in queryset defined in views.
router.register('feed', views.UserProfileFeedViewSet)

urlpatterns = [
    path('hello-view/', views.HelloAPIView.as_view()),
    path('login/', views.UserLoginApiView.as_view()),
    path('',include(router.urls)),#include all generated urls here
]
