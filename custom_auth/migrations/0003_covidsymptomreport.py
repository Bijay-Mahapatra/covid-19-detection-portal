# Generated by Django 5.1.3 on 2025-04-08 18:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0002_alter_user_options_alter_user_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='CovidSymptomReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checked_at', models.DateTimeField(auto_now_add=True)),
                ('is_positive', models.BooleanField(default=False)),
                ('breathing_problem', models.BooleanField(default=False)),
                ('fever', models.BooleanField(default=False)),
                ('dry_cough', models.BooleanField(default=False)),
                ('sore_throat', models.BooleanField(default=False)),
                ('runny_nose', models.BooleanField(default=False)),
                ('asthma', models.BooleanField(default=False)),
                ('headache', models.BooleanField(default=False)),
                ('heart_diseases', models.BooleanField(default=False)),
                ('diabetes', models.BooleanField(default=False)),
                ('hypertension', models.BooleanField(default=False)),
                ('fatigue', models.BooleanField(default=False)),
                ('abroad_travel', models.BooleanField(default=False)),
                ('attended_gathering', models.BooleanField(default=False)),
                ('visited_public_areas', models.BooleanField(default=False)),
                ('family_working_in_public', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
