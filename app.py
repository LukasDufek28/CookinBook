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
        return render_template('meal.html', meal=meal)


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
                    meal = Meal(
                        name=name,
                        image_url=image_url,
                        time_minutes=int(time_minutes),
                        recipe=recipe,
                    )
                    if ingredient_ids:
                        ingredients = Ingredient.query.filter(Ingredient.id.in_(ingredient_ids)).all()
                        meal.ingredients = ingredients
                    db.session.add(meal)
                    db.session.commit()
                    return redirect(url_for('index'))
                except Exception as e:
                    db.session.rollback()
                    error = f'Error saving meal: {e}'

        ingredients = Ingredient.query.order_by(Ingredient.name).all()
        return render_template('create_meal.html', ingredients=ingredients, error=error)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
