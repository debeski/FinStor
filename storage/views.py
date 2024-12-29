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
    # Clear residual session data
    if 'import_items' in request.session:
        del request.session['import_items']
    if 'import_record_id' in request.session:
        del request.session['import_record_id']

    print("Cleared import_items and import_record_id from session.")
    # Fetch all ImportRecord entries
    records = ImportRecord.objects.all().order_by('-date')
    table = ImportRecordTable(records)
    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    return render(request, 'import.html', {'table': table})


@login_required
def import_create(request):
    # Check if the import record has already been saved
    import_record_id = request.session.get('import_record_id')
    import_record_instance = None

    if import_record_id:
        # Retrieve the existing import record instance
        import_record_instance = ImportRecord.objects.get(trans_id=import_record_id)

    # Initialize forms
    import_record_form = ImportRecordForm(request.POST or None, instance=import_record_instance)
    import_item_form = ImportItemForm()

    # Session-based dictionary for storing items temporarily
    if 'import_items' not in request.session:
        request.session['import_items'] = {}
        print("Initialized import_items in session.")

    # Handle both form submissions and Cancel action
    if request.method == 'POST':
        print(f"POST request received: {request.POST}")
        
        # Finalize the import record submission
        if 'submit_record' in request.POST:
            print("Submitting import record form.")
            if import_record_form.is_valid():
                import_record = import_record_form.save()
                print("ImportRecord created successfully.")

                # Save all items from the session to the ImportItem Table in DB
                # items = request.session.get('import_items', {})
                for asset_id, item_data in request.session.get('import_items', {}).items():
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
                if 'import_record_id' in request.session:
                    del request.session['import_record_id']
                print("Cleared import_items and import_record_id from session.")

                # Redirect to success or summary page
                messages.success(request, 'Import record created successfully!')
                return redirect('import_records')
            else:
                print("Import record form is invalid.")
                print(f"Form errors: {import_record_form.errors}")

    # Before rendering, check what is in import_items
    import_items = request.session.get('import_items', {})
    print(request.session.get('import_items', {}))

    # Prepare items with asset names for display
    import_items = []
    for asset_id, item_data  in request.session.get('import_items', {}).items():
        asset = Asset.objects.get(id=asset_id)  # Fetch the asset object
        import_items.append({
            'id': asset_id,       # Pass the asset_id for delete functionality
            'name': asset.name,  # Use the asset's name field
            'quantity': item_data['quantity'],
            'price': item_data['price'],
            'total': float(item_data['price']) * int(item_data['quantity']),
        })

    print(f"{import_record_id}")
    print(f"Rendering template with import_items: {import_items}")
    return render(request, 'invoice.html', {
        'import_record_form': import_record_form,
        'import_item_form': import_item_form,
        'import_items': import_items,  # Updated import items with names
    })


def get_assets(request, category_id):
    assets = Asset.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse({'assets': list(assets)})


@login_required
def import_item_add(request):
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
    
    # Optionally, delete the associated ImportRecord (if any exists)
    if 'import_record' in request.session:
        import_record = ImportRecord.objects.filter(trans_id=request.session['import_record']).first()
        if import_record:
            import_record.delete()
            print(f"Deleted ImportRecord with trans_id: {request.session['import_record']}")
        del request.session['import_record']
        print("Cleared import_record from session.")

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



# def import_details(request, trans_id):
#     # Get the transaction record by trans_id
#     record = get_object_or_404(ImportRecord, trans_id=trans_id)
    
#     # Get related assets from ImportItem
#     related_assets = ImportItem.objects.filter(record=record)

#     context = {
#         'record': record,
#         'related_assets': related_assets,
#     }
#     print(related_assets)
#     return render(request, 'import_details.html', context)  # Adjust template path as needed

# ------------------------------------------------------------  IMPORTANT  ------------------------------------------------------------

# @login_required
# def import_create(request):
#     # Check if the import record has already been saved
#     import_record_id = request.session.get('import_record_id')
#     import_record_instance = None

#     if import_record_id:
#         # Retrieve the existing import record instance
#         import_record_instance = ImportRecord.objects.get(trans_id=import_record_id)

#     # Initialize forms
#     import_record_form = ImportRecordForm(request.POST or None, instance=import_record_instance)
#     import_item_form = ImportItemForm(request.POST or None)

#     # Session-based dictionary for storing items temporarily
#     if 'import_items' not in request.session:
#         request.session['import_items'] = {}
#         print("Initialized import_items in session.")

#     # Handle both form submissions and Cancel action
#     if request.method == 'POST':
#         print(f"POST request received: {request.POST}")
        
#         # Handle adding an item to the import record
#         if 'add_item' in request.POST:

#             # Validate and save the import record form
#             if import_record_form.is_valid():
#                 import_record = import_record_form.save()

#                 # Save the import record ID in the session for "edit mode"
#                 request.session['import_record_id'] = import_record.trans_id
                
#                 # Add the item to the session
#                 if import_item_form.is_valid():
#                     item_data = {
#                         'asset': str(request.POST.get('asset')),
#                         'quantity': request.POST.get('quantity')
#                     }
#                     print(f"Adding item: {item_data}")
#                     items = request.session['import_items']
#                     items[item_data['asset']] = item_data['quantity']
#                     request.session['import_items'] = items
#                     print(f"Current items in session: {items}")

#                 # Redirect to the same page to keep adding items
#                 return redirect('import_create')
#             else:
#                 print(f"Item form errors: {import_item_form.errors}")


#         # Finalize the import record submission
#         elif 'submit_record' in request.POST:
#             print("Submitting import record form.")
#             if import_record_form.is_valid():
#                 import_record = import_record_form.save()
#                 print("ImportRecord created successfully.")

#                 # Save all items from the session to the ImportItem Table in DB
#                 items = request.session.get('import_items', {})
#                 for asset_id, quantity in items.items():
#                     print(f"Creating ImportItem with asset_id: {asset_id}, quantity: {quantity}")
#                     ImportItem.objects.create(
#                         record=import_record,
#                         asset_id=asset_id,
#                         quantity=quantity
#                     )

#                 # Clear session data after submission
#                 del request.session['import_items']
#                 del request.session['import_record_id']
#                 print("Cleared import_items and import_record_id from session.")

#                 # Redirect to success or summary page
#                 messages.success(request, 'Import record created successfully!')
#                 return redirect('import_records')
#             else:
#                 print("Import record form is invalid.")
#                 print(f"Form errors: {import_record_form.errors}")

#         elif 'cancel' in request.POST:
#             print("Cancel button pressed. Clearing import_items and deleting ImportRecord.")
        
#             # Clear the import_items from session
#             del request.session['import_items']
#             print("Cleared import_items from session.")
            
#             # Optionally, delete the associated ImportRecord (if any exists)
#             if 'import_record' in request.session:
#                 import_record = ImportRecord.objects.filter(trans_id=request.session['import_record']).first()
#                 if import_record:
#                     import_record.delete()
#                     print(f"Deleted ImportRecord with trans_id: {request.session['import_record']}")
#                 del request.session['import_record']
#                 print("Cleared import_record from session.")
#             print(request)
#             # Redirect to the import_create page
#             return redirect('import_records')

#     # # Before rendering, check what is in import_items
#     # import_items = request.session.get('import_items', {})
#     print(request.POST)
#     # Prepare items with asset names for display
#     import_items = []
#     for asset_id, quantity in request.session.get('import_items', {}).items():
#         asset = Asset.objects.get(id=asset_id)  # Fetch the asset object
#         import_items.append({
#             'id': asset_id,       # Pass the asset_id for delete functionality
#             'name': asset.name,  # Use the asset's name field
#             'quantity': quantity,
#         })


#     print(f"Rendering template with import_items: {import_items}")
#     return render(request, 'invoice.html', {
#         'import_record_form': import_record_form,
#         'import_item_form': import_item_form,
#         'import_items': import_items,  # Updated import items with names
#     })

