# Generated by Django 2.2.4 on 2019-10-01 06:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InsuranceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('mobile', models.CharField(max_length=10)),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InsurancePlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, null=True)),
                ('premium', models.FloatField()),
                ('total', models.FloatField()),
                ('duration', models.DurationField()),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.InsuranceType')),
            ],
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('plan_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.InsurancePlan')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=40, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('insurance_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Insurance')),
            ],
        ),
    ]