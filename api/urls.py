from django.urls import path

from api.views import VectorListAPIView, CreateVectorAPIView, \
    CreateOperatorAPIView, UpdateVectorAPIView, UpdateOperatorAPIView, DeleteVectorAPIView, DeleteOperatorAPIView

urlpatterns = [
    path('', VectorListAPIView.as_view(), name='vector-list'),
    path('create/vector/',
         CreateVectorAPIView.as_view(), name='create-vector'),
    path('update/vector/<int:pk>/',
         UpdateVectorAPIView.as_view(), name='update-vector'),
    path('delete/vector/<int:pk>/',
         DeleteVectorAPIView.as_view(), name='delete-vector'),
    path('create/operator/',
         CreateOperatorAPIView.as_view(), name='create-operator'),
    path('update/operator/<int:pk>/',
         UpdateOperatorAPIView.as_view(), name='update-operator'),
    path('delete/operator/<int:pk>/',
         DeleteOperatorAPIView.as_view(), name='delete-operator')
]
