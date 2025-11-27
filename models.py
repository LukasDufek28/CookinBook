from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association table between Meal and Ingredient (many-to-many)
meal_ingredient = db.Table(
    'meal_ingredient',
    db.Column('meal_id', db.Integer, db.ForeignKey('meal.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True),
)


class Meal(db.Model):
    __tablename__ = 'meal'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    recipe = db.Column(db.Text, nullable=True)
    time_minutes = db.Column(db.Integer, nullable=True)

    ingredients = db.relationship('Ingredient', secondary=meal_ingredient, backref='meals')

    def __repr__(self):
        return f"<Meal {self.name}>"


class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Ingredient {self.name}>"
