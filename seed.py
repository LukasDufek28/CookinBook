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

        # Nutrition values per 100g for some common ingredients
        nutrition_map = {
    # --- Vami definované hodnoty ---
    'Vajce':          {'calories': 155, 'protein': 13, 'fat': 11, 'carbs': 1.1},
    'Ryža':           {'calories': 130, 'protein': 2.7, 'fat': 0.3, 'carbs': 28}, # Varená (podľa vášho zadania)
    'Cibuľa':         {'calories': 40,  'protein': 1.1, 'fat': 0.1, 'carbs': 9.3},
    'Olej':           {'calories': 884, 'protein': 0,   'fat': 100, 'carbs': 0},
    'Sójová omáčka':  {'calories': 53,  'protein': 8,   'fat': 0.6, 'carbs': 4.9},
    'Aligátor':       {'calories': 143, 'protein': 22,  'fat': 6,   'carbs': 0},
    'Fentanyl':       {'calories': 0,   'protein': 0,   'fat': 0,   'carbs': 0},

    # --- Základné potraviny ---
    'Paradajka':      {'calories': 18,  'protein': 0.9, 'fat': 0.2, 'carbs': 3.9},
    'Syr':            {'calories': 402, 'protein': 25,  'fat': 33,  'carbs': 1.3}, # Typ Eidam/Gouda
    'Cestoviny':      {'calories': 371, 'protein': 13,  'fat': 1.5, 'carbs': 75},  # Surové (dry)
    'Bazalka':        {'calories': 23,  'protein': 3.2, 'fat': 0.6, 'carbs': 2.7},
    'Múka':           {'calories': 364, 'protein': 10,  'fat': 1,   'carbs': 76},
    'Soľ':            {'calories': 0,   'protein': 0,   'fat': 0,   'carbs': 0},
    'Čierne korenie': {'calories': 251, 'protein': 10,  'fat': 3.3, 'carbs': 64},  # Koreniny majú vysoké hodnoty na 100g, ale používajú sa v mg
    'Kuracie mäso':   {'calories': 165, 'protein': 31,  'fat': 3.6, 'carbs': 0},
    'Hovädzie mäso':  {'calories': 250, 'protein': 26,  'fat': 15,  'carbs': 0},
    'Bravčové mäso':  {'calories': 242, 'protein': 27,  'fat': 14,  'carbs': 0},
    'Cesnak':         {'calories': 149, 'protein': 6.4, 'fat': 0.5, 'carbs': 33},
    'Mrkva':          {'calories': 41,  'protein': 0.9, 'fat': 0.2, 'carbs': 9.6},
    'Zemiak':         {'calories': 77,  'protein': 2,   'fat': 0.1, 'carbs': 17},
    'Mlieko':         {'calories': 61,  'protein': 3.2, 'fat': 3.3, 'carbs': 4.8}, # Polotučné/Plnotučné priemer
    'Maslo':          {'calories': 717, 'protein': 0.9, 'fat': 81,  'carbs': 0.1},
    'Olivový olej':   {'calories': 884, 'protein': 0,   'fat': 100, 'carbs': 0},
    'Fazuľa':         {'calories': 347, 'protein': 21,  'fat': 1.2, 'carbs': 63},  # Surová (dry)
    'Šalát':          {'calories': 15,  'protein': 1.4, 'fat': 0.2, 'carbs': 2.9},

    # --- Zelenina ---
    'Uhorka':         {'calories': 15,  'protein': 0.7, 'fat': 0.1, 'carbs': 3.6},
    'Špenát':         {'calories': 23,  'protein': 2.9, 'fat': 0.4, 'carbs': 3.6},
    'Brokolica':      {'calories': 34,  'protein': 2.8, 'fat': 0.4, 'carbs': 6.6},
    'Karfiol':        {'calories': 25,  'protein': 1.9, 'fat': 0.3, 'carbs': 5},
    'Hrášok':         {'calories': 81,  'protein': 5,   'fat': 0.4, 'carbs': 14},
    'Kukurica':       {'calories': 86,  'protein': 3.2, 'fat': 1.2, 'carbs': 19},
    'Šampiňón':       {'calories': 22,  'protein': 3.1, 'fat': 0.3, 'carbs': 3.3},
    'Paprika':        {'calories': 26,  'protein': 1,   'fat': 0.3, 'carbs': 6},   # Červená/Mix
    'Chilli':         {'calories': 40,  'protein': 1.9, 'fat': 0.4, 'carbs': 8.8},
    'Dyňa':           {'calories': 26,  'protein': 1,   'fat': 0.1, 'carbs': 6.5}, # Vodný melón
    'Avokádo':        {'calories': 160, 'protein': 2,   'fat': 15,  'carbs': 9},
    'Tekvica':        {'calories': 26,  'protein': 1,   'fat': 0.1, 'carbs': 6.5},
    'Cuketa':         {'calories': 17,  'protein': 1.2, 'fat': 0.3, 'carbs': 3.1},
    'Baklažán':       {'calories': 25,  'protein': 1,   'fat': 0.2, 'carbs': 6},
    'Kapusta':        {'calories': 25,  'protein': 1.3, 'fat': 0.1, 'carbs': 5.8},
    'Zeler':          {'calories': 16,  'protein': 0.7, 'fat': 0.2, 'carbs': 3},
    'Reďkovka':       {'calories': 16,  'protein': 0.7, 'fat': 0.1, 'carbs': 3.4},
    'Petržlen':       {'calories': 36,  'protein': 3,   'fat': 0.8, 'carbs': 6.3}, # Koreň
    'Sladký zemiak':  {'calories': 86,  'protein': 1.6, 'fat': 0.1, 'carbs': 20},
    'Batát':          {'calories': 86,  'protein': 1.6, 'fat': 0.1, 'carbs': 20},
    'Špargľa':        {'calories': 20,  'protein': 2.2, 'fat': 0.1, 'carbs': 3.9},
    'Pór':            {'calories': 61,  'protein': 1.5, 'fat': 0.3, 'carbs': 14},
    'Šalotka':        {'calories': 72,  'protein': 2.5, 'fat': 0.1, 'carbs': 17},
    'Cibuľka':        {'calories': 32,  'protein': 1.8, 'fat': 0.2, 'carbs': 7.3}, # Jarná
    'Okra':           {'calories': 33,  'protein': 1.9, 'fat': 0.2, 'carbs': 7.5},
    'Repa':           {'calories': 43,  'protein': 1.6, 'fat': 0.2, 'carbs': 10},
    'Kel':            {'calories': 49,  'protein': 4.3, 'fat': 0.9, 'carbs': 9},
    'Rukola':         {'calories': 25,  'protein': 2.6, 'fat': 0.7, 'carbs': 3.7},
    'Endívia':        {'calories': 17,  'protein': 1.3, 'fat': 0.2, 'carbs': 3.4},
    'Fenikel':        {'calories': 31,  'protein': 1.2, 'fat': 0.2, 'carbs': 7},
    'Pak choi':       {'calories': 13,  'protein': 1.5, 'fat': 0.2, 'carbs': 2.2},
    'Daikon':         {'calories': 18,  'protein': 0.6, 'fat': 0.1, 'carbs': 4.1},
    'Jicama':         {'calories': 38,  'protein': 0.7, 'fat': 0.1, 'carbs': 9},
    'Lotusový koreň': {'calories': 74,  'protein': 2.6, 'fat': 0.1, 'carbs': 17},
    'Bambusový výhonok': {'calories': 27, 'protein': 2.6, 'fat': 0.3, 'carbs': 5},
    'Artičoka':       {'calories': 47,  'protein': 3.3, 'fat': 0.2, 'carbs': 11},

    # --- Ovocie ---
    'Jablko':         {'calories': 52,  'protein': 0.3, 'fat': 0.2, 'carbs': 14},
    'Banán':          {'calories': 89,  'protein': 1.1, 'fat': 0.3, 'carbs': 23},
    'Pomaranč':       {'calories': 47,  'protein': 0.9, 'fat': 0.1, 'carbs': 12},
    'Citrón':         {'calories': 29,  'protein': 1.1, 'fat': 0.3, 'carbs': 9},
    'Limetka':        {'calories': 30,  'protein': 0.7, 'fat': 0.2, 'carbs': 11},
    'Jahoda':         {'calories': 32,  'protein': 0.7, 'fat': 0.3, 'carbs': 7.7},
    'Čučoriedka':     {'calories': 57,  'protein': 0.7, 'fat': 0.3, 'carbs': 14},
    'Malina':         {'calories': 52,  'protein': 1.2, 'fat': 0.7, 'carbs': 12},
    'Hrozno':         {'calories': 69,  'protein': 0.7, 'fat': 0.2, 'carbs': 18},
    'Ananás':         {'calories': 50,  'protein': 0.5, 'fat': 0.1, 'carbs': 13},
    'Melón':          {'calories': 34,  'protein': 0.8, 'fat': 0.2, 'carbs': 8}, # Žltý melón (Cantaloupe)

    # --- Orechy, Semená, Obilniny (Surové/Dry) ---
    'Quinoa':         {'calories': 368, 'protein': 14,  'fat': 6,   'carbs': 64},
    'Jačmeň':         {'calories': 354, 'protein': 12,  'fat': 2.3, 'carbs': 73},
    'Ovsené vločky':  {'calories': 389, 'protein': 17,  'fat': 7,   'carbs': 66},
    'Mandľa':         {'calories': 579, 'protein': 21,  'fat': 50,  'carbs': 22},
    'Vlašský orech':  {'calories': 654, 'protein': 15,  'fat': 65,  'carbs': 14},
    'Lieskový orech': {'calories': 628, 'protein': 15,  'fat': 61,  'carbs': 17},
    'Kešu':           {'calories': 553, 'protein': 18,  'fat': 44,  'carbs': 30},
    'Arašid':         {'calories': 567, 'protein': 26,  'fat': 49,  'carbs': 16},
    'Slnečnicové semienko': {'calories': 584, 'protein': 20, 'fat': 51, 'carbs': 20},
    'Sezam':          {'calories': 573, 'protein': 18,  'fat': 50,  'carbs': 23},
    'Chia semienko':  {'calories': 486, 'protein': 17,  'fat': 31,  'carbs': 42},
    'Kokos':          {'calories': 354, 'protein': 3.3, 'fat': 33,  'carbs': 15}, # Dužina
    'Gaštan':         {'calories': 196, 'protein': 1.6, 'fat': 1.3, 'carbs': 44}, # Pečený
    'Pekanový orech': {'calories': 691, 'protein': 9,   'fat': 72,  'carbs': 14},
    'Makadamový orech': {'calories': 718, 'protein': 8, 'fat': 76,  'carbs': 14},
    'Pistácia':       {'calories': 560, 'protein': 20,  'fat': 45,  'carbs': 28},
    'Raž':            {'calories': 338, 'protein': 10,  'fat': 1.6, 'carbs': 76},
    'Špalda':         {'calories': 338, 'protein': 15,  'fat': 2.4, 'carbs': 70},
    'Farro':          {'calories': 337, 'protein': 14,  'fat': 2,   'carbs': 72},
    'Proso':          {'calories': 378, 'protein': 11,  'fat': 4.2, 'carbs': 73},
    'Cirok':          {'calories': 339, 'protein': 11,  'fat': 3.3, 'carbs': 75},
    'Teff':           {'calories': 367, 'protein': 13,  'fat': 2.4, 'carbs': 73},
    'Amarant':        {'calories': 371, 'protein': 14,  'fat': 7,   'carbs': 65},
    'Pohánka':        {'calories': 343, 'protein': 13,  'fat': 3.4, 'carbs': 71},
    'Polenta':        {'calories': 85,  'protein': 2,   'fat': 0.3, 'carbs': 18}, # Varená
    'Krupica':        {'calories': 360, 'protein': 13,  'fat': 1,   'carbs': 73},

    # --- Mliečne výrobky a náhrady ---
    'Jogurt':         {'calories': 59,  'protein': 10,  'fat': 0.4, 'carbs': 3.6}, # Grécky typ / biely
    'Smotana':        {'calories': 195, 'protein': 2.7, 'fat': 19,  'carbs': 3.7}, # Na varenie 12-20%
    'Feta':           {'calories': 264, 'protein': 14,  'fat': 21,  'carbs': 4},
    'Mozzarella':     {'calories': 280, 'protein': 28,  'fat': 17,  'carbs': 3.1},
    'Parmezán':       {'calories': 431, 'protein': 38,  'fat': 29,  'carbs': 4.1},
    'Čedar':          {'calories': 402, 'protein': 25,  'fat': 33,  'carbs': 1.3},
    'Paneer':         {'calories': 265, 'protein': 18,  'fat': 20,  'carbs': 1.2},
    'Ricotta':        {'calories': 174, 'protein': 11,  'fat': 13,  'carbs': 3},
    'Mascarpone':     {'calories': 455, 'protein': 4,   'fat': 47,  'carbs': 2}, # Veľmi tučné
    'Gorgonzola':     {'calories': 350, 'protein': 21,  'fat': 29,  'carbs': 2},
    'Modrý syr':      {'calories': 353, 'protein': 21,  'fat': 29,  'carbs': 2},
    'Kozí syr':       {'calories': 364, 'protein': 22,  'fat': 30,  'carbs': 0.1}, # Tvrdý
    'Ovčí syr':       {'calories': 283, 'protein': 18,  'fat': 23,  'carbs': 0.5}, # Hrudka
    'Tvaroh':         {'calories': 85,  'protein': 12,  'fat': 2.5, 'carbs': 3.5}, # Jemný
    'Crème fraîche':  {'calories': 393, 'protein': 2,   'fat': 42,  'carbs': 2},
    'Kyslá smotana':  {'calories': 193, 'protein': 2,   'fat': 19,  'carbs': 4},
    'Tofu':           {'calories': 76,  'protein': 8,   'fat': 4.8, 'carbs': 1.9},
    'Tempeh':         {'calories': 192, 'protein': 19,  'fat': 11,  'carbs': 9},
    'Seitan':         {'calories': 370, 'protein': 75,  'fat': 2,   'carbs': 14}, # Pšeničný lepok (prášok/suchý)

    # --- Mäso a údeniny ---
    'Šunka':          {'calories': 145, 'protein': 21,  'fat': 6,   'carbs': 1.5},
    'Klobása':        {'calories': 300, 'protein': 12,  'fat': 27,  'carbs': 2}, # Priemer
    'Slanina':        {'calories': 541, 'protein': 37,  'fat': 42,  'carbs': 1.4},
    'Morka':          {'calories': 189, 'protein': 29,  'fat': 7,   'carbs': 0},
    'Kačica':         {'calories': 337, 'protein': 19,  'fat': 28,  'carbs': 0},
    'Jahňacina':      {'calories': 294, 'protein': 25,  'fat': 21,  'carbs': 0},
    'Králik':         {'calories': 173, 'protein': 33,  'fat': 3.5, 'carbs': 0},
    'Jelenie mäso':   {'calories': 158, 'protein': 30,  'fat': 3.2, 'carbs': 0},
    'Diviak':         {'calories': 122, 'protein': 21,  'fat': 3.3, 'carbs': 0},
    'Bažant':         {'calories': 133, 'protein': 23,  'fat': 3.6, 'carbs': 0},
    'Hus':            {'calories': 371, 'protein': 16,  'fat': 33,  'carbs': 0},
    'Perlička':       {'calories': 158, 'protein': 23,  'fat': 6.5, 'carbs': 0},
    
    # --- Ryby a plody mora ---
    'Ryba':           {'calories': 100, 'protein': 20,  'fat': 2,   'carbs': 0},   # Biela ryba všeobecne
    'Losos':          {'calories': 208, 'protein': 20,  'fat': 13,  'carbs': 0},
    'Tuniak':         {'calories': 132, 'protein': 28,  'fat': 1,   'carbs': 0},   # Steak
    'Kreveta':        {'calories': 99,  'protein': 24,  'fat': 0.3, 'carbs': 0.2},
    'Krab':           {'calories': 97,  'protein': 19,  'fat': 1.5, 'carbs': 0},
    'Homár':          {'calories': 89,  'protein': 19,  'fat': 0.9, 'carbs': 0},
    'Mušľa':          {'calories': 172, 'protein': 24,  'fat': 4.5, 'carbs': 7},
    'Ustrica':        {'calories': 68,  'protein': 7,   'fat': 2.5, 'carbs': 4},
    'Kalamár':        {'calories': 92,  'protein': 15,  'fat': 1.4, 'carbs': 3},
    'Chobotnica':     {'calories': 82,  'protein': 15,  'fat': 1,   'carbs': 2.2},
    'Sardinka':       {'calories': 208, 'protein': 25,  'fat': 11,  'carbs': 0},
    'Ančovička':      {'calories': 210, 'protein': 29,  'fat': 10,  'carbs': 0},
    'Makrela':        {'calories': 305, 'protein': 19,  'fat': 25,  'carbs': 0},
    'Pstruh':         {'calories': 148, 'protein': 20,  'fat': 6.6, 'carbs': 0},

    # --- Bylinky a prísady ---
    # Poznámka: Bylinky majú na 100g kalórie, ale používajú sa v malom.
    'Oregano':        {'calories': 265, 'protein': 9,   'fat': 4,   'carbs': 69},  # Sušené
    'Rozmarín':       {'calories': 131, 'protein': 3.3, 'fat': 5.9, 'carbs': 20},  # Čerstvé
    'Tymian':         {'calories': 101, 'protein': 5.6, 'fat': 1.7, 'carbs': 24},
    'Šalvia':         {'calories': 315, 'protein': 10,  'fat': 12,  'carbs': 60},  # Sušená
    'Kôpor':          {'calories': 43,  'protein': 3.5, 'fat': 1.1, 'carbs': 7},
    'Mäta':           {'calories': 70,  'protein': 3.8, 'fat': 0.9, 'carbs': 15},
    'Koriander':      {'calories': 23,  'protein': 2.1, 'fat': 0.5, 'carbs': 3.7},
    'Petržlen vňať':  {'calories': 36,  'protein': 3,   'fat': 0.8, 'carbs': 6.3},
    'Pažítka':        {'calories': 30,  'protein': 3.3, 'fat': 0.7, 'carbs': 4.4},
    'Škorica':        {'calories': 247, 'protein': 4,   'fat': 1.2, 'carbs': 81},
    'Muškátový oriešok': {'calories': 525, 'protein': 6, 'fat': 36, 'carbs': 49},
    'Klinček':        {'calories': 274, 'protein': 6,   'fat': 13,  'carbs': 65},
    'Kardamóm':       {'calories': 311, 'protein': 11,  'fat': 6.7, 'carbs': 68},
    'Zázvor':         {'calories': 80,  'protein': 1.8, 'fat': 0.8, 'carbs': 18},
    'Kurkuma':        {'calories': 354, 'protein': 8,   'fat': 10,  'carbs': 65},  # Prášok
    'Rasca':          {'calories': 333, 'protein': 20,  'fat': 15,  'carbs': 44},
    'Kari korenie':   {'calories': 325, 'protein': 13,  'fat': 14,  'carbs': 58},
    'Horčica':        {'calories': 66,  'protein': 4,   'fat': 3.4, 'carbs': 6},   # Plnotučná
    'Ocot':           {'calories': 18,  'protein': 0,   'fat': 0,   'carbs': 0.1},
    'Worcesterská omáčka': {'calories': 78, 'protein': 0, 'fat': 0, 'carbs': 19},
    'Pikantná omáčka': {'calories': 11, 'protein': 0.5, 'fat': 0.4, 'carbs': 2},
    'Kečup':          {'calories': 101, 'protein': 1,   'fat': 0.1, 'carbs': 27},
    'Majonéza':       {'calories': 680, 'protein': 1,   'fat': 75,  'carbs': 0.6},
    'Med':            {'calories': 304, 'protein': 0.3, 'fat': 0,   'carbs': 82},
    'Javorový sirup': {'calories': 260, 'protein': 0,   'fat': 0.1, 'carbs': 67},
    'Džem':           {'calories': 250, 'protein': 0.5, 'fat': 0,   'carbs': 60},
    'Želé':           {'calories': 260, 'protein': 0,   'fat': 0,   'carbs': 65},
    'Cukor':          {'calories': 387, 'protein': 0,   'fat': 0,   'carbs': 100},
    'Hnedý cukor':    {'calories': 380, 'protein': 0.1, 'fat': 0,   'carbs': 98},
    'Melasa':         {'calories': 290, 'protein': 0,   'fat': 0.1, 'carbs': 75},
    'Sirup':          {'calories': 260, 'protein': 0,   'fat': 0,   'carbs': 70},   # Všeobecný
    'Čokoláda':       {'calories': 546, 'protein': 4.9, 'fat': 31,  'carbs': 61},   # Tmavá
    'Kakao':          {'calories': 228, 'protein': 20,  'fat': 14,  'carbs': 58},   # Prášok
    'Vanilka':        {'calories': 288, 'protein': 0.1, 'fat': 0.1, 'carbs': 12},   # Extrakt
    'Miso':           {'calories': 199, 'protein': 12,  'fat': 6,   'carbs': 26},
    'Nori':           {'calories': 35,  'protein': 5.8, 'fat': 0.3, 'carbs': 5},
    'Kimchi':         {'calories': 15,  'protein': 1.1, 'fat': 0.5, 'carbs': 2.4},
    'Kyslá kapusta':  {'calories': 19,  'protein': 0.9, 'fat': 0.1, 'carbs': 4.3},
    'Uhorka nakladaná': {'calories': 11, 'protein': 0.3, 'fat': 0.1, 'carbs': 2.3},
    'Relish':         {'calories': 130, 'protein': 0.6, 'fat': 0.5, 'carbs': 35},
    'Kapary':         {'calories': 23,  'protein': 2.4, 'fat': 0.9, 'carbs': 5},

    # --- Nápoje a Alkohol ---
    # Kalórie z alkoholu sú cca 7 kcal/g, ale často sa neuvádzajú v makrách. Tu sú v 'calories'.
    'Káva':           {'calories': 0,   'protein': 0.1, 'fat': 0,   'carbs': 0},
    'Čaj':            {'calories': 1,   'protein': 0,   'fat': 0,   'carbs': 0.2},
    'Soda':           {'calories': 40,  'protein': 0,   'fat': 0,   'carbs': 10},   # Sladená
    'Pivo':           {'calories': 43,  'protein': 0.5, 'fat': 0,   'carbs': 3.6},
    'Víno':           {'calories': 83,  'protein': 0.1, 'fat': 0,   'carbs': 2.6},  # Červené
    'Whisky':         {'calories': 250, 'protein': 0,   'fat': 0,   'carbs': 0.1},
    'Rum':            {'calories': 231, 'protein': 0,   'fat': 0,   'carbs': 0},
    'Vodka':          {'calories': 231, 'protein': 0,   'fat': 0,   'carbs': 0},
    'Gin':            {'calories': 263, 'protein': 0,   'fat': 0,   'carbs': 0},
    'Tequila':        {'calories': 231, 'protein': 0,   'fat': 0,   'carbs': 0},
    'Brandy':         {'calories': 225, 'protein': 0,   'fat': 0,   'carbs': 0},
    'Šampanské':      {'calories': 84,  'protein': 0.1, 'fat': 0,   'carbs': 2.8},
    'Portské':        {'calories': 154, 'protein': 0.2, 'fat': 0,   'carbs': 12},

    # --- Dezerty a doplnky ---
    'Zmrzlina':       {'calories': 207, 'protein': 3.5, 'fat': 11,  'carbs': 24},
    'Gelato':         {'calories': 220, 'protein': 4,   'fat': 8,   'carbs': 30},
    'Sorbet':         {'calories': 140, 'protein': 0,   'fat': 0,   'carbs': 34},
    'Šerbet':         {'calories': 144, 'protein': 1.1, 'fat': 2,   'carbs': 30},
    'Puding':         {'calories': 120, 'protein': 3,   'fat': 4,   'carbs': 18},
    'Sneh':           {'calories': 52,  'protein': 11,  'fat': 0.2, 'carbs': 0.7},  # Bielkový
    'Marshmallow':    {'calories': 318, 'protein': 1.8, 'fat': 0.2, 'carbs': 81},
    'Nugat':          {'calories': 400, 'protein': 3,   'fat': 10,  'carbs': 80},
    'Halva':          {'calories': 470, 'protein': 12,  'fat': 22,  'carbs': 60},
    'Granola':        {'calories': 471, 'protein': 10,  'fat': 20,  'carbs': 64},
    'Musli':          {'calories': 340, 'protein': 11,  'fat': 5,   'carbs': 66},
    'Trail mix':      {'calories': 462, 'protein': 14,  'fat': 30,  'carbs': 45},
    'Energetická tyčinka': {'calories': 400, 'protein': 20, 'fat': 10, 'carbs': 50},
    'Proteínový prášok': {'calories': 370, 'protein': 80, 'fat': 3, 'carbs': 6},   # Whey 80%
    'Srvátka':        {'calories': 27,  'protein': 0.9, 'fat': 0.4, 'carbs': 5},    # Tekutá
    'Kazeín':         {'calories': 360, 'protein': 75,  'fat': 1.5, 'carbs': 10},
    'Vaječný bielok': {'calories': 52,  'protein': 11,  'fat': 0.2, 'carbs': 0.7},
    'Vaječný žĺtok':  {'calories': 322, 'protein': 16,  'fat': 27,  'carbs': 3.6},
    'Kačacie vajce':  {'calories': 185, 'protein': 13,  'fat': 14,  'carbs': 1.5},
    'Prepeličie vajce': {'calories': 158, 'protein': 13, 'fat': 11, 'carbs': 0.4},
    'Husacie vajce':  {'calories': 185, 'protein': 14,  'fat': 13,  'carbs': 1.4},
}

        base_ingredients = list(nutrition_map.keys())
        ingredient_objs = []
        for name in base_ingredients:
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

        # Meal 1
        meal1 = Meal(
            name='Eggs Fried Rice',
            image_url='https://www.seriouseats.com/thmb/BJjCEDw9OZe95hpZxmNcD3rJnHo=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/20230529-SEA-EggFriedRice-AmandaSuarez-hero-c8d95fbf69314b318bc279159f582882.jpg',
            recipe='Na miernom ohni rozohrejeme olej, pridáme vajíčka a miešame, kým nie sú skoro uvarené. Pridáme uvarenú ryžu, sójovú omáčku a nakrájanú cibuľku. Miešame, kým sa všetko dobre nespojí a ryža je horúca.',
            time_minutes=20,
        )
        db.session.add(meal1)
        from models import MealIngredient
        meal1.meal_ingredients.extend([
            MealIngredient(ingredient=next(i for i in ingredient_objs if i.name == 'Vajce'), grams=200),
            MealIngredient(ingredient=next(i for i in ingredient_objs if i.name == 'Ryža'), grams=300),
            MealIngredient(ingredient=next(i for i in ingredient_objs if i.name == 'Cibuľa'), grams=30),
            MealIngredient(ingredient=next(i for i in ingredient_objs if i.name == 'Olej'), grams=30),
            MealIngredient(ingredient=next(i for i in ingredient_objs if i.name == 'Sójová omáčka'), grams=30),
        ])

        # Meal 2 - Aligator
        meal2 = Meal(
            name='Aligátor',
            image_url='https://www.ifauna.cz/upload/plemena/photos/images/202505/1107-aligator-cinsky_17480650891710.jpg?ver=1748065089',
            recipe='Zjedz ho, lebo on zje teba. Na oslavu máš 200 ml šampanského.',
            time_minutes=15,
        )
        db.session.add(meal2)
        meal2.meal_ingredients.extend([
            MealIngredient(ingredient=next(i for i in ingredient_objs if i.name == 'Aligátor'), grams=367000),
        ])

        db.session.commit()

        print(f'Seeded database with {len(ingredient_objs)} ingredients and 2 meals.')

if __name__ == '__main__':
    app = create_app()
    seed_data(app)
