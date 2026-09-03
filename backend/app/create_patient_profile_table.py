from database import get_database_connection


def create_patient_profiles_table():
    connection = get_database_connection()
    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS patient_profiles (
        id SERIAL PRIMARY KEY,

        user_id INTEGER UNIQUE NOT NULL,

        date_of_birth DATE,
        gender VARCHAR(20),
        phone VARCHAR(20),
        blood_group VARCHAR(10),

        height_cm NUMERIC(5, 2),
        weight_kg NUMERIC(5, 2),

        emergency_contact_name VARCHAR(100),
        emergency_contact_phone VARCHAR(20),

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        CONSTRAINT fk_patient_user
            FOREIGN KEY (user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
    );
    """

    cursor.execute(create_table_query)

    connection.commit()

    cursor.close()
    connection.close()

    print("Patient profiles table created successfully!")


create_patient_profiles_table()
