from django.urls import path, re_path
from .views import (
    BookingSlotsListView,
    UserBookingListView,
#     PostListView, 
#     PostDetailView, 
#     PostDeleteView,
#     PostCreateView,
#     PostUpdateView,
#     UserPostListView,
)

from . import views

urlpatterns = [
    #re_path(r'^booking.{1}slots/', BookingSlotsListView.as_view(), name='booking-slots-home'),
    path('', views.calendar, name='calendar'),
    path('admin_calendar', views.admin_calendar, name='admin-calendar'),
    path('person_registration/<int:pk>/', views.person_registration, name='person_registration'),
    path('user/<str:username>/', UserBookingListView.as_view(), name='user_bookings'),
    
    #path('?week=<int:week_number>/', views.calendar, name='calendar'),
    # path('', PostListView.as_view(), name='blog-home'),
    # path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    # path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    # path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    # path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    # path('post/new/', PostCreateView.as_view(), name='post-create'),
    # path('about/', views.about, name='blog-about'),
    # path('tailwind_testing/', views.tailwind_testing, name='tailwind-testing'),
]
