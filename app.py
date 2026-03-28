"""
app.py
======
Entry point for the Advanced Inventory System.

Integrates the servicios.py and archivos.py modules to provide
an interactive console menu with the following options:

    1. Add product
    2. Show inventory
    3. Search product
    4. Update product
    5. Delete product
    6. Statistics
    7. Save CSV
    8. Load CSV
    9. Exit

Features:
    - Input validations for each option.
    - Error handling: no error closes the application.
    - Active while loop until the user chooses "Exit".
"""

# ── Own module imports ────────────────────────────────────────────────────────
import services  # CRUD operations and statistics
import files   # CSV persistence (save / load)


# ─────────────────────────────────────────────────────────────────────────────
# INPUT UTILITIES
# ─────────────────────────────────────────────────────────────────────────────

def ask_float(message: str, allow_empty: bool = False) -> float | None:
    """
    Prompts the user for a decimal number ≥ 0. Repeats until a valid value is obtained.

    Parameters:
        message (str):      Text displayed to the user.
        allow_empty (bool): If True, returns None when the user presses Enter.

    Returns:
        float: Value entered, or None if allow_empty=True and the user entered nothing.
    """
    while True:
        entry = input(message).strip()
        if allow_empty and entry == "":
            return None
        try:
            value = float(entry)
            if value < 0:
                print("   ⚠️  The value cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print("   ⚠️  Please enter a valid number (e.g. 12.50).")


def ask_int(message: str, allow_empty: bool = False) -> int | None:
    """
    Prompts the user for an integer ≥ 0. Repeats until a valid value is obtained.

    Parameters:
        message (str):      Text displayed to the user.
        allow_empty (bool): If True, returns None when the user presses Enter.

    Returns:
        int: Value entered, or None if allow_empty=True and the user entered nothing.
    """
    while True:
        entry = input(message).strip()
        if allow_empty and entry == "":
            return None
        try:
            value = int(entry)
            if value < 0:
                print("   ⚠️  The value cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print("   ⚠️  Please enter a valid integer (e.g. 10).")


def ask_name(message: str) -> str:
    """
    Prompts the user for a non-empty name.

    Parameters:
        message (str): Text displayed to the user.

    Returns:
        str: Name entered (without leading/trailing spaces).
    """
    while True:
        name = input(message).strip()
        if name:
            return name
        print("   ⚠️  The name cannot be empty.")


def confirm(question: str) -> bool:
    """
    Prompts the user for Y/N confirmation.

    Parameters:
        question (str): Question text.

    Returns:
        bool: True if the user enters 'Y' or 'y', False if 'N' or 'n'.
    """
    while True:
        resp = input(question).strip().upper()
        if resp in ("Y", "N"):
            return resp == "Y"
        print("   ⚠️  Please answer Y (yes) or N (no).")


# ─────────────────────────────────────────────────────────────────────────────
# MENU HANDLERS
# ─────────────────────────────────────────────────────────────────────────────

def handle_add(inventory: list) -> None:
    """Handles the 'Add product' menu option."""
    print("\n── Add product ───────────────────────────")
    name     = ask_name ("  Name     : ")
    price    = ask_float("  Price    : $")
    quantity = ask_int  ("  Quantity : ")

    if servicios.add_product(inventory, name, price, quantity):
        print(f"\n✅ Product '{name}' added successfully.")
    else:
        print(f"\n⚠️  Product '{name}' already exists in the inventory.")
        print("     Use option 4 (Update) to modify it.")


def handle_show(inventory: list) -> None:
    """Handles the 'Show inventory' menu option."""
    print("\n── Current inventory ─────────────────────")
    servicios.show_inventory(inventory)


def handle_search(inventory: list) -> None:
    """Handles the 'Search product' menu option."""
    print("\n── Search product ────────────────────────")
    name    = ask_name("  Name to search: ")
    product = servicios.search_product(inventory, name)

    if product:
        print(f"\n✅ Product found:")
        print(f"   Name     : {product['name']}")
        print(f"   Price    : ${product['price']:.2f}")
        print(f"   Quantity : {product['quantity']}")
    else:
        print(f"\n⚠️  Product '{name}' not found in the inventory.")


def handle_update(inventory: list) -> None:
    """Handles the 'Update product' menu option."""
    print("\n── Update product ────────────────────────")
    name = ask_name("  Name to update: ")

    # Check that the product exists before asking for new values
    if servicios.search_product(inventory, name) is None:
        print(f"\n⚠️  Product '{name}' not found.")
        return

    print("  (Press Enter to leave the value unchanged)")
    new_price    = ask_float("  New price    : $", allow_empty=True)
    new_quantity = ask_int  ("  New quantity : ",  allow_empty=True)

    # Check that at least one field was provided
    if new_price is None and new_quantity is None:
        print("\n⚠️  No value was entered. Operation cancelled.")
        return

    servicios.update_product(inventory, name, new_price, new_quantity)
    print(f"\n✅ Product '{name}' updated successfully.")


def handle_delete(inventory: list) -> None:
    """Handles the 'Delete product' menu option."""
    print("\n── Delete product ────────────────────────")
    name = ask_name("  Name to delete: ")

    # Check existence
    if servicios.search_product(inventory, name) is None:
        print(f"\n⚠️  Product '{name}' not found.")
        return

    # Request confirmation before deleting
    if confirm(f"  Confirm deletion of '{name}'? (Y/N): "):
        servicios.delete_product(inventory, name)
        print(f"\n✅ Product '{name}' removed from inventory.")
    else:
        print("\n  Operation cancelled.")


def handle_statistics(inventory: list) -> None:
    """Handles the 'Statistics' menu option."""
    servicios.show_statistics(inventory)


def handle_save(inventory: list) -> None:
    """Handles the 'Save CSV' menu option."""
    print("\n── Save inventory to CSV ─────────────────")
    print("  (Path example: inventory.csv  or  data/inventory.csv)")
    path = input("  File path: ").strip()

    if not path:
        print("\n⚠️  The path cannot be empty. Operation cancelled.")
        return

    # Add .csv extension if missing
    if not path.lower().endswith(".csv"):
        path += ".csv"

    archivos.save_csv(inventory, path)


def handle_load(inventory: list) -> None:
    """
    Handles the 'Load CSV' menu option.

    Merge policy (when the user chooses NOT to overwrite):
        - New name    → added to the inventory.
        - Existing name → quantity is summed and price is updated.
    """
    print("\n── Load inventory from CSV ───────────────")
    print("  (Path example: inventory.csv  or  data/inventory.csv)")
    path = input("  File path: ").strip()

    if not path:
        print("\n⚠️  The path cannot be empty. Operation cancelled.")
        return

    # Attempt to load the CSV
    new_items = archivos.load_csv(path)
    if new_items is None:
        # load_csv already printed the corresponding error message
        return

    if not new_items:
        print("\n⚠️  The file contains no valid products. Inventory unchanged.")
        return

    # Decide between overwriting or merging
    print(f"\n  Found {len(new_items)} valid product(s) in '{path}'.")
    print("  Merge policy (option N): quantity summed, price updated to new value.\n")

    overwrite = confirm("  Overwrite current inventory? (Y/N): ")

    if overwrite:
        # Replace the entire inventory
        inventory.clear()
        inventory.extend(new_items)
        print(
            f"\n✅ Load summary:"
            f"\n   Action            : Full replacement"
            f"\n   Products loaded   : {len(new_items)}"
        )
    else:
        # Merge following the defined policy
        result = archivos.merge_inventories(inventory, new_items)
        print(
            f"\n✅ Load summary:"
            f"\n   Action            : Merge"
            f"\n   New products      : {result['added']}"
            f"\n   Updated products  : {result['updated']}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# MAIN MENU
# ─────────────────────────────────────────────────────────────────────────────

def show_menu() -> None:
    """Prints the main menu to the console."""
    print("\n" + "╔" + "═" * 40 + "╗")
    print("║      🗃️  INVENTORY SYSTEM  🗃️            ║")
    print("╠" + "═" * 40 + "╣")
    print("║  1. Add product                        ║")
    print("║  2. Show inventory                     ║")
    print("║  3. Search product                     ║")
    print("║  4. Update product                     ║")
    print("║  5. Delete product                     ║")
    print("║  6. Statistics                         ║")
    print("║  7. Save CSV                           ║")
    print("║  8. Load CSV                           ║")
    print("║  9. Exit                               ║")
    print("╚" + "═" * 40 + "╝")


def main() -> None:
    """
    Main function. Initializes the inventory and runs the menu
    loop until the user chooses option 9 (Exit).
    """
    # In-memory inventory: list of dictionaries
    inventory: list = []

    # Option → handler map
    actions = {
        "1": handle_add,
        "2": handle_show,
        "3": handle_search,
        "4": handle_update,
        "5": handle_delete,
        "6": handle_statistics,
        "7": handle_save,
        "8": handle_load,
    }

    print("\nWelcome to the Advanced Inventory System!")

    # Main loop: stays active until "9 - Exit"
    option = ""
    while option != "10":
        show_menu()

        try:
            option = input("\n  Select an option (1–9): ").strip()
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C or end of input → clean exit
            print("\n\n  Program interrupted. Goodbye!")
            option = "10"  # Force exit

        # Option 9: exit
        if option == "9":
            print("\n  Goodbye! The program has finished.\n")
            break

        # Valid option (1–8)
        if option in actions:
            try:
                actions[option](inventory)
            except Exception as e:
                # Generic catch to prevent any unexpected error
                # from closing the application
                print(f"\n❌ Unexpected error: {e}")
                print("   The application will continue running.")
        else:
            # Invalid option
            print("\n⚠️  Invalid option. Please enter a number between 1 and 9.")

        # Pause before returning to the menu
        input("\n  Press Enter to continue...")

# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
