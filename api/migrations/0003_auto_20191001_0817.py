# Generated by Django 2.2.4 on 2019-10-01 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20191001_0712'),
    ]

    operations = [
        migrations.RenameField(
            model_name='claim',
            old_name='insurance_id',
            new_name='insurance',
        ),
        migrations.RenameField(
            model_name='insurance',
            old_name='plan_id',
            new_name='insurance_plan',
        ),
        migrations.RenameField(
            model_name='insurance',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='insuranceplan',
            old_name='type_id',
            new_name='insurance_type',
        ),
        migrations.RenameField(
            model_name='insurancetype',
            old_name='type_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='userinfo',
            old_name='user_id',
            new_name='user',
        ),
    ]
