from django.db import models
import uuid
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from core.models import Company, Department, Affiliate, Employee


# PDF and IMG Files Naming Functions:
def generate_random_filename(instance, filename):
    """Generate a random filename for uploaded files."""
    random_filename = f"{uuid.uuid4().hex}.pdf"
    model_name = instance.__class__.__name__.lower()
    return f'{model_name}/{random_filename}'

def get_pdf_upload_path(instance, filename):
    """Get the upload path for PDF files."""
    return f'pdfs/{generate_random_filename(instance, filename)}'

def get_img_upload_path(instance, filename):
    """Get the upload path for IMG files."""
    return f'item_img/{generate_random_filename(instance, filename)}'



class AssetCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="اسم التصنيف")
    discription = models.CharField(max_length=255, blank=True, verbose_name="التفاصيل...")  # For Arabic or other descriptive names

    def __str__(self):
        return self.name


# Asset Models:
class Asset(models.Model):
    ASSET_TYPES = [
        ('Car', 'سيارات'),
        ('Electronic', 'الكترونيات'),
        ('Computer', 'اجهزة تقنية'),
        ('Hardware', 'قطع غيار تقنية'),
        ('Printers', 'طابعات وماسحات'),
        ('Office', 'مكتبية'),
        ('Appliance', 'كهرومنزلية'),
        ('Electrical', 'كهربائية'),
        ('Equipment', 'معدات ورش'),
        ('Furniture', 'اثاث'),
        ('Cleaner', 'مواد تنظيف'),
        ('Food', 'مواد اعاشة'),
        ('Other', 'اخرى'),
    ]

    category = models.ForeignKey(AssetCategory, on_delete=models.PROTECT, related_name='assets', blank=True, verbose_name="التصنيف")
    name = models.CharField(max_length=255, verbose_name="اسم الصنف")
    brand = models.CharField(max_length=255, verbose_name="الماركة", blank=True)
    unit = models.CharField(max_length=50, choices=[
        ('piece', 'قطعة'),
        ('box', 'علبة'),
    ], verbose_name="وحدة القياس", default='piece')

    class Meta:
        verbose_name = "صنف"
        verbose_name_plural = "اصناف"
        ordering = ['-category']

    def __str__(self):
        return self.name


# Import Transaction Model:
class ImportRecord(models.Model):
    trans_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    date = models.DateField()
    assign_number = models.CharField(max_length=50)
    assign_date = models.DateField()
    items = models.ManyToManyField(Asset, through='ImportItem')
    notes = models.TextField()
    pdf_file = models.FileField(upload_to=get_pdf_upload_path, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Import {self.trans_id} - {self.date}"


# Import Transaction Items:
class ImportItem(models.Model):
    trans_id = models.ForeignKey(ImportRecord, related_name='Importeditems', on_delete=models.SET_NULL, null=True)
    asset = models.ForeignKey('Asset', related_name='ImportRecord', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    return_at = models.DateTimeField(blank=True, null=True)
    return_purpose = models.CharField(max_length=50, choices=[
        ('Damaged', 'Damaged'),
        ('Replace', 'Replace'),
    ], blank=True, null=True)
    return_notes = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.asset.name} - {self.quantity} pcs"


# Export Transaction Model:
class ExportRecord(models.Model):
    trans_id = models.AutoField(primary_key=True)
    export_type = models.CharField(max_length=50, choices=[
        ('Consume', 'Consume'),
        ('Personal', 'Personal'),
        ('Department', 'Department'),
        ('Loan', 'Loan'),
    ])
    # ContentType for dynamic ForeignKey
    # entity_content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    # entity_object_id = models.PositiveIntegerField()
    # entity_selection = GenericForeignKey('entity_content_type', 'entity_object_id')
    date = models.DateField()
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Export Record {self.trans_id} - {self.export_type} - {self.date}"


# Export Transaction Items:
class ExportItem(models.Model):
    trans_id = models.ForeignKey(ExportRecord, related_name='items', on_delete=models.SET_NULL, null=True)
    asset = models.ForeignKey('Asset', related_name='EmportRecord', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    sn = models.CharField(max_length=100, blank=True, null=True)
    pic = models.ImageField(upload_to=get_img_upload_path, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    return_at = models.DateTimeField(blank=True, null=True)
    return_purpose = models.CharField(max_length=50, choices=[
        ('EndJob', 'End Job'),
        ('Stolen', 'Stolen'),
        ('NoReason', 'No Reason'),
    ], blank=True, null=True)
    return_condition = models.CharField(max_length=50, choices=[
        ('Good', 'Good'),
        ('Bad', 'Bad'),
        ('Dead', 'Dead'),
    ], blank=True, null=True)
    return_notes = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.asset.name} - {self.quantity} pcs"
