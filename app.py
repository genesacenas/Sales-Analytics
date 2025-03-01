from flask import Flask, render_template,jsonify, request
import sqlite3

import matplotlib 
matplotlib.use('Agg') # Use a non-GUI backend
import pandas as pd
import matplotlib.pyplot as plt 

import os

app = Flask(__name__)
DATABASE = "sales_data.db"

# Ensure the 'static' folder exists

if not os.path.exists("static"):
    os.makedirs("static")

def get_sales_data():
    """Fetch sales data from database."""
    conn=sqlite3.connect(DATABASE)
    
    df = pd.read_sql_query('SELECT * FROM sales', conn)
    
    conn.close()
    return df

def save_graph(df, graph_name):
    """Generate a graph and save it an image"""
    plt.figure(figsize=(8, 5))
    df.plot(kind='bar', x='product', y ='sales', color = 'skyblue')
    plt.title('Sales by Product')
    plt.xlabel('Product')
    plt.ylabel('Sales')
    graph_path = os.path.join("static", graph_name)
    plt.savefig(graph_path)
    plt.close()
    return graph_path

@app.route("/")
def index():
    """Render the home page"""
    sales_data = get_sales_data()
    sales_summary = sales_data.groupby("product") ["sales"].sum().reset_index()
    graph_path = save_graph(sales_summary,"sales_graph.png")
    return render_template("index.html", graph_path=graph_path)

@app.route("/analyze", methods =["POST"])
def analyze():
    """Analyze data to provide suggestions"""
    sales_data = get_sales_data()
    top_product = sales_data.groupby("product") ["sales"].sum().idxmax()
    suggestion = f"Focus on increasing marketing efforts for {top_product}, as it performsn the best."
    
    return jsonify({"suggestion": suggestion})

if __name__ == "__main__":
    app.run(debug=True)
