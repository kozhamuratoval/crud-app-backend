from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = "postgresql://postgres:postgres@db:5432/tasks_db"

def test_database_connection():
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Test connection
        with engine.connect() as connection:
            # Test basic query
            result = connection.execute(text("SELECT version();"))
            version = result.scalar()
            print("Successfully connected to PostgreSQL!")
            print(f"PostgreSQL version: {version}")
            
            # Test creating a table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS test_table (
                    id SERIAL PRIMARY KEY,
                    test_column VARCHAR(50)
                );
            """))
            print("Successfully created test table!")
            
            # Test inserting data
            connection.execute(text("""
                INSERT INTO test_table (test_column) 
                VALUES ('test_data');
            """))
            print("Successfully inserted test data!")
            
            # Test reading data
            result = connection.execute(text("SELECT * FROM test_table;"))
            data = result.fetchall()
            print("Successfully read test data!")
            print(f"Test data: {data}")
            
            # Clean up
            connection.execute(text("DROP TABLE test_table;"))
            print("Successfully cleaned up test table!")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    test_database_connection() 