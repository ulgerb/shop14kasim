# Generated by Django 4.1.4 on 2022-12-28 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appMy', '0009_card_image1_card_image2_alter_card_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='image',
        ),
        migrations.AddField(
            model_name='card',
            name='image3',
            field=models.FileField(null=True, upload_to='', verbose_name='Card Resimi 3'),
        ),
        migrations.AlterField(
            model_name='card',
            name='image1',
            field=models.FileField(null=True, upload_to='', verbose_name='Card Resimi 1'),
        ),
        migrations.AlterField(
            model_name='card',
            name='image2',
            field=models.FileField(null=True, upload_to='', verbose_name='Card Resimi 2'),
        ),
    ]
