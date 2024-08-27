import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import create_app  # Import your Flask app factory function
from app.models.fund import Fund

logging.basicConfig(level=logging.INFO)

app = create_app()

mysql_url = os.environ.get('MYSQL_DATABASE_URL') or 'mysql://aham:password@db/fund_mgt_development'
print(mysql_url)
mysql_engine = create_engine(mysql_url)
mysql_session = sessionmaker(bind=mysql_engine)

def migrate_funds():
    with app.app_context():
        try:
            with mysql_session() as session:
                cached_funds = Fund.query.all()

                funds = [Fund(
                    uuid=f.uuid,
                    name=f.name,
                    fund_house=f.fund_house,
                    nav=f.nav,
                    performance_percentage=f.performance_percentage,
                    description=f.description,
                    created_at=f.created_at,
                    updated_at=f.updated_at,
                    deleted_at=f.deleted_at
                ) for f in cached_funds]

                session.bulk_save_objects(funds)
                session.commit()
                
                logging.info("Funds migrated successfully")
    
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            try:
                session.rollback()
            except Exception as rollback_exception:
                logging.error(f"Rollback failed: {rollback_exception}")

if __name__ == '__main__':
    migrate_funds()
