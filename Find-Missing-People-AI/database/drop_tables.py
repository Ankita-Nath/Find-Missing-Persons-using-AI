from postgres_conn import PostgresConnection

tables = ["user_submissions", "submitted_cases", "users"]


def main():
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        for table in tables:
            query = f"DROP TABLE IF EXISTS {table}"
            cursor.execute(query)
        print("All tables removed")


if __name__ == "__main__":
    response = input("Do you want to Drop ALL Tables: (Y/N)")
    if response.lower() == "y":
        main()
    else:
        print("You didn't press Y, exiting")
