from django.shortcuts import render, get_object_or_404, redirect
import logging
from django_tables2 import RequestConfig 
from django.contrib.auth.decorators import login_required
from .models import Asset, AssetCategory
from .tables import AssetTable, AssetCategoryTable
from .forms import AssetForm, AssetCategoryForm


logger = logging.getLogger('FinStor')


@login_required
def manage_categories(request, category_id=None):
    # Fetch all categories for display in the table
    categories = AssetCategory.objects.all()
    table = AssetCategoryTable(categories)
    RequestConfig(request).configure(table)

    # Handle editing a category
    if category_id:
        category = get_object_or_404(AssetCategory, id=category_id)
        form = AssetCategoryForm(instance=category)
    else:
        form = AssetCategoryForm()

    # Handle form submission for adding or editing
    if request.method == 'POST':
        if category_id:
            form = AssetCategoryForm(request.POST, instance=category)
        else:
            form = AssetCategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('manage_categories')

    return render(request, 'assetcats.html', {
        'table': table,
        'form': form,
        'editing': bool(category_id),  # Flag to determine if editing
    })


@login_required
def manage_assets(request):
    # Get all asset types for the tab view
    categories = AssetCategory.objects.all()
    categories_dict = {cat.id: cat.name for cat in categories}  # Create a dict for categories

    category = request.GET.get('category')  # Get 'category' from query params

    # Get the selected category if it exists
    if category:
        try:
            category = int(category)  # Ensure the category is an integer
            selected_cat = AssetCategory.objects.filter(id=category).first()
        except ValueError:
            selected_cat = None
    else:
        selected_cat = None

    # Handle form submission
    if request.method == 'POST':
        form = AssetForm(request.POST, selected_cat=selected_cat)
        if form.is_valid():
            form.save()
            # Redirect to clear the form and stay on the same tab
            return redirect(f"{request.path}?category={selected_cat.id if selected_cat else ''}")
        else:
            print(form.errors)  # Debugging: Print form errors to the console
    else:
        form = AssetForm(selected_cat=selected_cat)

    # Check if a category was selected; otherwise, show all assets
    if selected_cat:
        assets = Asset.objects.filter(category=selected_cat)
    else:
        assets = Asset.objects.all()  # Show all assets by default

    # Create the table
    table = AssetTable(assets)
    RequestConfig(request).configure(table)

    print(f"Selected Category: {selected_cat, selected_cat.id if selected_cat else ''}")
    print(f"category: {category}")

    # Render the page with the table and tabs
    return render(request, 'assets.html', {
        'categories': categories_dict,
        'selected_cat': selected_cat,
        'table': table,
        'form': form,
        'ar_name': Asset._meta.verbose_name,
        'ar_names': Asset._meta.verbose_name_plural,
    })

