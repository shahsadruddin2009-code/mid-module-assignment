from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import Book, Cart
import sys
import time
import logging
from werkzeug.middleware.profiler import ProfilerMiddleware

# Python 3.13+ compatibility fix for sys.getframe
# This fixes AttributeError: module 'sys' has no attribute 'getframe'
if not hasattr(sys, 'getframe') and hasattr(sys, '_getframe'):
    sys.getframe = sys._getframe

app = Flask(__name__)
app.secret_key = 'your_secret_key'   # Required for session management

# Performance monitoring setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enable profiler in debug mode
if app.debug:
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir='./profiles')


# Create a cart instance to manage the cart
cart = Cart()

# Create a global books list to avoid duplication
BOOKS = [
    Book("The Great Gatsby", "Fiction", 10.99, "images/books/the_great_gatsby.jpg"),
    Book("1984", "Dystopia", 8.99, "images/books/1984.jpg"),
    Book("I Ching", "Traditional", 18.99, "images/books/I-Ching.jpg"),
    Book("Moby Dick", "Adventure", 12.49, "images/books/moby_dick.jpg")
]

def get_book_by_title(title):
    """Helper function to find a book by title"""
    return next((book for book in BOOKS if book.title == title), None)


def get_books_by_category(category):
    """Helper function to find books by category"""
    if not category:
        return BOOKS
    return [book for book in BOOKS if book.category.lower() == category.lower()]


def get_all_categories():
    """Helper function to get all unique categories"""
    return list(set(book.category for book in BOOKS))


def log_performance(func):
    """Decorator to log performance metrics for routes"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        logger.info(f"Route {func.__name__} executed in {execution_time:.2f}ms")
        return result
    wrapper.__name__ = func.__name__
    return wrapper


# Performance metrics storage (in-memory for demo)
performance_stats = {
    'request_count': 0,
    'total_response_time': 0,
    'route_stats': {}
}

@app.before_request
def before_request():
    """Log request start time"""
    request.start_time = time.time()
    performance_stats['request_count'] += 1

@app.after_request
def after_request(response):
    """Log response time and collect metrics"""
    if hasattr(request, 'start_time'):
        response_time = (time.time() - request.start_time) * 1000
        performance_stats['total_response_time'] += response_time
        
        # Track per-route statistics
        route = request.endpoint or 'unknown'
        if route not in performance_stats['route_stats']:
            performance_stats['route_stats'][route] = {
                'count': 0,
                'total_time': 0,
                'avg_time': 0
            }
        
        stats = performance_stats['route_stats'][route]
        stats['count'] += 1
        stats['total_time'] += response_time
        stats['avg_time'] = stats['total_time'] / stats['count']
        
        logger.info(f"{request.method} {request.path} - {response.status_code} - {response_time:.2f}ms")
    
    return response


@app.route('/')
def index():
    return render_template('index.html', books=BOOKS, cart=cart)


@app.route('/category/<category_name>')
def browse_by_category(category_name):
    """Route to browse books by category"""
    books_in_category = get_books_by_category(category_name)
    
    if not books_in_category:
        flash(f'No books found in category "{category_name}"!', 'info')
        return redirect(url_for('index'))
    
    categories = get_all_categories()
    return render_template('index.html', books=books_in_category, cart=cart, 
                         current_category=category_name, categories=categories)


@app.route('/categories')
def list_categories():
    """Route to list all available categories"""
    categories = get_all_categories()
    category_counts = {}
    for category in categories:
        category_counts[category] = len(get_books_by_category(category))
    
    return render_template('categories.html', categories=category_counts, cart=cart)


@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    book_title = request.form.get('title')
    
    # Get quantity with more robust validation
    quantity_str = request.form.get('quantity', '1')
    
    # Handle None, empty string, or whitespace-only strings
    if not quantity_str or not quantity_str.strip():
        quantity_str = '1'
    
    try:
        # Strip whitespace and validate
        quantity_str = quantity_str.strip()
        
        # Check for decimal values which would cause invalid literal error
        if '.' in quantity_str:
            flash('Quantity must be a whole number!', 'error')
            return redirect(url_for('index'))
        
        quantity = 1
    except (ValueError, TypeError) as e:
        flash('Invalid quantity! Please enter a valid whole number.', 'error')
        return redirect(url_for('index'))
    
    if quantity < 1:
        flash('Quantity must be at least 1!', 'error')
        return redirect(url_for('index'))

    book = get_book_by_title(book_title)
    
    if book:
        cart.add_book(book, quantity)
        flash(f'Added {quantity} "{book.title}" to cart!', 'success')
    else:
        flash('Book not found!', 'error')

    return redirect(url_for('index'))


@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    book_title = request.form.get('title')
    cart.remove_book(book_title)
    flash(f'Removed "{book_title}" from cart!', 'success')
    return redirect(url_for('view_cart'))


@app.route('/update-cart', methods=['POST'])
def update_cart():
    """
    Update the quantity of a book in the cart.
    This function handles HTTP POST requests to update the quantity of a book in the user's cart.
    If the quantity is set to 0 or less, the book is effectively removed from the cart.
    Args:
        None (uses form data from the request)
    Returns:
        Response: Redirects to the view_cart page after updating the cart.
    Form Parameters:
        title (str): The title of the book to update.
        quantity (int): The new quantity of the book. Defaults to 1.
    Flash Messages:
        - Confirmation of removal if quantity <= 0
        - Confirmation of update otherwise
    """
    book_title = request.form.get('title')
    
    # Get quantity with more robust validation
    quantity_str = request.form.get('quantity', '1')
    
    # Handle None, empty string, or whitespace-only strings
    if not quantity_str or not quantity_str.strip():
        quantity_str = '1'
    
    try:
        # Strip whitespace and validate
        quantity_str = quantity_str.strip()
        
        # Check for decimal values which would cause invalid literal error
        if '.' in quantity_str:
            flash('Quantity must be a whole number!', 'error')
            return redirect(url_for('view_cart'))
        
        # Convert to integer
        quantity = int(quantity_str)
    except (ValueError, TypeError) as e:
        flash('Invalid quantity! Please enter a valid whole number.', 'error')
        return redirect(url_for('view_cart'))
    
    cart.update_quantity(book_title, quantity)
    
    if quantity <= 0:
        flash(f'Removed "{book_title}" from cart!', 'success')
    else:
        flash(f'Updated "{book_title}" quantity to {quantity}!', 'success')
    
    return redirect(url_for('view_cart'))


@app.route('/cart')
def view_cart():
    return render_template('cart.html', cart=cart)


@app.route('/clear-cart', methods=['POST'])
def clear_cart():
    cart.clear()
    flash('Cart cleared!', 'success')
    return redirect(url_for('view_cart'))


@app.route('/checkout')
def checkout():
    if cart.is_empty():
        flash('Your cart is empty!', 'error')
        return redirect(url_for('index'))
    
    total_price = cart.get_total_price()
    return render_template('checkout.html', cart=cart, total_price=total_price)


@app.route('/search')
def search_books():
    """Search for books by title or category"""
    query = request.args.get('query', '').strip()
    
    if not query:
        flash('Please enter a search term!', 'error')
        return redirect(url_for('index'))
    
    # Search in both title and category
    matching_books = []
    query_lower = query.lower()
    
    for book in BOOKS:
        if (query_lower in book.title.lower() or 
            query_lower in book.category.lower()):
            matching_books.append(book)
    
    if matching_books:
        flash(f'Found {len(matching_books)} book(s) for "{query}"', 'success')
    else:
        flash(f'No books found for "{query}"', 'info')
    
    return render_template('index.html', books=matching_books, cart=cart, search_query=query)


@app.route('/metrics')
def performance_metrics():
    """Display performance metrics dashboard"""
    avg_response_time = 0
    if performance_stats['request_count'] > 0:
        avg_response_time = performance_stats['total_response_time'] / performance_stats['request_count']
    
    metrics = {
        'total_requests': performance_stats['request_count'],
        'average_response_time': f"{avg_response_time:.2f}ms",
        'route_statistics': performance_stats['route_stats']
    }
    
    return jsonify(metrics)


@app.route('/dashboard')
def metrics_dashboard():
    """Serve the performance metrics dashboard HTML"""
    return render_template('metrics.html')


@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'uptime': time.time() - app.config.get('START_TIME', time.time())
    })


if __name__ == '__main__':
    app.config['START_TIME'] = time.time()
    app.run(debug=True)