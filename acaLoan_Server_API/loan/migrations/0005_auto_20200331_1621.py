# Generated by Django 3.0.3 on 2020-03-31 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0004_auto_20200310_1441'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='action',
            options={'ordering': ['timestamp']},
        ),
        migrations.AlterField(
            model_name='board',
            name='board_no',
            field=models.IntegerField(unique=True, verbose_name='board number'),
        ),
        migrations.AlterField(
            model_name='board',
            name='raspi_tag',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loan.RaspiTag'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_card',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loan.StudentCard'),
        ),
    ]