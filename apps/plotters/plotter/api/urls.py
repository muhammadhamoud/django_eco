from django.urls import path, include
from .views import *

urlpatterns = [

    path('applications/', ApplicationListView.as_view(), name='application-list'),
    path('bodies/', BodyListView.as_view(), name='body-list'),
    path('makes/', MakeListView.as_view(), name='make-list'),

    path('models/<int:make_id>/', ModelsListView.as_view(), name='model-list'),
    path('trims/<int:model_id>/', TrimsListView.as_view(), name='trim-list'),

    path('applications/<slug:slug>/', ApplicationDetailView.as_view(), name='application-detail'),
    path('applications/', ApplicationDetailView.as_view(), name='application-search'),

    path('body_parts/', BodyPartListView.as_view(), name='body_part_detail'),

    path('car-list/', CarListView.as_view(), name='car-list'),
    path('car-list/<str:search_term>/', CarSearchView.as_view(), name='car-search'),

    path('car-filter/<slug:slug>', CarFilterView.as_view(), name='car-filter'),
    path('car-search/<str:search_term>/', CarSearchView.as_view(), name='car-search'),

    path('files/', FilesListView.as_view(), name='files-list'),
    # path('files/<int:car_id>/', FilesListView.as_view(), name='files-list-with-car'),
    path('files/<slug:slug>/', FilesDetailView.as_view(), name='files-detail'),

]

