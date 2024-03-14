import csv
import sqlite3
from tkinter import Tk, filedialog

def search_and_write_to_csv(keywords):
    # Connect to the SQLite database
    conn = sqlite3.connect('news_data.db')
    cursor = conn.cursor()

    # Write the data to a CSV file
    csv_filename = "search_results.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'author_name', 'url', 'image_url', 'category_name', 'sub_category_name', 'inner_title', 'details', 'published_date', 'update_date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for keyword in keywords:
            # SQL query to select data based on keyword
            query = """
                SELECT title, author_name, url, image_url, category_name, sub_category_name, inner_title, details, published_date, update_date 
                FROM news 
                WHERE inner_title LIKE ? OR details LIKE ?
            """

            # Execute the query with the keyword as parameter
            cursor.execute(query, ('%' + keyword + '%', '%' + keyword + '%'))
            rows = cursor.fetchall()

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
    # Create a Tkinter root window
    root = Tk()
    root.withdraw()  # Hide the root window

    # Prompt the user to select a file
    filename = filedialog.askopenfilename(title="Select Keywords File", filetypes=[("Text files", "*.txt")])

    # Read keywords from the selected text file
    with open(filename, "r") as file:
        keywords_str = file.read()

    # Split the keywords by commas
    keywords = [keyword.strip().strip('"') for keyword in keywords_str.split(',')]

    search_and_write_to_csv(keywords)
