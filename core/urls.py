from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter
from django.urls import include,path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import CustomTokenObtainPairView,UserUpdateView,ProfileView


routers = DefaultRouter()
routers.register('signup',UserViewSet,basename='signup')
routers.register('user',UserUpdateView,basename='user')
routers.register('profile',ProfileView,basename='profile')

urlpatterns = [
    path('',include(routers.urls)),
    path(r'login/',CustomTokenObtainPairView.as_view(),name='login'),
    path(r'refresh_token/',TokenRefreshView.as_view(),name='refresh_token')
]



