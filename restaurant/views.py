from django.shortcuts import render, get_object_or_404

# Create your views here.

from .models import Business, Review
from django.db.models import Q


# class FirstReview:
#     def __init__(self, business_id, text):
#         self.business_id = business_id
#         self.text = text

def search_result(request):
    keywords = request.GET.get('q')
    address = request.GET.get('n')
    print(keywords, address)

    # q = Q()
    #
    # for var in category_list:
    #     q = Q(categories=var) | q

    if ',' in keywords:
        keywords = keywords[0:keywords.find(',')]

    if keywords == '' and address != '':
        business_list = Business.objects.filter(Q(city__iregex=address))
    elif address == '' and keywords != '':
        business_list = Business.objects.filter(
            Q(name__iregex=keywords) | Q(categories__iregex=keywords))
    else:
        business_list = Business.objects.filter(
            (Q(name__iregex=keywords) | Q(categories__iregex=keywords)) & (Q(address__iregex=address) | Q(
                city__iregex=address)))
    business_list = business_list.order_by('-stars')
    for var in business_list:
        first_text = ''
        list = Review.objects.filter(business_id=var.business_id)
        if list[0] is not None:
            first_text = list[0].text
        var.attributes = first_text[0:350]

    photo_path_list = ['Wv9P3aWWLJY2MFlQj7iUVg',
                       '4aL4G1RaC4yHedYnGHXOTQ',
                       'lHTzTGDu3T0p83j33e0HIg',
                       '9-S7sAZDTpBuPoPd9xAD0g',
                       'AzhUiPgZLR3dEucr4StOsQ',
                       'ibfxtZAMjrUnINaQi_DMtQ',
                       'nfSk9l6MLIAgYeoXfwMamw',
                       'lJLzbpbtdfDAsOSWqwI3cg',
                       'oPTTofd8OhWcXI5eB86CfQ',
                       'ktgyc_l8fp1tkn5pxC59gQ', ]
    context = {
        'business_list': business_list,
        'photo_path_list': photo_path_list,
    }
    return render(request, 'restaurant/search_result.html', context)


def detail(request, business_id):
    # context = ''
    # return render(request, 'restaurant/search_result.html', context)
    business = get_object_or_404(Business, pk=business_id)
    review_list = Review.objects.filter(business_id=business_id)
    context = {
        'business': business,
        'review_list': review_list
    }

    return render(request, 'restaurant/detail.html', context)
