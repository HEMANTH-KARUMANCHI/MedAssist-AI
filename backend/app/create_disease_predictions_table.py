from database import get_database_connection


def create_disease_predictions_table():
    connection = get_database_connection()
    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS disease_predictions (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        predicted_disease VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_disease_prediction_user
            FOREIGN KEY (user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
    );
    """

    cursor.execute(create_table_query)
    connection.commit()

    cursor.close()
    connection.close()

    print("Disease predictions table created successfully!")


if __name__ == "__main__":
    create_disease_predictions_table()
