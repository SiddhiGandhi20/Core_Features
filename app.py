from flask import Flask
from flask_pymongo import PyMongo
from config import Config
from routes.auth_routes import create_auth_routes  # Existing Sign-Up routes
from routes.signin_routes import create_signin_routes 
from routes.beds_routes import create_beds_routes
from routes.coffee_tables_routes import create_coffee_table_routes
from routes.sofas_routes import create_sofa_routes
from routes.wall_lamp_routes import create_wall_lamp_routes
from routes.table_lamp_routes import create_table_lamp_routes
from routes.wall_decor_routes import create_wall_decor_routes
from routes.category_routes import create_category_routes  # New category route
from routes.product_routes import create_product_routes
from routes.order_routes import create_order_routes
from routes.cart_wishlist_routes import create_cart_routes



# New Sign-In routes

app = Flask(__name__)

# Load MongoDB configuration
app.config.from_object(Config)
mongo = PyMongo(app)

# Register routes
app.register_blueprint(create_auth_routes(mongo.db))  # Existing Sign-Up routes
app.register_blueprint(create_signin_routes(mongo.db)) 
app.register_blueprint(create_beds_routes(mongo.db))
app.register_blueprint(create_coffee_table_routes(mongo.db))
app.register_blueprint(create_sofa_routes(mongo.db))
app.register_blueprint(create_wall_lamp_routes(mongo.db))
app.register_blueprint(create_table_lamp_routes(mongo.db))
app.register_blueprint(create_wall_decor_routes(mongo.db))
app.register_blueprint(create_category_routes(mongo.db))  # Category routes
app.register_blueprint(create_product_routes(mongo.db))
app.register_blueprint(create_order_routes(mongo.db))
cart_bp, wishlist_bp = create_cart_routes(mongo.db)
app.register_blueprint(cart_bp)
app.register_blueprint(wishlist_bp)


if __name__ == "__main__":
    app.run(debug=True)
