import requests
import sqlite3
from datetime import datetime, timedelta

# Function to fetch data from API
def fetch_data(start_date, end_date, access_token):
    url = f"https://128.199.143.136/api/en/getrangedata?start_date={start_date}&end_date={end_date}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers, verify=False)
    return response.json()

# Function to create SQLite connection and table
def create_database_and_table():
    conn = sqlite3.connect('news_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS news (
                 title TEXT,
                 author_name TEXT,
                 url TEXT,
                 image_url TEXT,
                 category_name TEXT,
                 sub_category_name TEXT,
                 inner_title TEXT,
                 details TEXT,
                 published_date TEXT,
                 update_date TEXT
                 )''')
    conn.commit()
    conn.close()

# Function to insert data into SQLite database
def insert_data_into_database(data):
    conn = sqlite3.connect('news_data.db')
    c = conn.cursor()
    c.execute("DELETE FROM news")  # Clear existing data
    for item in data:
        c.execute("INSERT INTO news VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (item['title'], item['author_name'], item['url'], item['image_url'],
                   item['category_name'], item['sub_category_name'], item['inner_title'],
                   item['details'], item['published_date'], item['update_date']))
    conn.commit()
    conn.close()

# Main function
def main():
    access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SnGryL2TBVwRHg1I14AlWryFzaDwlm5aqEIftv2-RVY"
    end_date = datetime.today().strftime('%d-%m-%Y')
    start_date = (datetime.today() - timedelta(days=7)).strftime('%d-%m-%Y')
    
    data = fetch_data(start_date, end_date, access_token)
    create_database_and_table()
    insert_data_into_database(data)

if __name__ == "__main__":
    main()
