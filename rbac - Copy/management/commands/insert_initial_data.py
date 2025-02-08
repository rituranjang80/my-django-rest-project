from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from rbac.models import User, Role, Menu

class Command(BaseCommand):
    help = 'Delete all data and insert initial data into the database'

    def handle(self, *args, **kwargs):
        # Delete existing data
        User.objects.all().delete()
        Role.objects.all().delete()
        Menu.objects.all().delete()
        Group.objects.all().delete()
        Permission.objects.all().delete()

        # Create Roles
        roles = [
            Role(name='Admin', description='Administrator role'),
            Role(name='User', description='Regular user role'),
        ]
        Role.objects.bulk_create(roles)

        # Create Menus
        menus = [
            Menu(name='Dashboard', url='/dashboard/'),
            Menu(name='Settings', url='/settings/'),
        ]
        Menu.objects.bulk_create(menus)

        # Create Groups if they do not exist
        groups = ['Admins', 'Users']
        for group_name in groups:
            Group.objects.get_or_create(name=group_name)

        # Create Users
        users = [
            User(username='admin', email='admin@example.com', is_staff=True, is_superuser=True),
            User(username='user1', email='user1@example.com'),
        ]
        User.objects.bulk_create(users)

        # Assign Roles to Users
        admin_role = Role.objects.get(name='Admin')
        user_role = Role.objects.get(name='User')
        admin_user = User.objects.get(username='admin')
        regular_user = User.objects.get(username='user1')
        admin_user.roles.add(admin_role)
        regular_user.roles.add(user_role)

        # Assign Groups to Users
        admin_group = Group.objects.get(name='Admins')
        user_group = Group.objects.get(name='Users')
        admin_user.groups.add(admin_group)
        regular_user.groups.add(user_group)

        self.stdout.write(self.style.SUCCESS('Successfully deleted existing data and inserted initial data'))