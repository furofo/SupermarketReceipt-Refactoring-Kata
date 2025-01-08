import pytest

from model_objects import Product, SpecialOfferType, ProductUnit, Offer
from shopping_cart import ShoppingCart, five_for_amount_discount, three_for_two_discount
from teller import Teller
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


    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 1)

    receipt = teller.checks_out_articles_from(cart)

    assert 0.72 ==  pytest.approx(receipt.total_price(), 0.01)

class TestThreeForTwoDiscount:
    def test_negative_price(self):
        toothbrush = Product("toothbrush", ProductUnit.EACH)
        quantity = 1
        unit_price = -10
        offer = Offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, argument=3.00)
        with pytest.raises(ValueError) as excinfo:
            three_for_two_discount(toothbrush, quantity, unit_price, offer)
        assert str(excinfo.value) == f"Error: Unit price cannot be less than <= 0"

    def test_less_than_two_discount(self):
        toothbrush = Product("toothbrush", ProductUnit.EACH)
        quantity = 1
        # what if unit price is negative number ?
        unit_price = 0.80
        offer = Offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, argument=3.00)
        with pytest.raises(ValueError) as excinfo:
            three_for_two_discount(toothbrush, quantity, unit_price, offer)
        assert str(excinfo.value) == f"Error: Quantity of product {toothbrush.name} must be at least 3 to apply the discount."


class TestFiveForAmountDiscount:
    # what if goes over
    def test_less_than_five_quantity(self):
        toothbrush = Product("toothbrush", ProductUnit.EACH)
        # Define the parameters for the discount function
        quantity = 1
        unit_price = 0.80
        offer = Offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothbrush, argument=3.00)
        # Assert that ValueError is raised
        with pytest.raises(ValueError) as excinfo:
            five_for_amount_discount(toothbrush, quantity, unit_price, offer)
            assert str(excinfo.value) == f"Error: Quantity of product {toothbrush.name} must be at least 5 to apply the discount."

    def test_five_quantity(self):
        toothbrush = Product("toothbrush", ProductUnit.EACH)
        # Define the parameters for the discount function
        quantity = 5
        unit_price = 0.80
        offer = Offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothbrush, argument=3.00)
        discount = five_for_amount_discount(toothbrush, quantity, unit_price, offer)
        assert discount.discount_amount == -1.0

    def test_ten_quantity(self):
        toothbrush = Product("toothbrush", ProductUnit.EACH)
        quantity = 10
        unit_price = 0.80
        offer = Offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothbrush, argument=3.00)
        discount = five_for_amount_discount(toothbrush, quantity, unit_price, offer)
        assert discount.discount_amount == -2.0
    
    def test_twenty_seven_quantity(self):
        toothbrush = Product("toothbrush", ProductUnit.EACH)
        quantity = 27
        unit_price = 0.80
        offer = Offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothbrush, argument=3.0)
        discount = five_for_amount_discount(toothbrush, quantity, unit_price, offer)
        assert discount.discount_amount == -5
