import requests
import json
import psycopg2
import numpy as np
from sklearn.linear_model import LogisticRegression

# Set up connection to ElephantSQL
conn = psycopg2.connect(
    host = 'rajje.db.elephantsql.com',
    database = 'syabkhtb',
    user = 'syabkhtb',
    port = '5432',
    password = 'J7LXI5pNQ_UoUP316yEd-yoXnCOZK8HE'
)
cursor = conn.cursor()

# Retrieve data from the table
query = "SELECT * FROM probablesstats"
cursor.execute(query)
data = cursor.fetchall()

# Prepare the data for training
X = []
y = []

for row in data:
    # Extract features and target variable from each row
    features = [row[1], row[2], ...]  # Replace indices with the appropriate column indices from the fetched data
    outcome = row[3]  # Replace index with the appropriate column index for the target variable

    X.append(features)
    y.append(outcome)

# Convert lists to NumPy arrays for training
X = np.array(X)
y = np.array(y)

# Train your model
model = LogisticRegression()
model.fit(X, y)

# Close the database connection
cursor.close()
conn.close()
