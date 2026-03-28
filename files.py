"""
files.py
========
Persistence module for the inventory system.
Provides functions to save and load the inventory in CSV format.

Expected / generated CSV format:
    name,price,quantity
    Laptop,1200.00,5
    Mouse,25.50,30
"""

import csv
import os

# Canonical CSV header
HEADER = ["name", "price", "quantity"]


# ─────────────────────────────────────────────
# SAVE CSV
# ─────────────────────────────────────────────

def save_csv(inventory: list, path: str, include_header: bool = True) -> bool:
    """
    Writes the inventory to a CSV file with comma separator.

    The resulting file has the format:
        name,price,quantity
        Laptop,1200.00,5
        ...

    Parameters:
        inventory (list):       List of inventory dictionaries.
        path (str):             Full (or relative) path of the destination file.
        include_header (bool):  If True, writes the header line. Default True.

    Returns:
        bool: True if saved successfully, False if an error occurred.
    """
    # Validate that the inventory is not empty
    if not inventory:
        print("\n⚠️  The inventory is empty. There is no data to save.")
        return False

    try:
        # Create intermediate directories if they don't exist
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=HEADER)

            # Write header if required
            if include_header:
                writer.writeheader()

            # Write each product as a row
            for product in inventory:
                writer.writerow({
                    "name":     product["name"],
                    "price":    f"{product['price']:.2f}",
                    "quantity": product["quantity"]
                })

        print(f"\n✅ Inventory saved to: {os.path.abspath(path)}")
        return True

    except PermissionError:
        print(f"\n⚠️  Permission error: cannot write to '{path}'.")
        print("     Check that the path is correct and you have write permissions.")
    except OSError as e:
        print(f"\n⚠️  System error while saving: {e}")
    except Exception as e:
        print(f"\n⚠️  Unexpected error while saving the CSV: {e}")

    return False


# ─────────────────────────────────────────────
# LOAD CSV
# ─────────────────────────────────────────────

def load_csv(path: str) -> list | None:
    """
    Reads a CSV file and returns a list of valid products.

    Row validation rules:
        - Must have exactly 3 columns (name, price, quantity).
        - price must convert to float and be ≥ 0.
        - quantity must convert to int and be ≥ 0.
        - Invalid rows are skipped (an error counter is accumulated).

    The file must have the header: name,price,quantity

    Parameters:
        path (str): Path to the CSV file to load.

    Returns:
        list: List of dicts {"name", "price", "quantity"} of valid rows,
              or None if an unrecoverable error occurred (file not found,
              invalid format, encoding error).
    """
    products      = []   # Valid products
    invalid_rows  = 0

    try:
        with open(path, mode="r", newline="", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)

            # ── Validate header ─────────────────────────────────────────────
            try:
                header = next(reader)
            except StopIteration:
                print(f"\n⚠️  The file '{path}' is empty.")
                return None

            # Normalize header (strip spaces and lowercase)
            header_norm = [col.strip().lower() for col in header]
            if header_norm != HEADER:
                print(
                    f"\n⚠️  Invalid format. Expected header:\n"
                    f"      name,price,quantity\n"
                    f"    Found:\n"
                    f"      {','.join(header)}"
                )
                return None

            # ── Process rows ────────────────────────────────────────────────
            for row_num, row in enumerate(reader, start=2):  # start=2 (row 1 = header)

                # Check for exactly 3 columns
                if len(row) != 3:
                    print(f"   ↳ Row {row_num} skipped (incorrect columns): {row}")
                    invalid_rows += 1
                    continue

                name_raw, price_raw, quantity_raw = row

                # Validate name
                name = name_raw.strip()
                if not name:
                    print(f"   ↳ Row {row_num} skipped (empty name).")
                    invalid_rows += 1
                    continue

                # Validate and convert price
                try:
                    price = float(price_raw.strip())
                    if price < 0:
                        raise ValueError("negative price")
                except ValueError:
                    print(f"   ↳ Row {row_num} skipped (invalid price: '{price_raw}').")
                    invalid_rows += 1
                    continue

                # Validate and convert quantity
                try:
                    quantity = int(quantity_raw.strip())
                    if quantity < 0:
                        raise ValueError("negative quantity")
                except ValueError:
                    print(f"   ↳ Row {row_num} skipped (invalid quantity: '{quantity_raw}').")
                    invalid_rows += 1
                    continue

                # Valid row → add product
                products.append({
                    "name":     name,
                    "price":    round(price, 2),
                    "quantity": quantity
                })

    except FileNotFoundError:
        print(f"\n⚠️  File not found: '{path}'")
        print("     Check that the path and file name are correct.")
        return None

    except UnicodeDecodeError:
        print(f"\n⚠️  Encoding error while reading '{path}'.")
        print("     Make sure the file is saved in UTF-8.")
        return None

    except PermissionError:
        print(f"\n⚠️  Permission error: cannot read '{path}'.")
        return None

    except Exception as e:
        print(f"\n⚠️  Unexpected error while loading the CSV: {e}")
        return None

    # Reading summary
    if invalid_rows > 0:
        print(f"\n   ℹ️  {invalid_rows} invalid row(s) skipped during load.")

    return products


# ─────────────────────────────────────────────
# INVENTORY MERGE
# ─────────────────────────────────────────────

def merge_inventories(current_inventory: list, new_products: list) -> dict:
    """
    Merges new products into the existing inventory following the policy:
        - If the name does NOT exist → add the product.
        - If the name ALREADY exists → add the new quantity to the existing one
          and update the price to the new value.

    Parameters:
        current_inventory (list): In-memory inventory (modified in place).
        new_products (list):      List of dicts loaded from the CSV.

    Returns:
        dict: Operation summary with keys:
              "added" (int):   New products incorporated.
              "updated" (int): Existing products modified.
    """
    added   = 0
    updated = 0

    # Build a quick-lookup map (name_lower → index)
    lookup = {p["name"].lower(): i for i, p in enumerate(current_inventory)}

    for new in new_products:
        key = new["name"].lower()

        if key in lookup:
            # Existing product: update price and add quantity
            idx = lookup[key]
            current_inventory[idx]["price"]    = new["price"]
            current_inventory[idx]["quantity"] += new["quantity"]
            updated += 1
        else:
            # New product: add it
            current_inventory.append(new)
            lookup[new["name"].lower()] = len(current_inventory) - 1
            added += 1

    return {"added": added, "updated": updated}
