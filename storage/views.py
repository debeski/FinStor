from django.shortcuts import render, get_object_or_404, redirect
import logging
from django_tables2 import RequestConfig 
from django.contrib.auth.decorators import login_required
from .models import Asset, AssetCategory, ImportRecord, ImportItem
from .tables import AssetTable, AssetCategoryTable, ImportRecordTable
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

    # Clear any residual session data
    if 'import_items' in request.session:
        del request.session['import_items']

    # Fetch all ImportRecord entries
    records = ImportRecord.objects.all().order_by('-date')
    table = ImportRecordTable(records)
    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    return render(request, 'import.html', {'table': table})


@login_required
def import_create(request):
    import_record_instance = None
    import_record_form = ImportRecordForm(request.POST or None, instance=import_record_instance)
    import_item_form = ImportItemForm()

    # Handle both form submissions and Cancel action
    if request.method == 'POST':

        # Finalize the import record submission
        if 'submit_record' in request.POST:
            print("Submitting import record form...")
            import_items = request.session.get('import_items', {})

            if not import_items:
                import_record_form.add_error(None, "يرجى اضافة صنف واحد على الاقل قبل محاولة حفظ الاذن.")

            if import_record_form.is_valid() and import_items:
                import_record = import_record_form.save()
                print("ImportRecord created successfully.")

                # Save all items from the session to the ImportItem Table in DB
                for asset_id, item_data in import_items.items():
                    print(f"Creating ImportItem with asset_id: {asset_id}, price and quantity: {item_data}")
                    ImportItem.objects.create(
                        record=import_record,
                        asset_id=asset_id,
                        quantity=item_data['quantity'],
                        price=item_data['price']
                    )

                # Clear session data after submission
                if 'import_items' in request.session:
                    del request.session['import_items']
                print("Cleared import items from session data after record creation.")

                # Redirect to success or summary page
                messages.success(request, f"تم اضافة اذن استلام رقم: {asset_id} بنجاح.")
                return redirect('import_records')
            else:
                print("Import record form is invalid.")
                print(f"Form errors: {import_record_form.errors}")

    # Prepare items with asset names for display
    import_items = []
    for asset_id, item_data  in request.session.get('import_items', {}).items():
        asset = Asset.objects.get(id=asset_id)
        import_items.append({
            'id': asset_id,
            'name': asset.name,
            'quantity': item_data['quantity'],
            'price': item_data['price'],
            'total': float(item_data['price']) * int(item_data['quantity']),
        })

    print(f"Rendering template with import_items: {import_items}")
    return render(request, 'invoice.html', {
        'import_record_form': import_record_form,
        'import_item_form': import_item_form,
        'import_items': import_items,
    })


def get_assets(request, category_id):
    assets = Asset.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse({'assets': list(assets)})


@login_required
def import_item_add(request):

    # Asset fields for the ImportItemForm
    asset_id = request.GET.get('asset')
    quantity = request.GET.get('quantity')
    price = request.GET.get('price')

    if asset_id and price and quantity:
        items = request.session.get('import_items', {})
        items[asset_id] = {
            'quantity': quantity,
            'price': price,
        }
        request.session['import_items'] = items
        print(f"Added item to session: {asset_id} -> {quantity} -> {price}")
    else:
        print("Asset ID or price or quantity missing.")
        print(f"requested:  {asset_id} -> {quantity} -> {price}")

    # Redirect back to the form page
    return redirect('import_create')


@login_required
def import_item_delete(request, asset_id):

    # Convert asset_id to string to match the session keys
    asset_id = str(asset_id)

    # Check if the item exists in the session
    items = request.session.get('import_items', {})
    if asset_id in items:
        del items[asset_id]  # Remove the item
        request.session['import_items'] = items  # Update the session
        print(f"Item with asset_id {asset_id} removed successfully!")
    else:
        print(f"Item with asset_id {asset_id} not found in the session!")

    # Redirect back to the import_create page
    return redirect('import_create')


@login_required
def import_cancel(request):
    # Clear the import_items from the session
    if 'import_items' in request.session:
        del request.session['import_items']
        print("Cleared import_items from session.")
    
    # Redirect to the import_create page
    return redirect('import_records')


def import_details(request, trans_id):
    # Get the transaction record by trans_id
    record = get_object_or_404(ImportRecord, trans_id=trans_id)
    
    # Get related assets from ImportItem
    related_assets = ImportItem.objects.filter(record=record).select_related('asset')

    # Prepare data for the template
    assets_with_totals = [
        {
            'name': asset.asset.name,
            'brand': asset.asset.brand,
            'quantity': asset.quantity,
            'price': asset.price,  # Assuming Asset model has a `price` field
            'total': asset.quantity * asset.price,  # Calculate total
        }
        for asset in related_assets
    ]

    context = {
        'record': record,
        'related_assets': assets_with_totals,
    }
    return render(request, 'import_details.html', context)

