from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mail import Mail, Message
import secrets
import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from dotenv import load_dotenv
from flask_migrate import Migrate
from datetime import timedelta
import razorpay
razorpay_client = razorpay.Client(auth=("rzp_test_is2RgeSGBanvEh", "HV9n88oRKPFhPkHzBFqWWbtO"))
from werkzeug.security import check_password_hash  
from werkzeug.security import generate_password_hash  # Import for password hashing
from werkzeug.utils import secure_filename
from models import db, User, ResetToken, FAQ, Category, Blog, ProductCategory, Subcategory, Brand, Product, RelatedImage, Order, OrderItem,AssistanceApplication,Prescription,RefillRequest,AdminUser
# Load environment variables from .env file
load_dotenv()

myapp = Flask(__name__)

myapp.secret_key = secrets.token_hex(32)
myapp.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://avnadmin:AVNS_5g5JAO_QRXn3sbMwflp@mysql-1744ddf1-mateshital41-5b9c.i.aivencloud.com:22765/medvibe2'
myapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
myapp.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
myapp.config['SESSION_COOKIE_SECURE'] = False  # Change to True if using HTTPS
myapp.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
# Make sure the uploads directory exists
if not os.path.exists(myapp.config['UPLOAD_FOLDER']):
    os.makedirs(myapp.config['UPLOAD_FOLDER'])
#migrate = Migrate(myapp, db)

# Configure email
myapp.config['MAIL_SERVER'] = 'smtp.gmail.com'
myapp.config['MAIL_PORT'] = 465
myapp.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
myapp.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
myapp.config['MAIL_USE_TLS'] = False
myapp.config['MAIL_USE_SSL'] = True

mail = Mail(myapp)
db.init_app(myapp)
# Hash the password and store it securely (in a real app, use a database)
# Initialize Flask-Admin
admin = Admin(myapp, name='Admin Panel', template_mode='bootstrap3')
# Add Model Views to Admin Panel
admin.add_view(ModelView(AdminUser, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(FAQ, db.session))
admin.add_view(ModelView(Blog, db.session))




@myapp.route('/')
def index():
    faqs = FAQ.query.limit(6).all()  # Fetch all the FAQ data
    images = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg','9.jpg']  # Sample images for Home
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
def items():
    return render_template('items.html')

@myapp.route('/contact')
def contact():
    return render_template('contact.html')

@myapp.route('/term_conditions')
def terms_conditions():
    return render_template('term_conditions.html')

@myapp.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')

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

@myapp.route('/prescription')
def prescription():
    return render_template('prescription.html')

@myapp.route('/upload', methods=['POST'])
def upload_prescription():
    if 'email' not in session:
        flash('You must be logged in to request a refill.')
        return redirect(url_for('login'))
    
    if 'prescriptionFile' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['prescriptionFile']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file:
        # Save the file to the designated upload folder
        filepath = os.path.join(myapp.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Save the file information to the database
        new_prescription = Prescription(filename=file.filename, user_email=session['email'])
        db.session.add(new_prescription)
        db.session.commit()

        # Set session variable to indicate the prescription has been uploaded
        session['upload_prescription'] = True

        flash('Prescription uploaded successfully!')
        return redirect(url_for('cart')) 

@myapp.route('/refill', methods=['GET', 'POST'])
def request_refill():
    if request.method == 'POST':
        prescription_number = request.form['refillPrescription']

        # Ensure user is logged in
        if 'email' not in session:
            flash('You must be logged in to request a refill.')
            return redirect(url_for('login'))

        # Fetch the prescription
        prescription = Prescription.query.filter_by(id=prescription_number, user_email=session['email']).first()
        
        if not prescription:
            flash('Prescription not found or you do not have permission to refill this prescription.')
            return redirect(request.url)  # Redirect back to the same page

        # Check refill count
        MAX_REFILLS = 3
        if prescription.refill_count >= MAX_REFILLS:
            flash('Maximum refill limit of 3 reached for this prescription.')
            return render_template('refill.html', prescription=prescription)  # Render the refill page with the prescription

        # Create refill request
        user_email = session['email']  # Get email from session
        new_refill_request = RefillRequest(prescription_id=prescription.id, user_email=user_email)
        
        # Try to add the refill request to the database
        try:
            db.session.add(new_refill_request)
            prescription.refill_count += 1  # Increment refill count
            db.session.commit()
            flash('Refill request submitted successfully.')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while submitting your refill request: {}'.format(str(e)))

        return redirect(url_for('view_refills'))

    # Handle GET request logic here if needed
    return render_template('refill.html')  # Render the refill page for GET requests



@myapp.route('/view_prescriptions')
def view_prescriptions():
    # Check if user is logged in
    if 'email' not in session:
        flash('You need to log in to view your prescriptions.', 'warning')
        return redirect(url_for('login'))

    user_email = session['email']  # Get the logged-in user's email

    # Fetch prescriptions for the logged-in user
    prescriptions = Prescription.query.filter_by(user_email=user_email).all()
    return render_template('view_prescriptions.html', prescriptions=prescriptions)

@myapp.route('/view_refills')
def view_refills():
    # Check if user is logged in
    if 'email' not in session:
        flash('You need to log in to view your refill requests.', 'warning')
        return redirect(url_for('login'))

    user_email = session['email']  # Get the logged-in user's email

    # Fetch refill requests for the logged-in user
    refill_requests = RefillRequest.query.filter_by(user_email=user_email).all()
    return render_template('view_refills.html', refill_requests=refill_requests)


@myapp.route('/return')  # Add the slash here
def returns_policy():
    return render_template('return.html')

@myapp.route('/FAQ')
def faq():
    faqs = FAQ.query.all()  # This should fetch all the FAQ data
    return render_template('FAQ.html', faqs=faqs)

@myapp.route('/footer')
def Footer():
    return render_template("footer.html")

@myapp.route('/upload')
def upload():
    return render_template('upload.html')

@myapp.route('/brand')
def brand():
    return render_template('brand.html')

@myapp.route('/userprofilenavbar')
def userp():
    return render_template("userprofilenavbar.html")

@myapp.route('/financial_assistance', methods=['GET', 'POST'])
def financial_assistance():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        income = request.form['household_income']
        medication = request.form['medication']
        document = request.files['supporting_document']

        # Handle file upload
        if document:
            filename = secure_filename(document.filename)
            filepath = os.path.join(myapp.config['UPLOAD_FOLDER'], filename)
            document.save(filepath)
        else:
            filepath = None

        # Create new application instance
        new_application = AssistanceApplication(
            name=name,
            email=email,
            phone=phone,
            household_income=float(income),  # Convert to float
            medication=medication,
            supporting_documents=filepath
        )

        # Store data in the database
        db.session.add(new_application)
        db.session.commit()

        flash('Your application has been submitted successfully!', 'success')
        return redirect(url_for('financial_assistance'))

    return render_template('financial_assistance.html')


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
            session['phone'] = user.phone
            session['address'] = user.address
            session['city'] = user.city
            session['state'] = user.state
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
    selected_category = request.args.get('product_category', type=int)
    category_range = request.args.get('category_range')  # New: Get category range if specified
    selected_subcategory = request.args.get('subcategory', type=int)
    selected_brand = request.args.get('brand', type=int)
    selected_price = request.args.get('price')  # Get the selected price range

    # Base query to get all products
    query = Product.query

    # New: Apply filters for category range (e.g., 1-6, 7-11, or 16-29)
    if category_range:
        range_start, range_end = map(int, category_range.split('-'))
        query = query.filter(Product.category_id.between(range_start, range_end))

    # Apply filters based on selected category, subcategory, brand, and price
    elif selected_category:  # Priority given to category_range, if present
        query = query.filter(Product.category_id == selected_category)

    if selected_subcategory:
        query = query.filter(Product.subcategory_id == selected_subcategory)
    if selected_brand:
        query = query.filter(Product.brand_id == selected_brand)
    if selected_price:
        price_range = selected_price.split('-')
        if len(price_range) == 2:
            min_price = float(price_range[0])
            max_price = float(price_range[1])
            query = query.filter(Product.mrp >= min_price, Product.mrp <= max_price)

    products = query.paginate(page=request.args.get('page', 1, type=int), per_page=20)

    # Fetch subcategories and brands based on the selected category range
    if category_range:
        range_start, range_end = map(int, category_range.split('-'))
        if range_start == 1:  # Categories 1-6
            subcategories = Subcategory.query.filter(Subcategory.category_id.between(1, 6)).all()
            brands = Brand.query.filter(Brand.category_id.between(1, 6)).all()
        elif range_start == 7:  # Categories 7-11
            subcategories = Subcategory.query.filter(Subcategory.category_id.between(7, 15)).all()
            brands = Brand.query.filter(Brand.category_id.between(7, 15)).all()
        elif range_start == 16:  # Categories 16-29
            subcategories = Subcategory.query.filter(Subcategory.category_id.between(16, 29)).all()
            brands = Brand.query.filter(Brand.category_id.between(16, 29)).all()
    elif selected_category is not None:
        if selected_category <= 6:  # Categories 1 to 6
            subcategories = Subcategory.query.filter_by(category_id=selected_category).all()
            brands = []  # We will show brands after a subcategory is selected
        elif selected_category >= 7:  # Categories 7 and after
            subcategories = []
            brands = Brand.query.filter(Brand.category_id == selected_category).all()
    else:
        subcategories = []
        brands = Brand.query.all()

    # If a subcategory is selected, fetch related brands
    if selected_subcategory:
        brands = Brand.query.filter_by(subcategory_id=selected_subcategory).all()
        
    categories = ProductCategory.query.all()
    

    return render_template('products.html', products=products, categories=categories,
                           subcategories=subcategories, brands=brands,
                           selected_category=selected_category,
                           selected_subcategory=selected_subcategory,
                           selected_brand=selected_brand,
                           selected_price=selected_price)  # Pass selected_price to template

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
    # Fetch the product from the database
    product = Product.query.get_or_404(product_id)

    # Get the quantity from the form submission
    quantity = int(request.form['quantity'])

    # Retrieve cart from session or initialize an empty one
    cart_items = session.get('cart', {})

    # Add the product to the cart or update the quantity
    product_id_str = str(product_id)
    if product_id_str in cart_items:
        cart_items[product_id_str] += quantity
    else:
        cart_items[product_id_str] = quantity

    # Save the updated cart in the session
    session['cart'] = cart_items

    flash(f"{product.name} added to cart!", "success")
    return redirect(url_for('cart'))


@myapp.route('/cart')
def cart():
    # Ensure user is logged in
    if 'email' not in session:  # Replace 'email' with the key you use for session tracking
        flash('Please log in to view your cart.', 'warning')
        return redirect(url_for('login'))  # Redirect to your login route

    # Retrieve the cart from the session
    cart_items = session.get('cart', {})
    
    # No items in cart
    if not cart_items:
        return render_template('cart.html', cart_details=None, total_amount=0)

    # Retrieve product IDs from cart
    product_ids = [int(pid) for pid in cart_items.keys()]
    
    # Fetch products from the database
    products = Product.query.filter(Product.id.in_(product_ids)).all()
    
    # Prepare cart details and calculate total amount
    cart_details = []
    total_amount = 0

    for product in products:
        quantity = cart_items[str(product.id)]
        subtotal = product.mrp * (1 - (product.discount or 0) / 100) * quantity
        total_amount += subtotal

        cart_details.append({
            'id': product.id,
            'name': product.name,
            'quantity': quantity,
            'mrp': product.mrp,
            'discount': product.discount,
            'subtotal': round(subtotal, 2),
            'image_filename': product.image_filename,
            'prescription_required' : product.prescription_required        
        })

    # Render the cart template with cart details
    return render_template('cart.html', cart_details=cart_details, total_amount=round(total_amount, 2))




@myapp.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    session['cart'] = cart
    session.modified = True  # Mark session as modified

    return redirect(url_for('cart'))


@myapp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # Check if user is authenticated
    if 'email' not in session:  # Ensure user is logged in
        flash('Please log in to place an order.', 'warning')
        return redirect(url_for('login'))  # Adjust 'login' to your login route name

    # Get user data from session
    user_profile = {
        'name': session.get('name', ''),
        'email': session.get('email', ''),
        'phone': session.get('phone', ''),
        'address': session.get('address', ''),
        'city': session.get('city', ''),
        'state': session.get('state', ''),
        'zip_code': session.get('zip_code', ''),
    }

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
        
        payment_method = request.form.get('payment_method')
        razorpay_payment_id = request.form.get('razorpay_payment_id')

        # Create a new Order instance
        order = Order(user_email=email, total_amount=total_price, name=name)
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

        # Check the payment method
        if payment_method == 'razorpay' and razorpay_payment_id:
            order.payment_id = razorpay_payment_id
            order.status = 'Paid'  # Payment successful
        else:
            order.status = 'Pending'  # Cash on Delivery

        db.session.commit()  # Commit all changes

        # Clear the cart after placing the order
        session.pop('cart', None)

        # Display success message and redirect to confirmation page
        flash('Your order has been placed successfully!', 'success')
        return redirect(url_for('order_confirmation', order_id=order.id))

    # Render checkout page with user profile, products, and total price
    return render_template('checkout.html', 
                           products=products, 
                           total_price=total_price, 
                           cart_items=cart_items, 
                           user=user_profile)


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

@myapp.route('/order_history', methods=['GET'])
def order_history():
    # Check if user is authenticated
    if 'email' not in session:  # Ensure user is logged in
        flash('Please log in to view your order history.', 'warning')
        return redirect(url_for('login'))  # Adjust 'login' to your login route name

    # Fetch orders for the logged-in user
    user_email = session['email']
    orders = Order.query.filter_by(user_email=user_email).all()

    return render_template('order_history.html', orders=orders)


@myapp.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    quantity = request.form.get('quantity', type=int)

    if quantity is None:
        return jsonify({'error': 'Quantity is required.'}), 400

    item_product = Product.query.get(product_id)  # Fetch the product

    if not item_product:
        return jsonify({'error': 'Product not found.'}), 404

    available_stock = item_product.stock
    cart_items = session.get('cart', {})

    if quantity > available_stock:
        return jsonify({'error': f'Only {available_stock} items available in stock.'}), 400

    if quantity <= 0:
        cart_items.pop(str(product_id), None)
    else:
        cart_items[str(product_id)] = quantity

    session['cart'] = cart_items

    # Calculate total amount using mrp instead of price
    total_amount = 0
    for item_id, qty in cart_items.items():
        item_product = Product.query.get(item_id)
        if item_product:
            total_amount += item_product.mrp * qty  # Use MRP to calculate total

    return jsonify({'total_amount': round(total_amount, 2)}), 200



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

        
        return jsonify(suggestions)
    return jsonify([])  # Return an empty list if no query

@myapp.route('/medicines', methods=['GET'])
def medicine_list():
    letter = request.args.get('letter', 'A')
    page = int(request.args.get('page', 1))  # Handle pagination, default to page 1
    per_page = 10  # Number of items per page

    if letter == '0-9':
        medicines_query = Product.query.filter(Product.id >= 73, Product.name.op('REGEXP')('^[0-9]'))
    else:
        medicines_query = Product.query.filter(Product.id >= 73, Product.name.like(f'{letter}%'))

    # Pagination logic
    medicines_paginated = medicines_query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'medicine_list.html',
        medicines=medicines_paginated.items,
        active_letter=letter,
        current_page=page,
        total_pages=medicines_paginated.pages,
    )


@myapp.route('/medicine/<int:id>')
def medicine_detail(id):
    # Fetch the medicine from the database by its ID
    medicine = Product.query.get_or_404(id)  # Assuming the 'Product' model is used

    # Generate available quantities based on the stock
    if medicine.stock > 0:
        available_quantities = list(range(1, medicine.stock + 1))  # e.g., [1, 2, ..., stock]
    else:
        available_quantities = []  # No stock available

    # Get the selected quantity from query parameters (defaults to 1)
    added_quantity = request.args.get('added_quantity', default=1, type=int)

    # Fetch related images
    related_images = RelatedImage.query.filter_by(product_id=id).all()  # Adjust this query based on your model structure

    # Render the medicine detail template with the required data
    return render_template(
        'medicine_detail.html', 
        medicine=medicine, 
        available_quantities=available_quantities, 
        added_quantity=added_quantity,
        related_images=related_images  # Pass related images to the template
    )


if __name__ == '__main__':
    myapp.run(host='0.0.0.0', port=5000, debug=True)