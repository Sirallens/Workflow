from share.db_init import db
import models.tables
from app import app


with app.app_context():
  db.create_all()
  db.session.commit()

print("Db created succesfully")

