
import os
from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from models import db, Meal, Ingredient


def create_app():
    app = Flask(__name__, static_folder='static')

    # Configure database: prefer DATABASE_URL env var (use pymysql for MySQL), otherwise fallback to sqlite
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cookbook.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.route('/')
    def index():
        meals = Meal.query.all()
        return render_template('index.html', meals=meals)

    @app.route('/meal/<int:meal_id>')
    def meal_detail(meal_id):
        meal = Meal.query.get(meal_id)
        if not meal:
            abort(404)

        # Sum nutrition values for all ingredients in the meal based on grams
        total_nutrition = {'calories': 0, 'protein': 0, 'fat': 0, 'carbs': 0}
        for mi in meal.meal_ingredients:
            ing = mi.ingredient
            grams = mi.grams or 0
            total_nutrition['calories'] += (ing.calories or 0) * grams / 100
            total_nutrition['protein'] += (ing.protein or 0) * grams / 100
            total_nutrition['fat'] += (ing.fat or 0) * grams / 100
            total_nutrition['carbs'] += (ing.carbs or 0) * grams / 100

        return render_template('meal.html', meal=meal, total_nutrition=total_nutrition)


    @app.route('/meal/new', methods=['GET', 'POST'])
    def create_meal():
        from flask import request, redirect, url_for

        error = None
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            image_url = request.form.get('image_url', '').strip() or '/static/placeholder.svg'
            time_minutes = request.form.get('time_minutes', '').strip()
            recipe = request.form.get('recipe', '').strip()

            ingredient_ids = request.form.getlist('ingredients')

            if not name or not time_minutes or not recipe:
                error = 'Please fill in all required fields.'
            else:
                try:
                    from models import MealIngredient
                    meal = Meal(
                        name=name,
                        image_url=image_url,
                        time_minutes=int(time_minutes),
                        recipe=recipe,
                    )
                    if ingredient_ids:
                        for ing_id in ingredient_ids:
                            grams_val = request.form.get(f'grams_{ing_id}', '0').strip()
                            grams = float(grams_val) if grams_val else 0
                            if grams > 0:
                                ingredient = Ingredient.query.get(int(ing_id))
                                meal.meal_ingredients.append(MealIngredient(ingredient=ingredient, grams=grams))
                    db.session.add(meal)
                    db.session.commit()
                    return redirect(url_for('index'))
                except Exception as e:
                    db.session.rollback()
                    error = f'Error saving meal: {e}'

        ingredients = Ingredient.query.order_by(Ingredient.name).all()
        return render_template('create_meal.html', ingredients=ingredients, error=error)

    @app.route('/meal/<int:meal_id>/edit', methods=['GET', 'POST'])
    def edit_meal(meal_id):
        from flask import request, redirect, url_for
        from models import MealIngredient
        meal = Meal.query.get(meal_id)
        if not meal:
            abort(404)
        error = None
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            image_url = request.form.get('image_url', '').strip() or '/static/placeholder.svg'
            time_minutes = request.form.get('time_minutes', '').strip()
            recipe = request.form.get('recipe', '').strip()
            ingredient_ids = request.form.getlist('ingredients')

            if not name or not time_minutes or not recipe:
                error = 'Please fill in all required fields.'
            else:
                try:
                    meal.name = name
                    meal.image_url = image_url
                    meal.time_minutes = int(time_minutes)
                    meal.recipe = recipe
                    meal.meal_ingredients.clear()
                    if ingredient_ids:
                        for ing_id in ingredient_ids:
                            grams_val = request.form.get(f'grams_{ing_id}', '0').strip()
                            grams = float(grams_val) if grams_val else 0
                            if grams > 0:
                                ingredient = Ingredient.query.get(int(ing_id))
                                meal.meal_ingredients.append(MealIngredient(ingredient=ingredient, grams=grams))
                    db.session.commit()
                    return redirect(url_for('meal_detail', meal_id=meal.id))
                except Exception as e:
                    db.session.rollback()
                    error = f'Error saving meal: {e}'

        ingredients = Ingredient.query.order_by(Ingredient.name).all()
        return render_template('edit_meal.html', meal=meal, ingredients=ingredients, selected_ingredients={str(mi.ingredient_id): mi.grams for mi in meal.meal_ingredients}, error=error)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
