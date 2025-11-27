# CookinBook (Minimal Flask App)

This is a small Flask app that stores meals and ingredients in a SQL database. It shows a homepage with meal cards (image + name) and a detail page for each meal that lists ingredients, recipe text, and estimated time.

Quick features
- Meals table with name, image_url (placeholder used), recipe and time estimate (minutes).
- Ingredients table with many-to-many relationship to meals.
- Simple HTML templates with placeholder SVG image.

Getting started (Windows / PowerShell)

1. Create a virtual environment and activate it:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```


3. Database configuration:
- By default the app uses a local SQLite file `cookbook.db` for convenience.
- To use MySQL, set the `DATABASE_URL` environment variable before running the app, for example:

```powershell
$env:DATABASE_URL = "mysql+pymysql://USER:PASS@HOST:PORT/DATABASE"
```

- To use PostgreSQL, install the driver and set the `DATABASE_URL` like this:

```powershell
pip install psycopg2-binary
$env:DATABASE_URL = "postgresql+psycopg2://USER:PASS@HOST:PORT/DATABASE"
```

Replace USER/PASS/HOST/PORT/DATABASE with your database credentials.

4. Seed the database with sample data:

```powershell
python seed.py
```

5. Run the app:

```powershell
python app.py
```

Open http://127.0.0.1:5000/ in your browser.

Notes and next steps
- The image is a simple SVG placeholder in `static/placeholder.svg`.
- The models live in `models.py`. If you want to store additional metadata (quantities, units), extend the association to an explicit model.
- If you switch to MySQL, ensure the `pymysql` driver is installed and your `DATABASE_URL` uses the `mysql+pymysql://...` dialect.

If you want, I can:
- Add unit tests for the models and routes.
- Add an API (JSON) endpoint for meals.
- Add ability to upload real images and store them (filesystem or S3).
