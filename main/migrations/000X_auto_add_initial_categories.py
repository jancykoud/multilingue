# main/migrations/000X_auto_add_initial_categories.py

from django.db import migrations

def create_initial_categories(apps, schema_editor):
    Category = apps.get_model('main', 'Category')
    Category.objects.create(name='Technology')
    Category.objects.create(name='Health')
    Category.objects.create(name='Science')
    Category.objects.create(name='Education')
    Category.objects.create(name='Lifestyle')

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_categories),
    ]