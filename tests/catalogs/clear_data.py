def clear_date(products: dict, attrs=("date",)):
    for product in products:
        for attr in attrs:
            product.pop(attr)
    return products