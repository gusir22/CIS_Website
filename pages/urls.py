# pages/urls.py
from django.urls import path

from .views import (
    SandboxView,  # # Used to try concepts in a clean slate. This import should be deleted when live
    HomePageView,
    QandAView,
    ProductsPublicListView,
    ProductPublicDetailView,
    ProductPublicSearchResultsListView,
    TermandConditionsView,
    ProjectPublicGalleryView,
    ProjectPublicDetailView,
    ProjectPublicSearchResultsListView,
    ContactView,
    ContactSuccessView,
    RequestEstimatesView,
    RequestEstimatesSuccessView,
)


urlpatterns = [
    path('sandbox/', SandboxView.as_view(), name='sandbox'),  # Used to try concepts in a clean slate. This url should be deleted when live

    # Q&A pages
    path('questions/', QandAView.as_view(), name='q&a'),

    # Contact pages
    path('request_estimate/', RequestEstimatesView.as_view(), name='request_estimate'),
    path('request_estimate/success/', RequestEstimatesSuccessView.as_view(), name='request_estimate_success'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact/success/', ContactSuccessView.as_view(), name='contact_success'),

    # Project Gallery pages
    path('project_gallery/search/', ProjectPublicSearchResultsListView.as_view(), name='project_public_search_results_list'),
    path('project_gallery/<uuid:pk>/', ProjectPublicDetailView.as_view(), name='project_public_detail'),
    path('project_gallery/', ProjectPublicGalleryView.as_view(), name='project_public_gallery'),

    # Product pages accessible in public pages
    path('products/search/', ProductPublicSearchResultsListView.as_view(), name='product_public_search_results_list'),
    path('products/<uuid:pk>/', ProductPublicDetailView.as_view(), name='product_public_detail'),
    path('products/', ProductsPublicListView.as_view(), name='products_public_list'),

    # Terms and Conditions pages
    path('terms_and_conditions/', TermandConditionsView.as_view(), name='terms_and_conditions'),

    # Home pages
    path('', HomePageView.as_view(), name='home'),
]