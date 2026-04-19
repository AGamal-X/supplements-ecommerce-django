from django.db import migrations


def deduplicate_products(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    seen = set()
    duplicates = []
    for product in Product.objects.all().order_by('category', 'name', 'price', 'id'):
        signature = (product.category, product.name.strip().lower(), str(product.price).strip())
        if signature in seen:
            duplicates.append(product.pk)
        else:
            seen.add(signature)
    if duplicates:
        Product.objects.filter(pk__in=duplicates).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0003_alter_product_options'),
    ]

    operations = [
        migrations.RunPython(deduplicate_products, migrations.RunPython.noop),
    ]
