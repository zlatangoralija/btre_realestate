from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        user_id = request.POST['user_id']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        realtor_email = request.POST['realtor_email']

        contact = Contact(
            listing_id=listing_id,
            listing=listing,
            user_id=user_id,
            name=name,
            email=email,
            phone=phone,
            message=message,
            realtor_email=realtor_email
        )

        contact.save()

        messages.success(request, 'Your request has been submitted. Realtor will get back to you soon')
        return redirect('/listings/' + listing_id)