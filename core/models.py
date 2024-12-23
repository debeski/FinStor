from django.db import models


# Entity Models:
class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)

    class Meta:
        verbose_name = "الشركة"
        verbose_name_plural = "الشركات"
        ordering = ['name']  # Sort by created_at in descending order

    def __str__(self):
        return self.name


class Department(models.Model):
    dept_types = [
        ('GM', 'General Management'),
        ('Department', 'Department'),
        ('Office', 'Office'),
        ('Section', 'Section'),
    ]
    type = models.CharField(max_length=50, choices=dept_types)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "الادارة"
        verbose_name_plural = "الادارات"
        ordering = ['name']  # Sort by created_at in descending order

    def __str__(self):
        return self.name


class Affiliate(models.Model):
    name = models.CharField(max_length=255)
    association = models.CharField(max_length=50, choices=[
        ('Ministry', 'Ministry'),
        ('Department', 'Department'),
        ('Office', 'Office'),
    ])

    class Meta:
        verbose_name = "الجهة"
        verbose_name_plural = "الجهات"
        ordering = ['-association']  # Sort by created_at in descending order

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date_employed = models.DateField()

    class Meta:
        verbose_name = "الموظف"
        verbose_name_plural = "الموظفين"
        ordering = ['name']  # Sort by created_at in descending order

    def __str__(self):
        return self.name

