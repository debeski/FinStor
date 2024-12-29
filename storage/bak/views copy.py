from django.shortcuts import render, get_object_or_404, redirect
import logging
from django_tables2 import RequestConfig 
from django.contrib.auth.decorators import login_required
from .models import Asset, AssetCategory, ImportRecord, ImportItem
from .tables import AssetTable, AssetCategoryTable
from .forms import AssetForm, AssetCategoryForm, ImportRecordForm, ImportItemForm
from django.http import JsonResponse
from django.contrib import messages


logger = logging.getLogger('storage')


@login_required
def manage_category(request, category_id=None):
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
            return redirect('manage_category')

    return render(request, 'assetcats.html', {
        'table': table,
        'form': form,
        'editing': bool(category_id),  # Flag to determine if editing
    })


@login_required
def manage_assets(request):
    # Get all asset types for the tab view
    categories = AssetCategory.objects.all()
    categories_dict = {cat.id: cat.name for cat in categories}

    # Get category and id from query parameters
    category = request.GET.get('category')
    asset_id = request.GET.get('id')

    selected_cat = None
    if category:
        try:
            category = int(category)
            selected_cat = AssetCategory.objects.filter(id=category).first()
        except ValueError:
            pass

    asset = None
    if asset_id:
        try:
            asset_id = int(asset_id)
            asset = Asset.objects.filter(id=asset_id).first()
        except ValueError:
            pass

    # Handle form submission
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset, selected_cat=selected_cat)
        if form.is_valid():
            form.save()
            # Redirect to clear the form and stay on the same tab
            return redirect(f"{request.path}?category={selected_cat.id if selected_cat else ''}")
        else:
            print(form.errors)  # Debugging: Print form errors to the console
    else:
        form = AssetForm(instance=asset, selected_cat=selected_cat)

    # Check if a category was selected; otherwise, show all assets
    if selected_cat:
        assets = Asset.objects.filter(category=selected_cat)
    else:
        assets = Asset.objects.all()  # Show all assets by default

    # Create the table
    table = AssetTable(assets)
    RequestConfig(request).configure(table)

    print(f"Selected Category: {selected_cat, selected_cat.id if selected_cat else ''}")
    print(f"Selected Asset: {asset, asset.id if asset else ''}")
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


@login_required
def import_records(request):
    # Fetch all ImportRecord entries
    records = ImportRecord.objects.all().order_by('-date')
    return render(request, 'import.html', {'records': records})


@login_required
def import_create(request):
    print(f"Current session contents: {request.session.items()}")
    # Initialize forms
    import_record_form = ImportRecordForm(request.POST or None)
    import_item_form = ImportItemForm(request.POST or None)

    # Session-based dictionary for storing items temporarily
    if 'import_items' not in request.session:
        request.session['import_items'] = {}
        print("Initialized import_items in session.")
    else:
        print("import_items already exists in session.")

    # Handle adding an item to the import record
    if request.method == 'POST':
        print(f"POST request received: {request.POST}")

        if 'add_item' in request.POST:
            if import_item_form.is_valid():
                item_data = {
                    'asset': request.POST.get('asset'),
                    'quantity': request.POST.get('quantity')
                }
                print(f"Adding item: {item_data}")

                # Add the item to the session
                items = request.session.get('import_items', {})
                items[item_data['asset']] = item_data['quantity']
                request.session['import_items'] = items
                print(f"Current items in session: {items}")

                # Redirect to refresh form
                return redirect('import_create')
            else:
                print(f"Item form errors: {import_item_form.errors}")


        # Handle final form submission
        elif 'submit_record' in request.POST:
            print("Submitting import record form.")
            if import_record_form.is_valid():
                # Create the ImportRecord instance
                import_record = import_record_form.save()
                print("ImportRecord created successfully.")

                # Create ImportItems from the session data
                items = request.session.get('import_items', {})
                for asset_id, quantity in items.items():
                    print(f"Creating ImportItem with asset_id: {asset_id}, quantity: {quantity}")
                    ImportItem.objects.create(
                        trans=import_record,
                        asset=asset_id,
                        quantity=quantity
                    )

                # Clear the session items after the import record is saved
                del request.session['import_items']
                print("Cleared import_items from session.")

                # Redirect to success or summary page
                messages.success(request, 'Import record created successfully!')
                return redirect('import_create')
            else:
                print("Import record form is invalid.")
                print(f"Form errors: {import_record_form.errors}")

    # Before rendering, check what is in import_items
    import_items = request.session.get('import_items', {})


    print(f"Rendering template with import_items: {import_items}")
    return render(request, 'invoice.html', {
        'import_record_form': import_record_form,
        'import_item_form': import_item_form,
        'import_items': import_items
    })


@login_required
def import_item_delete(request, asset_id):
    # Remove the item from the session
    items = request.session.get('import_items', {})
    if asset_id in items:
        del items[asset_id]
        request.session['import_items'] = items

    # Redirect to the import record creation page
    return redirect('import_create')
