from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mail import Mail, Message
import secrets
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta
from datetime import datetime
from werkzeug.security import check_password_hash  # Make sure to use hashed passwords
from werkzeug.security import generate_password_hash  # Import for password hashing
# Load environment variables from .env file
load_dotenv()

myapp = Flask(__name__)

@myapp.route('/')
def index():
    faqs = FAQ.query.limit(6).all()  # Fetch all the FAQ data

    images = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg']  # Sample images for Home
    
    return render_template("index.html", faqs=faqs, images=images)

@myapp.route('/main')
def main():
    categories = Category.query.all()  # Fetch all categories
    category_blogs = {}
    for category in categories:
        category_blogs[category.id] = Blog.query.filter_by(category_id=category.id).limit(5).all()

    separate_blogs = Blog.query.filter_by(category_id=None).limit(11).all()

    return render_template("main.html", categories=categories, category_blogs=category_blogs, separate_blogs=separate_blogs)


   

@myapp.route('/layout')
def lay():
    return render_template("layout.html")

@myapp.route('/items')
def index():
    return render_template('items.html')

@myapp.route('/contact')
def contact():
    return render_template('contact.html')

@myapp.route('/testimonals')
def testimonials():
    return render_template("testimonals.html")

@myapp.route('/aboutAs')
def about():
    return render_template("aboutAs.html")

@myapp.route('/location')
def location():
    return render_template("location.html")

@myapp.route('/category/<int:category_id>')
def category_detail(category_id):
    category = Category.query.get_or_404(category_id)
    user = Blog.query.filter_by(category_id=category_id).all()
    return render_template('main.html', category=category, user=user)

@myapp.route('/blog/<int:blog_id>')
def blog_detail(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    return render_template('main.html', blog=blog)


@myapp.route('/FAQ')
def faq():
    faqs = FAQ.query.all()  # This should fetch all the FAQ data
    return render_template('FAQ.html', faqs=faqs)

@myapp.route('/footer')
def Footer():
    return render_template("footer.html")

@myapp.route('/userprofilenavbar')
def userp():
    return render_template("userprofilenavbar.html")



myapp.secret_key = secrets.token_hex(32)

myapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
myapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
myapp.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
myapp.config['SESSION_COOKIE_SECURE'] = False  # Change to True if using HTTPS

db = SQLAlchemy(myapp)
migrate = Migrate(myapp, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(10), nullable=True)  # Adjust length as needed
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=True)  # Use Text for longer addresses

class ResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.Text, nullable=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image_filename = db.Column(db.String(100))  # Image for the category
    blogs = db.relationship('Blog', backref='category', lazy=True)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(100))  # Blog image
    detail_page = db.Column(db.Text, nullable=False)  # Full content
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    # category_id can be NULL for the separate 11 blogs

class ProductCategory(db.Model):
    __tablename__ = 'product_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subcategories = db.relationship('Subcategory', backref='product_category', lazy=True)
    products = db.relationship('Product', backref='product_category', lazy=True)

    def __repr__(self):
        return f'<ProductCategory {self.name}>'
    
class Subcategory(db.Model):
    __tablename__ = 'subcategory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'), nullable=False)
    products = db.relationship('Product', backref='subcategory', lazy=True)

class Brand(db.Model):
    __tablename__ = 'brand'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'), nullable=True)  # Foreign key to Category
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=True)  # Foreign key to Subcategory
    products = db.relationship('Product', backref='brand', lazy=True)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mrp = db.Column(db.Float, nullable=False)  # Add MRP field
    discount = db.Column(db.Float, nullable=True)  # Discount percentage
    description = db.Column(db.String(500), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=True)
    image_filename = db.Column(db.String(100), nullable=True)
    stock = db.Column(db.Integer, nullable=False, default=0)  # Add stock field
    benefits = db.Column(db.Text, nullable=True)  # New field for benefits
    directions = db.Column(db.Text, nullable=True)  # New field for directions
    features = db.Column(db.Text, nullable=True)  # New field for features
    safety_information = db.Column(db.Text, nullable=True)  # Optional field for safety information
    country_of_origin = db.Column(db.String(100), nullable=True)  # Country of origin field
    manufacturer = db.Column(db.String(100), nullable=True)        # Manufacturer field
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
class RelatedImage(db.Model):
    __tablename__ = 'related_images'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    image_filename = db.Column(db.String(100), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(100))  # Add this line to store the name
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    __tablename__ = 'OrderItem'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

# Configure email
myapp.config['MAIL_SERVER'] = 'smtp.gmail.com'
myapp.config['MAIL_PORT'] = 465
myapp.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
myapp.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
myapp.config['MAIL_USE_TLS'] = False
myapp.config['MAIL_USE_SSL'] = True

mail = Mail(myapp)

def send_reset_email(email, token):
    msg = Message('Password Reset Request',
                  sender=os.getenv('MAIL_USERNAME'),
                  recipients=[email])
    
    reset_url = url_for('reset_password', token=token, _external=True)
    reset_url = reset_url.replace('127.0.0.1','192.168.0.0.102')
    msg.body = f'''To reset your password, visit the following link:
{reset_url}

If you did not make this request, simply ignore this email.
'''
    mail.send(msg)


@myapp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        phone = request.form['phone']
        city = request.form['city']
        state = request.form['state']
        address = request.form['address']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return render_template('register.html')  # Return to the registration page

        # Check for existing user
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please choose a different one.', 'danger')
            return render_template('register.html')  # Return to the registration page

        # Hash the password for security
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')


        # Create a new user
        new_user = User(
            email=email,
            password=hashed_password,  # Store hashed password
            phone=phone,
            city=city,
            state=state,
            address=address
        )
        
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@myapp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()  # Fetch user by email

        if user and check_password_hash(user.password, password):  # Check hashed password
            session['email'] = user.email  # You may not need this if using Flask-Login
            return redirect(url_for('profile'))  # Redirect to the profile page
        else:
            flash('email or password is wrong. Please try again.', 'danger')
    return render_template('login.html')

@myapp.route('/userprofile', methods=['GET', 'POST'])
def profile():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    user = User.query.filter_by(email=session['email']).first()
    
    if request.method == 'POST':
        user.email = request.form['email']
        user.phone = request.form['phone']
        user.address = request.form['address']
        user.state = request.form['state']
        user.city = request.form['city']

        db.session.commit()  # Save changes to the database
        flash('Profile updated successfully!')  # Show a success message
        return redirect(url_for('profile'))  # Redirect back to the profile page
    
    # Render the profile page with the user data
    return render_template('userprofile.html', user=user)


@myapp.route('/logout')
def logout():
    session.pop('email', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@myapp.before_request
def make_session_permanent():
    session.permanent = True
    session.modified = True  # Mark the session as modified

@myapp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        
        if user:
            token = secrets.token_urlsafe()
            reset_token = ResetToken(token=token, user_id=user.id)
            db.session.add(reset_token)
            db.session.commit()
            send_reset_email(email, token)
            flash('Password reset link has been sent to your email!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Email not found.', 'danger')
    return render_template('forgot_password.html')


@myapp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    reset_token = ResetToken.query.filter_by(token=token).first()
    if not reset_token:
        flash('Invalid or expired token.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']
        if new_password == confirm_password:
            user = User.query.get(reset_token.user_id)
            if user:
                user.password = new_password
                db.session.delete(reset_token)  # Invalidate the used token
                db.session.commit()
                flash('Your password has been reset successfully!', 'success')
                return redirect(url_for('login'))
            flash('Invalid or expired token.', 'danger')
        else:
            flash('Passwords do not match. Please try again.', 'danger')

    
    return render_template('reset_password.html', token=token)


@myapp.route('/catalog')
def products():
    categories = ProductCategory.query.all()
    subcategories = Subcategory.query.all()
    brands = Brand.query.all()

    # Fetch filter values from query parameters
    selected_category = request.args.get('product_category')
    selected_subcategory = request.args.get('subcategory')
    selected_brand = request.args.get('brand')
    selected_price = request.args.get('price')

    products_query = Product.query

    # Filter products based on selected criteria
    if selected_category:
        products_query = products_query.filter_by(category_id=selected_category)
    if selected_subcategory:
        products_query = products_query.filter_by(subcategory_id=selected_subcategory)
    if selected_brand:
        products_query = products_query.filter_by(brand_id=selected_brand)
    if selected_category:
        brands = Brand.query.filter_by(category_id=selected_category).all()
    # Alternatively, you can filter based on subcategory
   
    
    price_range = request.args.get('price')
    if price_range:
        min_price, max_price = map(float, price_range.split('-'))
        products_query = products_query.filter(Product.mrp >= min_price,
                                               Product.mrp <= max_price)
    # Pagination
    page = request.args.get('page', 1, type=int)  # Get current page, default to 1
    per_page = 10  # Number of products per page
    products = products_query.paginate(page=page, per_page=per_page)  # Paginate the products

    return render_template('products.html', categories=categories,
                           subcategories=subcategories, brands=brands,
                           products=products)

@myapp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get(product_id)
    related_images = RelatedImage.query.filter_by(product_id=product_id).all()

    if product and product.stock > 0:
        # Create a list of available quantities based on stock
        available_quantities = list(range(1, product.stock + 1))  # e.g., [1, 2, ..., stock]
    else:
        available_quantities = []  # No available quantities if stock is 0 or product not found


    added_quantity = request.args.get('added_quantity', default=1, type=int)
    return render_template('product_detail.html', product=product, related_images=related_images,available_quantities=available_quantities,added_quantity=added_quantity)

@myapp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form['quantity'])
    cart_items = session.get('cart', {})

    print(f"Adding product {product_id} with quantity {quantity}")  # Debugging line

    product_id_str = str(product_id)
    if product_id_str in cart_items:
        cart_items[product_id_str] += quantity
    else:
        cart_items[product_id_str] = quantity

    session['cart'] = cart_items
    print(f"Current cart items: {session['cart']}")  # Debugging line
    
    return redirect(url_for('cart'))

@myapp.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    product_ids = list(map(int, cart_items.keys()))
    products = Product.query.filter(Product.id.in_(product_ids)).all()

    total_price = 0
    for product in products:
        quantity = cart_items[str(product.id)]
        discounted_price = product.mrp * (1 - (product.discount or 0) / 100)
        total_price += discounted_price * quantity

    if 'email' not in session:
        flash('Please log in to access your cart.', 'danger')
        return redirect(url_for('login'))  # Redirect to login if not logged in    

    return render_template('cart.html', products=products, cart_items=cart_items, total_price=total_price)



@myapp.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart_items = session.get('cart', {})
    if str(product_id) in cart_items:  # Convert product_id to string
        del cart_items[str(product_id)]  # Remove product from cart
        session['cart'] = cart_items
    return redirect(url_for('cart'))

from flask import session, request, redirect, url_for, flash, render_template

@myapp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # Check if user is authenticated
    if 'email' not in session:  # Ensure user is logged in
        flash('Please log in to place an order.', 'warning')
        return redirect(url_for('login'))  # Adjust 'login' to your login route name

    # Get the cart items from the session
    cart_items = session.get('cart', {})
    total_price = 0
    products = []

    if cart_items:
        # Get products in the cart
        products = Product.query.filter(Product.id.in_(cart_items.keys())).all()

        # Calculate the total price
        total_price = calculate_total_price(products, cart_items)

    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = session['email']  # Use the email from the session
        phone = request.form['phone']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']

        # Create a new Order instance
        order = Order(user_email=email, total_amount=total_price,name=name)
        db.session.add(order)
        db.session.flush()  # Flush to get the order ID for the items

        # Add order items
        for product in products:
            quantity = cart_items.get(str(product.id), 0)
            if quantity > 0:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    product_name=product.name,
                    quantity=quantity,
                    price=product.mrp * (1 - (product.discount or 0) / 100),
                    total=quantity * (product.mrp * (1 - (product.discount or 0) / 100))
                )
                db.session.add(order_item)

        db.session.commit()  # Commit all changes

        # Clear the cart after placing the order
        session.pop('cart', None)

        # Display success message and redirect to confirmation page
        flash('Your order has been placed successfully! Cash on Delivery.', 'success')
        return redirect(url_for('order_confirmation', order_id=order.id))

    # Render checkout page with products and total price
    return render_template('checkout.html', products=products, total_price=total_price, cart_items=cart_items)

def calculate_total_price(products, cart_items):
    """Helper function to calculate the total price based on cart items and discounts."""
    total = 0
    for product in products:
        quantity = cart_items.get(str(product.id), 0)
        price = product.mrp * (1 - ((product.discount or 0) / 100))  # Apply discount if available
        total += price * quantity
    return total


@myapp.route('/order_confirmation/<int:order_id>')
def order_confirmation(order_id):
    order = Order.query.get(order_id)
    

    if not order:
        flash('No order found!', 'warning')
        return redirect(url_for('checkout'))

    # Get order items
    order_items = OrderItem.query.filter_by(order_id=order.id).all()

    return render_template(
        'order_confirmation.html', 
        email=order.user_email,  # You may need to extract the user's name separately if you have it
        products=order_items,
        total_price=order.total_amount,
        order_id=order_id,
        name=order.name
    )



@myapp.route('/update_cart/<int:product_id>/<int:quantity>', methods=['POST'])
def update_cart(product_id, quantity):
    cart_items = session.get('cart', {})
    
    if quantity <= 0:
        cart_items.pop(str(product_id), None)  # Remove product from cart if quantity is 0
    else:
        cart_items[str(product_id)] = quantity  # Update quantity

    session['cart'] = cart_items  # Save changes to session
    return '', 204  # No content response


@myapp.route('/search_suggestions', methods=['GET'])
def search_suggestions():
    query = request.args.get('q', '')  # Get the search query from the URL parameter
    if query:
        # Query the database for products whose name matches the search query
        products = Product.query.filter(Product.name.ilike(f'%{query}%')).limit(10).all()

        # Format the results as a list of dictionaries (name, category, subcategory)
        suggestions = []
        for product in products:
            category = ProductCategory.query.get(product.category_id)
            subcategory = Subcategory.query.get(product.subcategory_id)
            suggestions.append({
                'id': product.id,
                'name': product.name,
                'category': category.name if category else '',
                'subcategory': subcategory.name if subcategory else ''
            })

        # Return the suggestions as a JSON response
        return jsonify(suggestions)
    return jsonify([])  # Return an empty list if no query


if __name__ == '__main__':
    myapp.run(host='0.0.0.0', port=5000, debug=True)