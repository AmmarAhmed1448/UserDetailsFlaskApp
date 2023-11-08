from app import app, db
with app.app_context():
    # Create the database tables
    db.create_all()
