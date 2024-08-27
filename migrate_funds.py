# migrate_funds.py

import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from app import create_app, db

def migrate_funds(sqlite_db_path, mysql_db_url):
    app = create_app(env='migration')

    with app.app_context():
        db.create_all()

    # SQLite DB engine
    sqlite_engine = create_engine(f'sqlite:///{sqlite_db_path}')
    sqlite_metadata = MetaData()

    # Check existing tables in SQLite
    try:
        sqlite_metadata.reflect(bind=sqlite_engine)
    except SQLAlchemyError as e:
        print(f"Metadata error: {e}")
        return

    if 'funds' not in sqlite_metadata.tables:
        print("Table funds does not exist")
        return

    # MySQL DB engine
    mysql_engine = create_engine(mysql_db_url)
    mysql_session = sessionmaker(bind=mysql_engine)()
    mysql_metadata = MetaData()
    mysql_metadata.reflect(bind=mysql_engine)

    # Define funds table in MySQL
    fund_table = Table(
        'funds', mysql_metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('uuid', String(36)),
        Column('name', String(255), nullable=False),
        Column('fund_house', String(255), nullable=False),
        Column('nav', Float, nullable=False),
        Column('performance_percentage', Float, nullable=False),
        Column('description', String),
        Column('created_at', DateTime),
        Column('updated_at', DateTime),
        Column('deleted_at', DateTime),
        extend_existing=True
    )

    # Fetch data from SQLite
    try:
        with sqlite_engine.connect() as sqlite_conn:
            sqlite_fund_table = Table('funds', sqlite_metadata, autoload_with=sqlite_engine)
            rows = sqlite_conn.execute(sqlite_fund_table.select()).fetchall()
            
            print(f"Total exising funds: {len(rows)}")
    except SQLAlchemyError as e:
        print(f"Fetching error: {e}")
        return

    column_names = [column.name for column in sqlite_fund_table.columns]

    # Start data migration
    with mysql_engine.connect() as mysql_conn:
        try:
            for row in rows:
                row_dict = {column_name: row[index] for index, column_name in enumerate(column_names)}
                row_dict = {key: value for key, value in row_dict.items() if key in fund_table.c.keys()}

                for key in ['created_at', 'updated_at', 'deleted_at']:
                    if key in row_dict and isinstance(row_dict[key], datetime):
                        row_dict[key] = row_dict[key].isoformat()

                # Map values and construct insert statement
                # Construct the SQL statement
                columns = ', '.join(row_dict.keys())
                values = ', '.join(f":{key}" for key in row_dict.keys())
                updates = ', '.join(f"{key}=VALUES({key})" for key in row_dict.keys() if key != 'id')

                insert_query = f"""
                    INSERT INTO funds ({columns})
                    VALUES ({values})
                    ON DUPLICATE KEY UPDATE {updates}
                """

                # Insert!
                mysql_session.execute(text(insert_query), row_dict)
            
            # Commit changes
            mysql_session.commit()
            print("Data migrated!")
        except SQLAlchemyError as e:
            print(f"Migration failed: {e}")
            mysql_session.rollback()
        finally:
            mysql_session.close()

if __name__ == "__main__":
    sqlite_db_path = 'instance/fund_mgt_development.db'
    mysql_db_url = os.environ.get('MYSQL_DATABASE_URL')
    
    migrate_funds(sqlite_db_path, mysql_db_url)
