from django.db import migrations, models

CATEGORY_SOURCES = [
    ('performance', 'shop2_product'),
    ('greens', 'shop3_product'),
    ('muscle', 'shop4_product'),
    ('peanut-butter', 'shop5_product'),
    ('protein-bars', 'shop6_product'),
    ('weight-loss', 'shop7_product'),
]


def copy_legacy_products(apps, schema_editor):
    connection = schema_editor.connection
    with connection.cursor() as cursor:
        cursor.execute("UPDATE shop_product SET category = 'performance' WHERE category IS NULL OR category = ''")
        for category, table_name in CATEGORY_SOURCES:
            try:
                rows = cursor.execute(
                    f"SELECT id, name, price, details, description, image FROM {table_name}"
                ).fetchall()
            except Exception:
                continue
            for row in rows:
                product_id, name, price, details, description, image = row
                new_id = f"{category}-{product_id}"
                exists = cursor.execute("SELECT 1 FROM shop_product WHERE id = %s", [new_id]).fetchone()
                if exists:
                    continue
                cursor.execute(
                    "INSERT INTO shop_product (id, category, name, price, details, description, image) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    [new_id, category, name, price, details, description, image],
                )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(
                choices=[
                    ('performance', 'Performance Essentials'),
                    ('greens', 'Green Superfood'),
                    ('muscle', 'Muscle Building Supplements'),
                    ('peanut-butter', 'Peanut Butter'),
                    ('protein-bars', 'Protein Bars'),
                    ('weight-loss', 'Weight Loss'),
                ],
                default='performance',
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.CharField(max_length=40, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='details',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.RunPython(copy_legacy_products, noop_reverse),
    ]
