from django.db import migrations


def fill_product_content(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')

    content_by_id = {
        '1': {
            'details': 'Daily performance support. Easy to mix before or after training.',
            'description': 'Creatine is commonly used in strength and power routines to support training performance, repeated efforts, and recovery as part of a consistent workout plan.',
        },
        '2': {
            'details': 'Essential amino acids formula for workout support and recovery.',
            'description': 'EAA provides essential amino acids often used around workouts to support muscle recovery, training output, and daily protein intake when your routine is demanding.',
        },
        '3': {
            'details': 'Amino support formula suited for pre- or intra-workout use.',
            'description': 'This EAA formula fits athletes looking for a simple amino blend that can be used around training to support hydration, recovery, and workout consistency.',
        },
        '5': {
            'details': 'Workout amino blend with a practical everyday serving format.',
            'description': 'A straightforward amino support option designed for active users who want a convenient way to add essential amino acids around exercise sessions.',
        },
        '8': {
            'details': 'Larger pack option for athletes with a regular training schedule.',
            'description': 'A higher-volume EAA pack built for people who train often and want an amino formula they can keep in regular rotation for training and recovery support.',
        },
        'greens-1': {
            'details': 'Daily greens blend for wellness-focused nutrition support.',
            'description': 'Musclife Green Superfood is positioned as an easy daily greens option that helps complement your nutrition routine with plant-based support for overall wellness.',
        },
        'muscle-1': {
            'details': 'Essential amino blend for muscle-focused training blocks.',
            'description': 'A muscle-support EAA product suited to gym routines where recovery, workout quality, and amino support matter across the week.',
        },
        'muscle-2': {
            'details': 'Biotin-focused capsule formula in a simple daily format.',
            'description': 'Biotin Amla Capsules fit a wellness-focused supplement stack and are typically used as a convenient daily support option within broader health and fitness routines.',
        },
        'muscle-3': {
            'details': 'High-calorie mass gainer for bulking phases and calorie support.',
            'description': 'Bulk-O-Mania is presented by Musclife as a weight and muscle gain formula designed for users looking to increase calorie intake, size, and strength during bulking phases.',
        },
        'muscle-4': {
            'details': 'Fish oil capsules with EPA and DHA for daily use.',
            'description': 'Fish oil with EPA and DHA is commonly used as part of a daily wellness routine for convenient omega-3 intake and general nutrition support.',
        },
        'muscle-5': {
            'details': 'Glutamine powder that fits post-workout and recovery routines.',
            'description': 'L-Glutamine Powder is often added to recovery-focused stacks and can be used by active users looking for a simple supplement around training days.',
        },
        'peanut-butter-1': {
            'details': 'Crunchy chocolate peanut butter with a richer texture.',
            'description': 'A snack-friendly peanut butter option that works well with toast, oats, smoothies, or quick calories between meals when you want more flavor and texture.',
        },
        'peanut-butter-2': {
            'details': 'Smooth chocolate peanut butter for easy spreading and mixing.',
            'description': 'A smooth high-protein style peanut butter designed for convenient everyday use in breakfasts, shakes, snacks, and calorie-support meals.',
        },
        'peanut-butter-3': {
            'details': 'Classic creamy peanut butter for balanced daily use.',
            'description': 'A versatile creamy peanut butter that fits simple meal prep, snacks, smoothies, and fitness-focused eating plans without overcomplicating your routine.',
        },
        'protein-bars-1': {
            'details': 'Blueberry-flavored protein bar for fast grab-and-go snacking.',
            'description': 'A convenient protein bar built for busy schedules, light hunger between meals, and simple on-the-go snacking with a fruit-forward flavor.',
        },
        'protein-bars-2': {
            'details': 'Chocolate protein bar suited for quick daily snacking.',
            'description': 'A practical snack option for users who want a portable bar that fits workdays, gym bags, or post-workout routines without needing preparation.',
        },
        'protein-bars-3': {
            'details': 'Cookies-and-cream style protein bar with dessert-like flavor.',
            'description': 'A sweet-style protein bar designed for convenient snacking when you want a more indulgent flavor profile while keeping your routine simple.',
        },
        'weight-loss-1': {
            'details': 'L-Carnitine liquid with cranberry flavor in a ready-to-use format.',
            'description': 'WeighTrans is presented as a dietary support liquid that fits active lifestyles and can be used as part of a balanced weight-management routine.',
        },
        'weight-loss-2': {
            'details': 'Green mango flavored L-Carnitine liquid for everyday support.',
            'description': 'A flavored liquid support option suited to users who prefer a ready-to-drink format within a wider plan focused on consistency, activity, and balanced nutrition.',
        },
        'weight-loss-3': {
            'details': 'Orange-flavored L-Carnitine liquid with convenient daily use.',
            'description': 'A practical liquid format for users who want a straightforward supplement option to pair with training, diet structure, and general weight-management goals.',
        },
    }

    for product in Product.objects.all():
        data = content_by_id.get(str(product.pk))
        if not data:
            continue
        product.details = data['details']
        product.description = data['description']
        product.save(update_fields=['details', 'description'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_deduplicate_products'),
    ]

    operations = [
        migrations.RunPython(fill_product_content, noop),
    ]
