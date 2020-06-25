# Generated by Django 3.1b1 on 2020-06-25 22:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200625_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='education', to='users.employee', verbose_name='Employee'),
        ),
        migrations.AlterField(
            model_name='workhistory',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_history', to='users.employee', verbose_name='Employee'),
        ),
    ]
