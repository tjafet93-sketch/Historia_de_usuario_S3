"""
services.py
===========
Business logic module for the inventory system.
Contains all CRUD operations and statistics calculations.

Structure of each product in the inventory:
    {"name": str, "price": float, "quantity": int}
"""


# ─────────────────────────────────────────────
# CRUD FUNCTIONS
# ─────────────────────────────────────────────

def add_product(inventory: list, name: str, price: float, quantity: int) -> bool:
    """
    Adds a new product to the inventory if it does not already exist.

    Parameters:
        inventory (list): List of dictionaries representing the inventory.
        name (str):       Product name (search key).
        price (float):    Unit price of the product (≥ 0).
        quantity (int):   Quantity in stock (≥ 0).

    Returns:
        bool: True if added successfully, False if the product already exists.
    """
    # Check for duplicate (case-insensitive search)
    if search_product(inventory, name) is not None:
        return False

    # Build the product dictionary and append it to the list
    product = {
        "name":     name.strip(),
        "price":    round(float(price), 2),
        "quantity": int(quantity)
    }
    inventory.append(product)
    return True


def show_inventory(inventory: list) -> None:
    """
    Prints the full inventory in table format with header and separators.

    Parameters:
        inventory (list): List of inventory dictionaries.

    Returns:
        None. Information is printed directly to the console.
    """
    if not inventory:
        print("\n⚠️  The inventory is empty.")
        return

    # Table header
    print("\n" + "═" * 52)
    print(f"  {'NAME':<22} {'PRICE':>10} {'QUANTITY':>10}")
    print("═" * 52)

    # Product rows
    for p in inventory:
        print(f"  {p['name']:<22} ${p['price']:>9.2f} {p['quantity']:>10}")

    print("═" * 52)
    print(f"  Total products: {len(inventory)}")
    print("═" * 52)


def search_product(inventory: list, name: str) -> dict | None:
    """
    Searches for a product by name (case-insensitive).

    Parameters:
        inventory (list): List of inventory dictionaries.
        name (str):       Name of the product to search for.

    Returns:
        dict: Product dictionary if found.
        None: If the product does not exist in the inventory.
    """
    name_lower = name.strip().lower()
    for product in inventory:
        if product["name"].lower() == name_lower:
            return product
    return None


def update_product(
    inventory: list,
    name: str,
    new_price: float | None = None,
    new_quantity: int | None = None
) -> bool:
    """
    Updates the price and/or quantity of an existing product.
    Only fields passed explicitly (not None) are updated.

    Parameters:
        inventory (list):         List of inventory dictionaries.
        name (str):               Name of the product to update.
        new_price (float|None):   New unit price; None = do not change.
        new_quantity (int|None):  New quantity in stock; None = do not change.

    Returns:
        bool: True if the product was found and updated, False if it does not exist.
    """
    product = search_product(inventory, name)
    if product is None:
        return False

    # Update only the provided fields
    if new_price is not None:
        product["price"] = round(float(new_price), 2)
    if new_quantity is not None:
        product["quantity"] = int(new_quantity)

    return True


def delete_product(inventory: list, name: str) -> bool:
    """
    Removes a product from the inventory by name.

    Parameters:
        inventory (list): List of inventory dictionaries.
        name (str):       Name of the product to delete.

    Returns:
        bool: True if the product was found and removed, False if it does not exist.
    """
    product = search_product(inventory, name)
    if product is None:
        return False

    inventory.remove(product)
    return True


# ─────────────────────────────────────────────
# STATISTICS
# ─────────────────────────────────────────────

def calculate_statistics(inventory: list) -> dict | None:
    """
    Calculates summary metrics for the inventory.

    Calculated metrics:
        - total_units:       Total sum of quantities in stock.
        - total_value:       Sum of (price × quantity) per product.
        - most_expensive:    Tuple (name, price) of the most costly product.
        - highest_stock:     Tuple (name, quantity) with the most units.

    Parameters:
        inventory (list): List of inventory dictionaries.

    Returns:
        dict: Dictionary with the described metrics.
        None: If the inventory is empty.
    """
    if not inventory:
        return None

    # Lambda to calculate the subtotal of a product
    subtotal = lambda p: p["price"] * p["quantity"]

    # Accumulated metrics
    total_units = sum(p["quantity"] for p in inventory)
    total_value = sum(subtotal(p) for p in inventory)

    # Product with the highest price
    most_expensive = max(inventory, key=lambda p: p["price"])
    # Product with the highest stock
    highest_stock = max(inventory, key=lambda p: p["quantity"])

    return {
        "total_units":    total_units,
        "total_value":    round(total_value, 2),
        "most_expensive": (most_expensive["name"], most_expensive["price"]),
        "highest_stock":  (highest_stock["name"], highest_stock["quantity"]),
    }


def show_statistics(inventory: list) -> None:
    """
    Prints the inventory statistics in a readable format.

    Parameters:
        inventory (list): List of inventory dictionaries.

    Returns:
        None. Information is printed directly to the console.
    """
    stats = calculate_statistics(inventory)

    if stats is None:
        print("\n⚠️  The inventory is empty. There are no statistics to show.")
        return

    name_expensive, price_expensive = stats["most_expensive"]
    name_stock, qty_stock           = stats["highest_stock"]

    print("\n" + "═" * 44)
    print("         📊  INVENTORY STATISTICS")
    print("═" * 44)
    print(f"  Total units in stock      : {stats['total_units']:>10}")
    print(f"  Total inventory value     : ${stats['total_value']:>10.2f}")
    print(f"  Most expensive product    : {name_expensive} (${price_expensive:.2f})")
    print(f"  Highest stock             : {name_stock} ({qty_stock} units)")
    print("═" * 44)
