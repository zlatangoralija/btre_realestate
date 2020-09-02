from django.shortcuts import render, get_object_or_404
from .models import Listing
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from listings.choices import price_choices, bedroom_choices, state_choices

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context = {
        'listings': paged_listings
    }

    return render(request, 'listings/index.html', context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    context = {
        'listing': listing
    }
    return render(request, 'listings/listing.html', context)

def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    keywords = request.GET['keywords'] if 'keywords' in request.GET else None
    city = request.GET['city'] if 'city' in request.GET else None
    state = request.GET['state'] if 'state' in request.GET else None
    bedrooms = request.GET['bedrooms'] if 'bedrooms' in request.GET else None
    price = request.GET['price'] if 'price' in request.GET else None

    if keywords:
        queryset_list = queryset_list.filter(description__icontains=keywords)

    if city:
        queryset_list = queryset_list.filter(city__iexact=city)

    if state:
        queryset_list = queryset_list.filter(state__iexact=state)

    if bedrooms:
        queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    if price:
        queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'listings': queryset_list,
        'price_choices': price_choices,
        'bedroom_choices': bedroom_choices,
        'state_choices': state_choices,
    }
    return render(request, 'listings/search.html', context)