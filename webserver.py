from flask import Flask, render_template_string, redirect, url_for
import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Veritabanı bağlantısı
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        client_encoding="utf8"
    )
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT entity_id, forename, name, date_of_birth, age, sex, nationalities, detail_link, created_at, last_updated_at
        FROM notices
        ORDER BY entity_id;
    """)
    notices = cur.fetchall()
    cur.close()
    conn.close()

    display_notices = []
    for notice in notices:
        status = ""
        if notice[8] == notice[9]:  # created_at == last_updated_at
            status = "NEW"
        else:
            status = "UPDATED"

        display_notices.append({
            "entity_id": notice[0],
            "forename": notice[1],
            "name": notice[2],
            "date_of_birth": notice[3],
            "age": notice[4],
            "sex": notice[5],
            "nationalities": notice[6],
            "detail_link": notice[7],
            "status": status
        })

    return render_template_string('''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Interpol Red Notices</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <meta http-equiv="refresh" content="600">
      </head>
      <body class="bg-light">
        <div class="container mt-4">
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h1 class="text-center flex-grow-1">Interpol Red Notices</h1>
            <a href="{{ url_for('index') }}" class="btn btn-primary">Refresh</a>
          </div>
          <table class="table table-striped table-bordered">
            <thead class="table-dark">
              <tr>
                <th>Entity ID</th>
                <th>Forename</th>
                <th>Name</th>
                <th>Date of Birth</th>
                <th>Age</th>
                <th>Sex</th>
                <th>Nationalities</th>
                <th>Detail Link</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
            {% for notice in notices %}
              <tr class="{% if notice.status == 'UPDATED' %}table-danger{% elif notice.status == 'NEW' %}table-success{% endif %}">
                <td>{{ notice.entity_id }}</td>
                <td>{{ notice.forename }}</td>
                <td>{{ notice.name }}</td>
                <td>{{ notice.date_of_birth }}</td>
                <td>{{ notice.age }}</td>
                <td>{{ notice.sex }}</td>
                <td>{{ notice.nationalities }}</td>
                <td><a href="{{ notice.detail_link }}" target="_blank">Link</a></td>
                <td>
                  {% if notice.status == 'NEW' %}
                    <span class="badge bg-success">NEW</span>
                  {% elif notice.status == 'UPDATED' %}
                    <span class="badge bg-danger">UPDATED</span>
                  {% endif %}
                </td>
              </tr>
            {% endfor %}
            </tbody>
          </table>
        </div>
      </body>
    </html>
    ''', notices=display_notices)


if __name__ == '__main__':
    app.run(debug=True)

