# Generated by Django 4.1 on 2022-09-14 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemimage',
            options={'verbose_name': '상품 이미지'},
        ),
        migrations.AlterField(
            model_name='itemoption',
            name='option_name',
            field=models.CharField(help_text='무게, 용량 등', max_length=30, verbose_name='옵션명'),
        ),
        migrations.AlterField(
            model_name='itemoption',
            name='option_value',
            field=models.CharField(help_text='판매 단위', max_length=30, verbose_name='옵션값'),
        ),
    ]