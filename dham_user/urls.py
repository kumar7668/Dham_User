from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    path('set_language/', views.set_language, name='set_language'),

    #acc
    path('accommodation_state', views.accommodation_state, name="accommodation"),
    path('e-pooja', views.e_pooja, name="e_pooja"),
    path('e-pooja', views.e_pooja_detail, name="e_pooja_detial"),

    


    # Hotels Listing or Details Routes 
    path('property-by-<str:property_city>/<str:property_city_id>/', views.get_hotel_by_city, name='property_by_city'),

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
