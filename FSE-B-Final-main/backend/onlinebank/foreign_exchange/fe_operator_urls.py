from django.urls import path, re_path
from foreign_exchange import fe_operator_views

urlpatterns = [
    re_path('foreign/delete',fe_operator_views.handleDeleteOperator),
    re_path('foreign/searchall', fe_operator_views.handlesearchallOperator),
    re_path('foreign/updateauthority', fe_operator_views.handleModifyOperator),
    re_path('foreign/search',fe_operator_views.handleSearch),
    re_path('foreign/add',fe_operator_views.handleAddOperator)
]