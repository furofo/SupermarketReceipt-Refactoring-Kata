import pytest

from ..src.model_objects import Product, SpecialOfferType, ProductUnit
from ..src.shopping_cart import ShoppingCart
from ..src.teller import Teller
from tests.fake_catalog import FakeCatalog


def test_ten_percent_discount():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)
    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 1.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)

    receipt = teller.checks_out_articles_from(cart)

    assert 4.975 == pytest.approx(receipt.total_price(), 0.01)
    assert [] == receipt.discounts
    assert 1 == len(receipt.items)
    receipt_item = receipt.items[0]
    assert apples == receipt_item.product
    assert 1.99 == receipt_item.price
    assert 2.5 * 1.99 == pytest.approx(receipt_item.total_price, 0.01)
    assert 2.5 == receipt_item.quantity

def test_ten_percent_discount_simplified():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.80) #ten percent of .80 is 8 cents so shoudl be 72 after htis
    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 1)
    receipt = teller.checks_out_articles_from(cart)
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)
    assert 0.70 == pytest.apporx(receipt.to)

def test_less_than_5_five_for_amount_discount():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.80) #ten percent of .80 is 8 cents so shoudl be 72 after htis
    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 1)
 # Define the parameters for the discount function
    product = toothbrush
    quantity = 1
    unit_price = 0.80
    offer = Offer(SpecialOfferType.FIVE_FOR_AMOUNT, argument=3.00)  # Example offer
    number_of_x = 1
    quantity_as_int = 1

    # Assert that ValueError is raised
    with self.assertRaises(ValueError) as context:
        five_for_amount_discount(product, quantity, unit_price, offer, number_of_x, quantity_as_int)

    # Optionally, check the error message
    self.assertEqual(
        str(context.exception),
        f"Error: Quantity of product {product} must be at least 5 to apply the discount."
    )