from major.route import db
from main.models import Buyer_user
from werkzeug.security import generate_password_hash

def create_default_admin():
    email = "sakyimustapha5@gmail.com"
    existing_admin = Buyer_user.query.filter_by(email=email).first()

    if not existing_admin:
        admin = Buyer_user(
            firstname="Sakyi",
            lastname="Mustapha",
            email=email,
            password=generate_password_hash("Penfields1"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        print(f"Admin {email} created.")
    else:
        print("Admin already exists.")
