🗃️ Advanced Inventory System
A modular command-line inventory management application written in Python. It supports full CRUD operations, statistics, and CSV-based persistence.

📁 Project Structure
├── app.py        # Entry point — main menu and user interaction
├── services.py   # Business logic — CRUD operations and statistics
├── files.py      # Persistence — CSV save/load and inventory merge
└── README.md

🧭 Menu Options
OptionDescription1Add a new product2Display the full inventory3Search a product by name4Update price and/or quantity5Delete a product6Show inventory statistics7Save inventory to a CSV file8Load inventory from a CSV file9Exit

📦 Module Reference
services.py
FunctionDescriptionadd_product(inventory, name, price, quantity)Adds a product if it doesn't already exist. Returns True on success.show_inventory(inventory)Prints the inventory as a formatted table.search_product(inventory, name)Case-insensitive search. Returns the product dict or None.update_product(inventory, name, new_price, new_quantity)Updates one or both fields. Pass None to leave a field unchanged.delete_product(inventory, name)Removes a product by name. Returns True on success.calculate_statistics(inventory)Returns a dict with total units, total value, most expensive product, and highest stock.show_statistics(inventory)Prints formatted statistics to the console.
Product dictionary structure:
python{
    "name":     str,    # Product name (unique key)
    "price":    float,  # Unit price (≥ 0)
    "quantity": int     # Units in stock (≥ 0)
}

files.py
FunctionDescriptionsave_csv(inventory, path, include_header=True)Writes the inventory to a CSV file. Creates directories if needed. Returns True on success.load_csv(path)Reads a CSV file. Returns a list of valid products, or None on error. Invalid rows are skipped with a warning.merge_inventories(current_inventory, new_products)Merges loaded products into the existing inventory. Returns a summary dict {"added": int, "updated": int}.
CSV format:
name,price,quantity
Laptop,1200.00,5
Mouse,25.50,30
Merge policy (when not overwriting):

Name not found → product is added.
Name already exists → quantity is summed, price is updated to the new value.


⚠️ Error Handling

All menu options are wrapped in try/except — no error will crash the application.
load_csv validates each row individually and skips invalid ones.
All I/O functions handle FileNotFoundError, PermissionError, UnicodeDecodeError, and general OSError.


💡 Usage Example
Welcome to the Advanced Inventory System!

╔════════════════════════════════════════╗
║      🗃️  INVENTORY SYSTEM  🗃️         ║
╠════════════════════════════════════════╣
║  1. Add product                        ║
║  ...                                   ║
╚════════════════════════════════════════╝

  Select an option (1–9): 1

── Add product ───────────────────────────
  Name     : Laptop
  Price    : $1200
  Quantity : 5

✅ Product added successfully.S3
<img width="2125" height="1625" alt="inventory_main_flow_1" src="https://github.com/user-attachments/assets/9f268ca6-677a-463a-8e90-37b32265e6a1" />
<img width="680" height="486" alt="option_01_add_product" src="https://github.com/user-attachments/assets/fb88ac43-34ea-42bb-a630-8e47ef2ef261" />
<img width="680" height="318" alt="option_02_show_inventory" src="https://github.com/user-attachments/assets/94fab815-bff8-494f-976c-8cd6612d41d0" />
<img width="680" height="318" alt="option_03_search_product" src="https://github.com/user-attachments/assets/9990ce25-0992-4399-9d88-062f3a0f0fd6" />
<img width="680" height="566" alt="option_04_update_product" src="https://github.com/user-attachments/assets/b8e2e421-218c-482c-a728-5d76761436fa" />
<img width="680" height="566" alt="option_05_delete_product" src="https://github.com/user-attachments/assets/1a05351a-42da-44b2-9b50-7bee8080db06" />
<img width="680" height="318" alt="option_06_statistics" src="https://github.com/user-attachments/assets/99d3d841-6b60-4694-9a28-f38b05f00074" />
<img width="680" height="486" alt="option_07_save_csv" src="https://github.com/user-attachments/assets/f18aff18-f7fa-44e7-a11a-820a03ead227" />
<img width="680" height="574" alt="option_08_load_csv" src="https://github.com/user-attachments/assets/1626ad32-2501-4e83-8ed0-927564bb465b" />
<img width="680" height="150" alt="option_09_exit" src="https://github.com/user-attachments/assets/fb493584-bd51-4374-b379-e60b354c237a" />

