import random

def generate_order_id(order):
    first_bit = order.user.username
    second_bit = str(order.ordered_date)
    third_bit = str(random.randint(0, 50))
    fourth_bit = str(random.randint(0, 50))

    order_id = first_bit + second_bit + third_bit + fourth_bit
    return order_id