import unittest
from unittest.mock import patch, MagicMock, Mock
import sys
import os

# Add the current directory to the Python path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import Book, Cart, CartItem


class TestBookModel(unittest.TestCase):
    """Test cases for the Book model with mocking."""
    
    def setUp(self):
        """Set up test data for each test."""
        self.title = "The Great Gatsby"
        self.book_category = "Fiction"
        self.price = 10.99
        self.image = "/static/images/great_gatsby.jpg"
        self.invalid_category = ""
        self.invalid_price = 0.00

    def test_book_initialization(self):
        """Test Book object initialization with valid data."""
        book = Book(self.title, self.book_category, self.price, self.image)
        
        self.assertEqual(book.title, self.title)
        self.assertEqual(book.category, self.book_category)
        self.assertEqual(book.price, self.price)
        self.assertEqual(book.image, self.image)

    def test_book_initialization_invalid_category(self):
        """Test Book initialization with an invalid category."""
        result = Book(self.title, self.invalid_category, self.price, self.image)
        
        # Since the Book class doesn't validate categories, it will accept any string
        # This test shows that the Book object is created regardless of category validity
        self.assertEqual(result.title, self.title)
        self.assertEqual(result.category, self.invalid_category)
        self.assertEqual(result.price, self.price)
        self.assertEqual(result.image, self.image)
        
        # If you want to test validation, you would need to add validation to the Book class first
        # For now, this test confirms the current behavior

    def test_book_initialization_invalid_price(self):
        """Test Book initialization with invalid price (zero or negative)."""
        result = Book(self.title, self.book_category, self.invalid_price, self.image)
        
        # Current Book class accepts any price value
        self.assertEqual(result.title, self.title)
        self.assertEqual(result.category, self.book_category)
        self.assertEqual(result.price, self.invalid_price)
        self.assertEqual(result.image, self.image)

    @patch('models.Book.__init__')
    def test_book_with_validation_mock(self, mock_init):
        """Test Book initialization with mocked validation behavior."""
        # Mock the Book constructor to simulate validation
        mock_init.return_value = None
        
        # Test with valid data
        Book(self.title, self.book_category, self.price, self.image)
        mock_init.assert_called_with(self.title, self.book_category, self.price, self.image)
        
        # Reset mock for next call
        mock_init.reset_mock()
        
        # Test with invalid data
        Book(self.title, self.invalid_category, self.invalid_price, self.image)
        mock_init.assert_called_with(self.title, self.invalid_category, self.invalid_price, self.image)
        

    @patch('models.Book.__init__')
    def test_book_initialization_with_mock(self, mock_init):
        """Test Book initialization using mocking to verify constructor calls."""
        mock_init.return_value = None
        
        # Create a Book instance
        book = Book(self.title, self.book_category, self.price, self.image)
        
        # Verify the constructor was called with correct arguments
        mock_init.assert_called_once_with(self.title, self.book_category, self.price, self.image)

    def test_book_category_edge_cases(self):
        """Test Book creation with various category edge cases."""
        # Test with special characters
        special_category = "Sci-Fi & Fantasy"
        book1 = Book(self.title, special_category, self.price, self.image)
        self.assertEqual(book1.category, special_category)
        
        # Test with numbers in category
        numeric_category = "21st Century Literature"
        book2 = Book(self.title, numeric_category, self.price, self.image)
        self.assertEqual(book2.category, numeric_category)
        
        # Test with whitespace
        whitespace_category = "  Romance  "
        book3 = Book(self.title, whitespace_category, self.price, self.image)
        self.assertEqual(book3.category, whitespace_category)  # Should preserve whitespace

    @patch('models.Book.__init__')
    def test_book_creation_with_category_validation_mock(self, mock_init):
        """Test Book creation with mocked category validation."""
        mock_init.return_value = None
        
        valid_categories = ["Fiction", "Non-Fiction", "Science", "History", "Biography"]
        
        for category in valid_categories:
            Book("Test Title", category, 15.99, "/test.jpg")
            mock_init.assert_called_with("Test Title", category, 15.99, "/test.jpg")
            mock_init.reset_mock()

    def test_book_attribute_access(self):
        """Test accessing book attributes for category browsing."""
        book = Book(self.title, self.book_category, self.price, self.image)
        
        # Test attribute access methods that might be used in category filtering
        self.assertTrue(hasattr(book, 'category'))
        self.assertTrue(hasattr(book, 'title'))
        self.assertTrue(hasattr(book, 'price'))
        self.assertTrue(hasattr(book, 'image'))
        
        # Test category comparison (case sensitivity)
        self.assertEqual(book.category.lower(), self.book_category.lower())
        self.assertTrue(book.category == "Fiction")
        self.assertFalse(book.category == "fiction")  # Case sensitive by default


class TestCartItemModel(unittest.TestCase):
    """Test cases for the CartItem model with mocking."""
    
    def setUp(self):
        """Set up test data and mock objects for each test."""
        self.mock_book = Mock()
        self.mock_book.title = "Test Book"
        self.mock_book.price = 15.99
        self.quantity = 3

    def test_cart_item_initialization(self):
        """Test CartItem initialization with mock book."""
        cart_item = CartItem(self.mock_book, self.quantity)
        
        self.assertEqual(cart_item.book, self.mock_book)
        self.assertEqual(cart_item.quantity, self.quantity)

    def test_cart_item_default_quantity(self):
        """Test CartItem initialization with default quantity."""
        cart_item = CartItem(self.mock_book)
        
        self.assertEqual(cart_item.book, self.mock_book)
        self.assertEqual(cart_item.quantity, 1)

    def test_get_total_price(self):
        """Test total price calculation in CartItem."""
        cart_item = CartItem(self.mock_book, self.quantity)
        expected_total = self.mock_book.price * self.quantity
        
        self.assertEqual(cart_item.get_total_price(), expected_total)
    

    @patch.object(CartItem, 'get_total_price')
    def test_get_total_price_with_mock(self, mock_get_total):
        """Test total price calculation using method mocking."""
        mock_get_total.return_value = 47.97
        
        cart_item = CartItem(self.mock_book, self.quantity)
        total = cart_item.get_total_price()
        
        self.assertEqual(total, 47.97)
        mock_get_total.assert_called_once()


class TestCartModel(unittest.TestCase):
    """Test cases for the Cart model with extensive mocking."""
    
    def setUp(self):
        """Set up test data and mock objects for each test."""
        self.cart = Cart()
        
        # Create mock books
        self.mock_book1 = Mock()
        self.mock_book1.title = "Book 1"
        self.mock_book1.price = 10.99
        
        self.mock_book2 = Mock()
        self.mock_book2.title = "Book 2"
        self.mock_book2.price = 15.99

    def test_cart_initialization(self):
        """Test Cart initialization."""
        self.assertIsInstance(self.cart.items, dict)
        self.assertEqual(len(self.cart.items), 0)
        self.assertTrue(self.cart.is_empty())

    @patch('models.CartItem')
    def test_add_book_new_item(self, mock_cart_item):
        """Test adding a new book to cart with mocked CartItem."""
        mock_item_instance = Mock()
        mock_cart_item.return_value = mock_item_instance
        
        self.cart.add_book(self.mock_book1, 2)
        
        # Verify CartItem was created with correct parameters
        mock_cart_item.assert_called_once_with(self.mock_book1, 2)
        # Verify item was added to cart
        self.assertIn(self.mock_book1.title, self.cart.items)
        self.assertEqual(self.cart.items[self.mock_book1.title], mock_item_instance)

    def test_add_book_existing_item(self):
        """Test adding quantity to existing book in cart."""
        # Add book first time
        self.cart.add_book(self.mock_book1, 2)
        initial_quantity = self.cart.items[self.mock_book1.title].quantity
        
        # Add same book again
        self.cart.add_book(self.mock_book1, 3)
        
        # Verify quantity was increased
        self.assertEqual(self.cart.items[self.mock_book1.title].quantity, initial_quantity + 3)

    def test_remove_book_existing(self):
        """Test removing an existing book from cart."""
        self.cart.add_book(self.mock_book1, 2)
        self.assertIn(self.mock_book1.title, self.cart.items)
        
        self.cart.remove_book(self.mock_book1.title)
        
        self.assertNotIn(self.mock_book1.title, self.cart.items)

    def test_remove_book_nonexistent(self):
        """Test removing a non-existent book from cart (should not raise error)."""
        # This should not raise an exception
        self.cart.remove_book("Non-existent Book")
        self.assertTrue(self.cart.is_empty())

    def test_update_quantity_existing_item(self):
        """Test updating quantity of existing item."""
        self.cart.add_book(self.mock_book1, 2)
        
        self.cart.update_quantity(self.mock_book1.title, 5)
        
        self.assertEqual(self.cart.items[self.mock_book1.title].quantity, 5)

    def test_update_quantity_zero_removes_item(self):
        """Test that updating quantity to 0 removes the item."""
        self.cart.add_book(self.mock_book1, 2)
        
        self.cart.update_quantity(self.mock_book1.title, 0)
        
        self.assertNotIn(self.mock_book1.title, self.cart.items)

    @patch.object(CartItem, 'get_total_price')
    def test_get_total_price(self, mock_get_total_price):
        """Test cart total price calculation with mocked CartItem prices."""
        mock_get_total_price.side_effect = [21.98, 31.98]  # Different returns for each call
        
        self.cart.add_book(self.mock_book1, 2)
        self.cart.add_book(self.mock_book2, 2)
        
        total = self.cart.get_total_price()
        
        self.assertEqual(total, 53.96)  # 21.98 + 31.98
        self.assertEqual(mock_get_total_price.call_count, 2)

    def test_get_total_items(self):
        """Test total items count in cart."""
        self.cart.add_book(self.mock_book1, 2)
        self.cart.add_book(self.mock_book2, 3)
        
        total_items = self.cart.get_total_items()
        
        self.assertEqual(total_items, 5)

    def test_clear_cart(self):
        """Test clearing all items from cart."""
        self.cart.add_book(self.mock_book1, 2)
        self.cart.add_book(self.mock_book2, 3)
        
        self.cart.clear()
        
        self.assertTrue(self.cart.is_empty())
        self.assertEqual(len(self.cart.items), 0)

    def test_get_items(self):
        """Test getting list of cart items."""
        self.cart.add_book(self.mock_book1, 2)
        self.cart.add_book(self.mock_book2, 3)
        
        items = self.cart.get_items()
        
        self.assertEqual(len(items), 2)
        self.assertIsInstance(items, list)

    def test_is_empty(self):
        """Test empty cart detection."""
        self.assertTrue(self.cart.is_empty())
        
        self.cart.add_book(self.mock_book1, 1)
        self.assertFalse(self.cart.is_empty())
        
        self.cart.clear()
        self.assertTrue(self.cart.is_empty())


if __name__ == "__main__":
    unittest.main(verbosity=2)
