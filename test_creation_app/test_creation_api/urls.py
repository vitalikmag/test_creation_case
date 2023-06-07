from django.urls import path
from .views import create_tests, save_iq_test_result, save_eq_test_result, view_test_results

urlpatterns = [
    path('create/', create_tests),
    path('iq/save/', save_iq_test_result),
    path('eq/save/', save_eq_test_result),
    path('<str:login>/', view_test_results),
]
