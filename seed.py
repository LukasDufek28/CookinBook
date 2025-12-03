import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from app import create_app
from models import db, Meal, Ingredient


def seed_data(app):
    with app.app_context():
        # Drop and recreate all tables
        db.drop_all()
        db.create_all()

        # Add 200+ unique ingredients
        base_ingredients = [
    'Paradajka', 'Syr', 'Cestoviny', 'Bazalka', 'Vajce', 'Olej', 'Múka', 'Soľ', 'Čierne korenie', 'Kuracie mäso', 'Hovädzie mäso', 'Bravčové mäso',
    'Cibuľa', 'Cesnak', 'Mrkva', 'Zemiak', 'Mlieko', 'Maslo', 'Olivový olej', 'Ryža', 'Fazuľa', 'Šalát',
    'Uhorka', 'Špenát', 'Brokolica', 'Karfiol', 'Hrášok', 'Kukurica', 'Šampiňón', 'Paprika', 'Chilli', 'Jablko',
    'Banán', 'Pomaranč', 'Citrón', 'Limetka', 'Jahoda', 'Čučoriedka', 'Malina', 'Hrozno', 'Ananás', 'Melón',
    'Dyňa', 'Avokádo', 'Tekvica', 'Cuketa', 'Baklažán', 'Kapusta', 'Zeler', 'Reďkovka', 'Petržlen', 'Sladký zemiak',
    'Batát', 'Quinoa', 'Jačmeň', 'Ovsené vločky', 'Mandľa', 'Vlašský orech', 'Lieskový orech', 'Kešu', 'Arašid', 'Slnečnicové semienko',
    'Sezam', 'Chia semienko', 'Kokos', 'Jogurt', 'Smotana', 'Feta', 'Mozzarella', 'Parmezán', 'Čedar', 'Šunka',
    'Klobása', 'Slanina', 'Morka', 'Kačica', 'Jahňacina', 'Ryba', 'Losos', 'Tuniak', 'Kreveta', 'Krab',
    'Homár', 'Mušľa', 'Ustrica', 'Kalamár', 'Chobotnica', 'Sardinka', 'Ančovička', 'Makrela', 'Pstruh', 'Bazalka',
    'Oregano', 'Rozmarín', 'Tymian', 'Šalvia', 'Kôpor', 'Mäta', 'Koriander', 'Petržlen vňať', 'Pažítka', 'Škorica',
    'Muškátový oriešok', 'Klinček', 'Kardamóm', 'Zázvor', 'Kurkuma', 'Rasca', 'Paprika', 'Kari korenie', 'Horčica', 'Ocot',
    'Sójová omáčka', 'Worcesterská omáčka', 'Pikantná omáčka', 'Kečup', 'Majonéza', 'Med', 'Javorový sirup', 'Džem', 'Želé', 'Cukor',
    'Hnedý cukor', 'Melasa', 'Sirup', 'Čokoláda', 'Kakao', 'Vanilka', 'Káva', 'Čaj', 'Soda', 'Pivo',
    'Víno', 'Whisky', 'Rum', 'Vodka', 'Gin', 'Tequila', 'Brandy', 'Šampanské', 'Portské', 'Tofu',
    'Tempeh', 'Seitan', 'Miso', 'Nori', 'Kimchi', 'Kyslá kapusta', 'Uhorka nakladaná', 'Relish', 'Kapary', 'Artičoka',
    'Špargľa', 'Pór', 'Šalotka', 'Cibuľka', 'Okra', 'Repa', 'Kel', 'Rukola', 'Endívia', 'Fenikel',
    'Pak choi', 'Daikon', 'Jicama', 'Lotusový koreň', 'Bambusový výhonok', 'Gaštan', 'Pekanový orech', 'Makadamový orech', 'Pistácia', 'Raž',
    'Špalda', 'Farro', 'Proso', 'Cirok', 'Teff', 'Amarant', 'Pohánka', 'Polenta', 'Krupica', 'Paneer',
    'Ricotta', 'Mascarpone', 'Gorgonzola', 'Modrý syr', 'Kozí syr', 'Ovčí syr', 'Tvaroh', 'Crème fraîche', 'Kyslá smotana', 'Zmrzlina',
    'Gelato', 'Sorbet', 'Šerbet', 'Puding', 'Sneh', 'Marshmallow', 'Nugat', 'Halva', 'Granola', 'Musli',
    'Trail mix', 'Energetická tyčinka', 'Proteínový prášok', 'Srvátka', 'Kazeín', 'Vaječný bielok', 'Vaječný žĺtok', 'Kačacie vajce', 'Prepeličie vajce', 'Husacie vajce',
    'Králik', 'Jelenie mäso', 'Diviak', 'Bažant', 'Hus', 'Perlička', 'Aligátor', 'Fentanyl'
]
        # Pad to 200+ if needed
        all_ingredients = base_ingredients.copy()
        for i in range(len(base_ingredients), 210):
            all_ingredients.append(f"Ingredient {i+1}")

        # Nutrition values per 100g for some common ingredients
        nutrition_map = {
            'Vajce':     {'calories': 155, 'protein': 13, 'fat': 11, 'carbs': 1.1},
            'Ryža':      {'calories': 130, 'protein': 2.7, 'fat': 0.3, 'carbs': 28},
            'Cibuľa':    {'calories': 40,  'protein': 1.1, 'fat': 0.1, 'carbs': 9.3},
            'Olej':      {'calories': 884, 'protein': 0,   'fat': 100, 'carbs': 0},
            'Sójová omáčka': {'calories': 53, 'protein': 8, 'fat': 0.6, 'carbs': 4.9},
            'Aligátor':  {'calories': 143, 'protein': 22, 'fat': 6, 'carbs': 0},
            'Fentanyl':  {'calories': 0, 'protein': 0, 'fat': 0, 'carbs': 0},
            # Add more as needed
        }

        ingredient_objs = []
        for name in all_ingredients:
            nut = nutrition_map.get(name, {'calories': 100, 'protein': 2, 'fat': 2, 'carbs': 10})
            ingredient_objs.append(Ingredient(
                name=name,
                calories=nut['calories'],
                protein=nut['protein'],
                fat=nut['fat'],
                carbs=nut['carbs']
            ))
        db.session.add_all(ingredient_objs)
        db.session.commit()

        # Meals (use some of the new ingredients)
        import random


        meal1 = Meal(
            name='Eggs Fried Rice',
            image_url='https://www.seriouseats.com/thmb/BJjCEDw9OZe95hpZxmNcD3rJnHo=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/20230529-SEA-EggFriedRice-AmandaSuarez-hero-c8d95fbf69314b318bc279159f582882.jpg',
            recipe='Na miernom ohni rozohrejeme olej, pridáme vajíčka a miešame, kým nie sú skoro uvarené. Pridáme uvarenú ryžu, sójovú omáčku a nakrájanú cibuľku. Miešame, kým sa všetko dobre nespojí a ryža je horúca.',
            time_minutes=20,
        )

        db.session.add(meal1)  # Add meal to session before associating ingredients
        from models import MealIngredient
        # Example grams for each ingredient
        meal1.meal_ingredients.extend([
            MealIngredient(ingredient=next(i for i in ingredient_objs if i.name == 'Vajce'), grams=200),
            MealIngredient(ingredient=next(i for i in ingredient_objs if i.name == 'Ryža'), grams=300),
            MealIngredient(ingredient=next(i for i in ingredient_objs if i.name == 'Cibuľa'), grams=30),
            MealIngredient(ingredient=next(i for i in ingredient_objs if i.name == 'Olej'), grams=30),
            MealIngredient(ingredient=next(i for i in ingredient_objs if i.name == 'Sójová omáčka'), grams=30),
        ])
        db.session.commit()

        print(f'Seeded database with {len(ingredient_objs)} ingredients and 1 meals.')

if __name__ == '__main__':
    app = create_app()
    seed_data(app)
