# Generated by Django 4.0.1 on 2022-01-20 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('favorite', '0005_remove_basketitem_content_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='books',
            field=models.ManyToManyField(blank=True, related_name='f_basket', to='favorite.BasketItem'),
        ),
        migrations.AlterField(
            model_name='basketitem',
            name='basket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='f_basket_item', to='favorite.basket'),
        ),
    ]
