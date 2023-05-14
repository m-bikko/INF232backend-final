# Generated by Django 4.2.1 on 2023-05-14 19:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0002_alter_product_descript'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='John Doe (Default)', max_length=200, null=True)),
                ('title', models.CharField(default='Bla Bla Bla....', max_length=200, null=True)),
                ('phone', models.CharField(max_length=12)),
                ('descript', models.CharField(default='Bla Bla Bla.....', max_length=200, null=True)),
                ('profile_img', models.ImageField(blank=True, default='media/default.jpg', null=True, upload_to='media')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
