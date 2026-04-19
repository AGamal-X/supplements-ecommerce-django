from payment.models import Order, OrderItem


def create_order_from_summary(*, user, form_data, summary):
    order = Order.objects.create(
        user=user,
        full_name=form_data['full_name'],
        email=form_data['email'],
        phone=form_data['phone'],
        address=form_data['address'],
        city=form_data['city'],
        payment_method=form_data['payment_method'],
        notes=form_data['notes'],
        subtotal=summary['subtotal'],
        shipping=summary['shipping'],
        total=summary['total'],
        status='confirmed',
    )
    OrderItem.objects.bulk_create([
        OrderItem(
            order=order,
            catalog_key=item.app_label,
            product_id=item.product_id,
            product_name=item.name,
            unit_price=item.price,
            quantity=item.quantity,
            line_total=item.line_total,
        )
        for item in summary['items']
    ])
    return order
