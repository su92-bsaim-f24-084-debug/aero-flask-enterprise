import os
from app import create_app
from app.models import db
from seed import seed_database

app = create_app(os.environ.get('FLASK_CONFIG', 'default'))

@app.cli.command('init-db')
def init_db_command():
    """CLI helper to initialize all tables across 51 models."""
    db.create_all()
    print("Database schema successfully generated across all 51 models!")

@app.cli.command('seed-db')
def seed_db_command():
    """CLI helper to populate database with operational sample data."""
    seed_database()
    print("Database successfully seeded!")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
