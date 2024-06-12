from django.urls import path, re_path
from foreign_exchange import rate_update_record_views

urlpatterns = [
    re_path('user/currency/search', rate_update_record_views.show_rate_update_record),
    re_path('user/currency/simulation', rate_update_record_views.get_simulation_data),
    re_path('Operator/search',rate_update_record_views.handlesearch),
    re_path('Operator/show',rate_update_record_views.handleshow)
]