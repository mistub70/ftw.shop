import unittest
from decimal import Decimal
from ftw.shop.tests.base import FtwShopTestCase


class TestVariations(FtwShopTestCase):
    """Here, we test the different variation methods with three items
    that are set up in FtwShopTestCase.afterSetUp():
    movie (no variations), book (one variation) and tshirt (two variations)
    """
    
    def afterSetUp(self):
        super(TestVariations, self).afterSetUp()

    def test_has_variations(self):
        self.assertFalse(self.movie_vc.hasVariations())
        self.assertTrue(self.book_vc.hasVariations())
        self.assertTrue(self.tshirt_vc.hasVariations())

    def test_get_item_uid(self):
        self.assertEquals(self.movie_vc.getItemUID(), self.movie.UID())
        self.assertEquals(self.book_vc.getItemUID(), self.book.UID())
        self.assertEquals(self.tshirt_vc.getItemUID(), self.tshirt.UID())

    def test_get_var1_values(self):
        movie_var1_values = self.movie_vc.getVariation1Values()
        book_var1_values = self.book_vc.getVariation1Values()
        tshirt_var1_values = self.tshirt_vc.getVariation1Values()
        self.assertEquals(movie_var1_values, [])
        self.assertEquals(book_var1_values, ('Hardcover', 'Paperback'))
        self.assertEquals(tshirt_var1_values, ('Red', 'Green', 'Blue'))

    def test_get_var2_values(self):
        movie_var2_values = self.movie_vc.getVariation2Values()
        book_var2_values = self.book_vc.getVariation2Values()
        tshirt_var2_values = self.tshirt_vc.getVariation2Values()
        self.assertEquals(movie_var2_values, [])
        self.assertEquals(book_var2_values, [])
        self.assertEquals(tshirt_var2_values, ('S', 'M', 'L'))

    def test_get_variation_attributes(self):
        movie_var_attrs = self.movie_vc.getVariationAttributes()
        book_var_attrs = self.book_vc.getVariationAttributes()
        tshirt_var_attrs = self.tshirt_vc.getVariationAttributes()
        self.assertEquals(movie_var_attrs, [])
        self.assertEquals(book_var_attrs, ['Cover'])
        self.assertEquals(tshirt_var_attrs, ['Color', 'Size'])

    def test_get_variation_data(self):
        price = self.movie_vc.getVariationData(None, None, 'price')
        stock = self.movie_vc.getVariationData(None, None, 'stock')
        skuCode = self.movie_vc.getVariationData(None, None, 'skuCode')
        active = self.movie_vc.getVariationData(None, None, 'active')
        not_there = self.movie_vc.getVariationData(None, None, 'nonexisting')

        self.assertEquals(price, Decimal('7.15'))
        self.assertEquals(stock, 0)
        self.assertEquals(skuCode, '12345')
        self.assertEquals(active, True)
        self.assertEquals(skuCode, '12345')
        self.assertEquals(not_there, None)

        price = self.book_vc.getVariationData('Paperback', None, 'price')
        stock = self.book_vc.getVariationData('Paperback', None, 'stock')
        skuCode = self.book_vc.getVariationData('Paperback', None, 'skuCode')
        active = self.book_vc.getVariationData('Paperback', None, 'active')
        self.assertEquals(price, Decimal('2.00'))
        self.assertEquals(stock, 2)
        self.assertEquals(skuCode, 'b22')
        self.assertTrue(active)

        price = self.tshirt_vc.getVariationData('Blue', 'S', 'price')
        stock = self.tshirt_vc.getVariationData('Blue', 'S', 'stock')
        skuCode = self.tshirt_vc.getVariationData('Blue', 'S', 'skuCode')
        active = self.tshirt_vc.getVariationData('Blue', 'S', 'active')
        self.assertEquals(price, Decimal('7.00'))
        self.assertEquals(stock, 7)
        self.assertEquals(skuCode, '77')
        self.assertTrue(active)

    def test_get_pretty_name(self):
        self.assertEquals(self.book_vc.getPrettyName('hardcover'), 'Hardcover')
        self.assertEquals(self.tshirt_vc.getPrettyName('blue-s'), 'Blue-S')
        self.assertEquals(self.tshirt_vc.getPrettyName('doesnt-exist'), None)
        
    def test_get_variation_dict(self):
        expected_var_dict = {
        'hardcover': {'active': True, 'price': Decimal('1.00'), 'stock': 1, 'skuCode': 'b11'},
        'paperback': {'active': True, 'price': Decimal('2.00'), 'stock': 2, 'skuCode': 'b22'},
        }
        self.assertEquals(self.book_vc.getVariationDict(), expected_var_dict)

        expected_var_dict = {
        'red-s': {'active': True, 'price': Decimal('1.00'), 'stock': 1, 'skuCode': '11'},
        'red-m': {'active': True, 'price': Decimal('2.00'), 'stock': 2, 'skuCode': '22'}, 
        'red-l': {'active': True, 'price': Decimal('3.00'), 'stock': 3, 'skuCode': '33'},
        'green-s': {'active': True, 'price': Decimal('4.00'), 'stock': 4, 'skuCode': '44'},
        'green-m': {'active': True, 'price': Decimal('5.00'), 'stock': 5, 'skuCode': '55'}, 
        'green-l': {'active': True, 'price': Decimal('6.00'), 'stock': 6, 'skuCode': '66'}, 
        'blue-s': {'active': True, 'price': Decimal('7.00'), 'stock': 7, 'skuCode': '77'}, 
        'blue-m': {'active': True, 'price': Decimal('8.00'), 'stock': 8, 'skuCode': '88'}, 
        'blue-l': {'active': True, 'price': Decimal('9.00'), 'stock': 9, 'skuCode': '99'},
        }
        self.assertEquals(self.tshirt_vc.getVariationDict(), expected_var_dict)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestVariations))
    return suite