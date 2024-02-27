import csv
import sqlite3

def search_and_write_to_csv(keyword):
    # Connect to the SQLite database
    conn = sqlite3.connect('news_data.db')
    cursor = conn.cursor()

    # SQL query to select data based on keyword
    query = """
        SELECT title, author_name, url, image_url, category_name, sub_category_name, inner_title, details, published_date, update_date 
        FROM news 
        WHERE inner_title LIKE ? OR details LIKE ?
    """

    # Execute the query with the keyword as parameter
    cursor.execute(query, ('%' + keyword + '%', '%' + keyword + '%'))
    rows = cursor.fetchall()

    # Write the data to a CSV file
    csv_filename = f"search_results_{keyword}.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'author_name', 'url', 'image_url', 'category_name', 'sub_category_name', 'inner_title', 'details', 'published_date', 'update_date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in rows:
            writer.writerow({
                'title': row[0],
                'author_name': row[1],
                'url': row[2],
                'image_url': row[3],
                'category_name': row[4],
                'sub_category_name': row[5],
                'inner_title': row[6],
                'details': row[7],
                'published_date': row[8],
                'update_date': row[9]
            })

    print(f"Search results have been written to '{csv_filename}'.")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    keyword = input("Enter keyword to search: ")
    search_and_write_to_csv(keyword)
