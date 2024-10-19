from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    path('set_language/', views.set_language, name='set_language'),


    #user/login/register/otp
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/',views.dham_logout_view, name='logout'),
    path('verify_otp_view/', views.verify_otp_view, name='verify_otp_view'),
    path('guide/guide-detail/<str:guideId>/', views.guide_detail, name='guide-detail'),
    path('book_guide/', views.book_guide, name='book-guide'),

    #acc
    path('accommodation_state', views.accommodation_state, name="accommodation"),
    path('e-pooja', views.e_pooja, name="e_pooja"),
    path('e-pooja-detial', views.e_pooja_detail, name="e_pooja_detial"),

    


    # Hotels Listing or Details Routes 
    path('property-by-<str:property_city>/<str:property_city_id>/', views.get_hotel_by_city, name='property_by_city'),
    path('about-hotel/<str:city_id>/<str:hotel_id>/', views.detail_page_hotel, name='detail_page_hotel'),
    path('book_hotel/', views.BookHotel, name='book_hotel'),

    # Guide Listing or Details Routes 
    path('guide/', views.guide, name='guide'),
    path('guide-carousel/', views.guide_carousel, name='guide-carousel'),
    path('guide/guide-detail/', views.guide_detail, name='guide-detail'),

    # Live Darshan Listing or Details Routes 
    path('live_darshan', views.live_darshan, name='live_darshan'),
    path('live_darshan/live_darshan_detail', views.live_darshan_detail, name='live_darshan_detail'),

    # Blog Listing or Details Routes 
    path('blogs', views.blog_list, name='blogs'),
    path('blogs/<str:blog_loc>/<str:blog_id>/', views.blog_detail_page , name='blog_detail_page'),

    # site skeleton Page routes
    path('contact', views.contact_us, name="contact_us"),
    path('about-us', views.about_us, name="about_us"),
    path('terms-condition', views.terms_condition, name="terms_condition"),
    path('privacy-policy', views.privacy_policy, name="privacy_policy"),
    path('faq', views.faq_board, name="faq"),
    path('testimonials', views.testimonials, name="testimonials"),





    

]
