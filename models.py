from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association table between Meal and Ingredient (many-to-many)

# Association object for Meal and Ingredient with grams
class MealIngredient(db.Model):
    __tablename__ = 'meal_ingredient'
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    grams = db.Column(db.Float, nullable=False, default=100)

    meal = db.relationship('Meal', back_populates='meal_ingredients')
    ingredient = db.relationship('Ingredient')





class Meal(db.Model):
    __tablename__ = 'meal'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    recipe = db.Column(db.Text, nullable=True)
    time_minutes = db.Column(db.Integer, nullable=True)

    meal_ingredients = db.relationship('MealIngredient', back_populates='meal', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Meal {self.name}>"



class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    calories = db.Column(db.Float, nullable=True)  # per 100g
    protein = db.Column(db.Float, nullable=True)   # per 100g
    fat = db.Column(db.Float, nullable=True)       # per 100g
    carbs = db.Column(db.Float, nullable=True)     # per 100g

    def __repr__(self):
        return f"<Ingredient {self.name}>"
