from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User, Permission
from django.core.management.utils import get_random_secret_key

class Command(BaseCommand):
    help = "Create Admin Group, Superuser, and Assign the Superuser to the Group"

    def add_arguments(self, parser):
        # Remove default from 'username' and make it required.
        parser.add_argument("username", type=str, help="Username of the superuser to create or add to the group")
        # Optional arguments with default values
        parser.add_argument("--email", type=str, help="Email address of the superuser", default="admin@admins.com")
        parser.add_argument("--password", type=str, help="Password for the superuser", default="ad123123")

    def handle(self, *args, **kwargs):
        username = kwargs["username"]
        email = kwargs["email"]
        password = kwargs["password"]

        # Ensure the password is provided
        if not password:
            password = get_random_secret_key()  # Generate a random password
            self.stdout.write(self.style.WARNING(f"No password provided. Using generated password: {password}"))

        # Create or get the superuser
        superuser, created = User.objects.get_or_create(username=username, defaults={
            "email": email,
            "is_staff": True,
            "is_superuser": True,
        })

        if created:
            superuser.set_password(password)
            superuser.save()
            self.stdout.write(self.style.SUCCESS(f"Superuser {username} created."))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser {username} already exists."))

        # Create or get the group
        group_name = "Admin Group"
        admins, created = Group.objects.get_or_create(name=group_name)

        # Assign permissions to the group
        permissions = Permission.objects.filter(codename__in=[
            "add_user", "change_user", "delete_user", "view_user"  # Example permissions
        ])
        admins.permissions.set(permissions)

        # Add the superuser to the group
        superuser.groups.add(admins)
        self.stdout.write(self.style.SUCCESS(f"Superuser {username} added to group '{group_name}'."))
