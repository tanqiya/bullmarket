from django.shortcuts import render, redirect

from . models import Category, Product, AuctionItem

from django.shortcuts import get_object_or_404

from .forms import ProductForm, BidForm

from django.contrib.auth.decorators import login_required

from PIL import Image

from django.contrib.auth.models import User

from account.models import UserProfile 



def store(request):

    # all_products = Product.objects.all()
    all_products = Product.objects.filter(quantity__gt=0)

    top_categories = Category.objects.order_by('-quantity_sold')[:3]

    context = {'my_products':all_products, 'top_categories':top_categories}

    return render(request, 'store/store.html', context)



def categories(request):

    all_categories = Category.objects.all()

    return {'all_categories': all_categories}



def list_category(request, category_slug=None):

    category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.filter(category=category)


    return render(request, 'store/list-category.html', {'category':category, 'products':products})


def product_info(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    
    # Assuming the seller field contains the username of the seller.
    seller = get_object_or_404(User, username=product.seller)
    user_profile = UserProfile.objects.get(user=seller)
    is_seller_verified = user_profile.is_verified

    context = {
        'product': product,
        'is_seller_verified': is_seller_verified  # Add the is_verified status to the context
    }

    return render(request, 'store/product-info.html', context)

def auction(request):
    items = AuctionItem.objects.all()
    bid_form = BidForm()
    return render(request, 'store/auction.html', {'items': items, 'bid_form': bid_form})

def auction_view(request):
    # Filter products with price greater than 100
    products = Product.objects.filter(price__gt=100)
    return render(request, 'store/auction.html', {'products': products})

@login_required
def upload_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.username
            product.save()  # Save the product instance, not the form

            return redirect('store')
    else:
        form = ProductForm()
    return render(request, 'store/upload_product.html', {'form': form})