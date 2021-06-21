# Generated by Django 3.2.4 on 2021-06-18 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('produto_id', models.CharField(max_length=50, unique=True, verbose_name='product_id')),
            ],
            options={
                'verbose_name': 'produto',
                'verbose_name_plural': 'produtos',
            },
        ),
        migrations.CreateModel(
            name='Favorito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente')),
                ('produtos', models.ManyToManyField(related_name='produtos', to='produtos.Produto')),
            ],
            options={
                'verbose_name': 'favorito',
                'verbose_name_plural': 'favoritos',
            },
        ),
    ]
