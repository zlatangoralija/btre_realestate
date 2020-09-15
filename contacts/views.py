from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect

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

        #Check if user already submitted inquiry
        if request.user.is_authenticated:
            auth_user_id = request.user.id
            has_inquiry = Contact.objects.all().filter(listing_id=listing_id, user_id=auth_user_id)
            if has_inquiry:
                messages.error(request, 'Your already submitted inquiry for this listing!')
                return redirect('/listings/' + listing_id)

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

        try:
            send_mail(
                'Property listing inquiry',
                'There has been an inquiry for ' + listing + '. Sing in to see more details!',
                email,
                [realtor_email],
                fail_silently=False
            )
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

        messages.success(request, 'Your request has been submitted. Realtor will get back to you soon')
        return redirect('/listings/' + listing_id)

