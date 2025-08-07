from fastapi import HTTPException
from backend.db import get_db_connection
from datetime import datetime


def post_product(product_data: dict):
    """Post a new classified ad."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO products (name, description, category, price, location, contact, image_url, posted_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        product_data["name"],
        product_data["description"],
        product_data["category"],
        product_data["price"],
        product_data["location"],
        product_data["contact"],
        product_data.get("image_url"),
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()

    return {"message": "Product posted successfully"}


def search_products(query: str):
    """Search products by name or description."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM products
        WHERE name LIKE ? OR description LIKE ?
    """, (f"%{query}%", f"%{query}%"))

    results = cursor.fetchall()
    conn.close()

    return [dict(row) for row in results]


def get_products_by_category(category: str):
    """Retrieve products by category."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM products
        WHERE category = ?
    """, (category,))

    results = cursor.fetchall()
    conn.close()

    return [dict(row) for row in results]


def get_products_by_location(location: str):
    """Retrieve products by location."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM products
        WHERE location = ?
    """, (location,))

    results = cursor.fetchall()
    conn.close()

    return [dict(row) for row in results]


def get_recent_products(limit: int = 10):
    """Retrieve the most recent product listings."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM products
        ORDER BY posted_at DESC
        LIMIT ?
    """, (limit,))

    results = cursor.fetchall()
    conn.close()

    return [dict(row) for row in results]


def report_product(product_id: int, reason: str):
    """Flag a product for review."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reports (product_id, reason, reported_at)
        VALUES (?, ?, ?)
    """, (product_id, reason, datetime.now().isoformat()))

    conn.commit()
    conn.close()

    return {"message": "Product reported for review"}
