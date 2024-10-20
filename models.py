from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(10), nullable=True)  # Adjust length as needed
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=True)  # Use Text for longer addresses

# Admin Model
class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)



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
    prescription_required = db.Column(db.Boolean, nullable=True)  # Nullable Boolean field
    
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


class AssistanceApplication(db.Model):
    __tablename__ = 'assistance_applications'

    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing primary key
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    household_income = db.Column(db.Float, nullable=False)  # Adjust type based on your needs
    medication = db.Column(db.String(200), nullable=False)
    supporting_documents = db.Column(db.String(200), nullable=True)  # Path to the uploaded file

    def __repr__(self):
        return f'<AssistanceApplication {self.name}, {self.email}>'
    
class Prescription(db.Model):
    __tablename__ = 'prescriptions'

    id = db.Column(db.Integer, primary_key=True)  # Unique ID
    filename = db.Column(db.String(255), nullable=False)  # Prescription file name
    upload_date = db.Column(db.DateTime, default=db.func.now())  # Upload timestamp
    refill_count = db.Column(db.Integer, default=0)  # Number of refills
    user_email = db.Column(db.String(120), nullable=False)  # Email of the user who uploaded the prescription

    # Relationship with RefillRequest
    refills = db.relationship('RefillRequest', backref='prescription', lazy=True, cascade="all, delete")

    def __repr__(self):
        return f"<Prescription(id={self.id}, filename={self.filename}, refill_count={self.refill_count}, user_email={self.user_email})>"

class RefillRequest(db.Model):
    __tablename__ = 'refill_requests'

    id = db.Column(db.Integer, primary_key=True)  # Unique ID
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescriptions.id'), nullable=False)  # FK to Prescription
    request_date = db.Column(db.DateTime, default=db.func.now())  # Request timestamp
    status = db.Column(db.String(50), default='Pending')  # Refill status (Pending, Approved, Rejected)
    user_email = db.Column(db.String(120), nullable=False)  # Email of the user who requested the refill

    def __repr__(self):
        return f"<RefillRequest(id={self.id}, prescription_id={self.prescription_id}, status={self.status}, user_email={self.user_email})>"
