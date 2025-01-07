import math

from model_objects import ProductQuantity, SpecialOfferType, Discount
from enum import Enum

#idea is to add special offer in dictionary and then method with these arguments that returns a discount object

def ten_percent_discount(product, quantity, unit_price, offer, quantity_as_int = None):
    discount_amount = -quantity * unit_price * offer.argument / 100.0
    return Discount(product, f"{offer.argument}% off", discount_amount)

#    offer = Offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothbrush, argument=3.00)  # Example offer

def five_for_amount_discount(product, quantity, unit_price, offer):
    if quantity >= 5:
        five_for_amount_value = offer.argument
        individual_item_cost_with_five_for_amount_discount_applied =  five_for_amount_value / 5
        products_normal_cost = unit_price * quantity
        remainder_of_quantity_divide_by_five = quantity % 5
        products_discounted_cost = (
            (individual_item_cost_with_five_for_amount_discount_applied * 
            (quantity - remainder_of_quantity_divide_by_five)) +
            (remainder_of_quantity_divide_by_five * unit_price)
        )
        discount_total = products_normal_cost - products_discounted_cost

        return Discount(product, "five for " + str(offer.argument), -discount_total)
    else:
        error_message = f"Error: Quantity of product {product} must be at least 5 to apply the discount."
        print(error_message)  # Print the error message
        raise ValueError(error_message)

def three_for_two_discount(product, quantity, unit_price, offer):
    if quantity > 2:
        five_for_amount_value = offer.argument
        individual_item_cost_with_three_for_two_discount_applied =  five_for_amount_value / 5
        products_normal_cost = unit_price * quantity
        remainder_of_quantity_divide_by_two = quantity % 2
        products_discounted_cost = (
            (individual_item_cost_with_three_for_two_discount_applied * 
            (quantity - remainder_of_quantity_divide_by_two)) +
            (remainder_of_quantity_divide_by_two * unit_price)
        )
        discount_total = products_normal_cost - products_discounted_cost
        return Discount(product, "3 for 2", -discount_total)
    else:
        error_message = f"Error: Quantity of product {product} must be at least 3 to apply the discount."
        print(error_message)  # Print the error message
        raise ValueError(error_message) 

discounts = {
    SpecialOfferType.TEN_PERCENT_DISCOUNT: ten_percent_discount,
    SpecialOfferType.FIVE_FOR_AMOUNT: five_for_amount_discount,
    SpecialOfferType.THREE_FOR_TWO: three_for_two_discount
}
class ShoppingCart:

    def __init__(self):
        self._items = []
        self._product_quantities = {}

    @property
    def items(self):
        return self._items

    def add_item(self, product):
        self.add_item_quantity(product, 1.0)

    @property
    def product_quantities(self):
        return self._product_quantities

    def add_item_quantity(self, product, quantity):
        self._items.append(ProductQuantity(product, quantity))
        if product in self._product_quantities.keys():
            self._product_quantities[product] = self._product_quantities[product] + quantity
        else:
            self._product_quantities[product] = quantity

    def create_discount_objects_factory(self, receipt, offers, catalog, quantity, product):
                offer = offers[product]
                unit_price = catalog.unit_price(product)
                quantity_as_int = int(quantity)
                discount = None
                if offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
                    if quantity_as_int >= 2:
                        total = offer.argument * (quantity_as_int / x) + quantity_as_int % 2 * unit_price
                        discount_amount = unit_price * quantity - total
                        discount = Discount(product, "2 for " + str(offer.argument), -discount_amount)
                if offer.offer_type in discounts:
                    discount_function = discounts[offer.offer_type]
                    discount = discount_function(product, quantity, unit_price, offer)
                    return discount
       

    def handle_offers(self, receipt, offers, catalog):
        for product in self._product_quantities.keys():
            quantity_of_product = self._product_quantities[product]
            if product in offers.keys():
                discount = self.create_discount_objects_factory(receipt, offers, catalog, quantity_of_product, product)
                if discount:
                    receipt.add_discount(discount)
