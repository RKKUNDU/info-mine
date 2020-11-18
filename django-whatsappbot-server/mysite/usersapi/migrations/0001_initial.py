# Generated by Django 3.1.3 on 2020-11-06 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('mobile_no', models.CharField(max_length=10)),
                ('ldap_email', models.EmailField(max_length=254)),
                ('ldap_pass', models.CharField(max_length=250)),
                ('cse_email', models.EmailField(max_length=254)),
                ('cse_email_pass', models.CharField(max_length=250)),
                ('moodle_id', models.CharField(max_length=30)),
                ('moodle_pass', models.CharField(max_length=250)),
            ],
        ),
    ]