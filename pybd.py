import mysql.connector
import tkinter as tk
from tkinter import messagebox
import datetime

# Global variables
current_user_id = None
current_faction_id = None

def db_connect():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234567890",  # Replace with your password
            database="games1"   # Replace with your database name
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

# Function for registering a new user
def register():
    reg_window = tk.Toplevel(login_window)
    reg_window.title("Register")
    reg_window.geometry("400x300")  # Set the window size to 400x300

    reg_username_label = tk.Label(reg_window, text="Username:")
    reg_username_label.pack(pady=5)
    reg_username_entry = tk.Entry(reg_window)
    reg_username_entry.pack(pady=5)

    reg_password_label = tk.Label(reg_window, text="Password:")
    reg_password_label.pack(pady=5)
    reg_password_entry = tk.Entry(reg_window, show="*")
    reg_password_entry.pack(pady=5)

    reg_age_label = tk.Label(reg_window, text="Age:")
    reg_age_label.pack(pady=5)
    reg_age_entry = tk.Entry(reg_window)
    reg_age_entry.pack(pady=5)
    
    reg_email_label = tk.Label(reg_window, text="Email:")
    reg_email_label.pack(pady=5)
    reg_email_entry = tk.Entry(reg_window)
    reg_email_entry.pack(pady=5)

    def register_user():
        username = reg_username_entry.get()
        password = reg_password_entry.get()
        age = reg_age_entry.get()
        email = reg_email_entry.get()

        db_connection = db_connect()
        if db_connection is None:
            return

        try:
            cursor = db_connection.cursor()
            sql_query = "INSERT INTO player (username, Password, gold, wood, stone, iron, Age, Email) VALUES (%s, %s, 500, 500, 500, 500, %s, %s)"
            cursor.execute(sql_query, (username, password, age, email))
            db_connection.commit()

            cursor.close()
            db_connection.close()

            messagebox.showinfo("Registration", "Registration successful")
            reg_window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    reg_button = tk.Button(reg_window, text="Register", command=register_user)
    reg_button.pack(pady=10)


# Function for user authentication
def authenticate():
    username = username_entry.get()
    password = password_entry.get()

    db_connection = db_connect()
    if db_connection is None:
        return

    try:
        cursor = db_connection.cursor()
        sql_query = "SELECT * FROM player WHERE username = %s AND password = %s"
        cursor.execute(sql_query, (username, password))
        result = cursor.fetchone()

        if result:
            global current_user_id
            current_user_id = result[0]
            messagebox.showinfo("Authentication", "Login successful")
            login_window.destroy()
            main_menu()  # Go to main menu
        else:
            messagebox.showerror("Authentication", "Invalid username or password")

        cursor.close()
        db_connection.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Function for displaying the main menu
def main_menu():
    menu_window = tk.Tk()
    menu_window.title("Main Menu")
    menu_window.geometry("400x300")  # Set the window size to 400x300
    new_game_button = tk.Button(menu_window, text="New Game", command=select_faction)
    new_game_button.pack(pady=10)

    load_game_button = tk.Button(menu_window, text="Load Game", command=load_game)
    load_game_button.pack(pady=10)

    quit_button = tk.Button(menu_window, text="Quit", command=menu_window.destroy)
    quit_button.pack(pady=10)

    menu_window.mainloop()

# Function for loading a game
def load_game():
    load_window = tk.Toplevel()
    load_window.title("Load Game")
    load_window.geometry("400x300")
    db_connection = db_connect()
    if db_connection is None:
        return

    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT ID_Game, game_name FROM game WHERE player_ID_Player = %s", (current_user_id,))
        games = cursor.fetchall()
        cursor.close()
        db_connection.close()

        if not games:
            messagebox.showinfo("No Games", "No games available")
            load_window.destroy()
            return

        game_listbox = tk.Listbox(load_window)
        for game in games:
            game_listbox.insert(tk.END, game[1])
        game_listbox.pack(pady=10)

        def load_selected_game():
            selected_game_index = game_listbox.curselection()
            if not selected_game_index:
                messagebox.showerror("Error", "Please select a game")
                return

            selected_game = games[selected_game_index[0]]
            game_id = selected_game[0]

            # Load the selected game
            # Here you can add the logic to load the selected game

            messagebox.showinfo("Load Game", f"Game '{selected_game[1]}' loaded successfully")
            load_window.destroy()
            main_window()

        load_game_button = tk.Button(load_window, text="Load Game", command=load_selected_game)
        load_game_button.pack(pady=10)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Function for selecting a faction
def select_faction():
    faction_window = tk.Toplevel()
    faction_window.title("Select Faction")
    faction_window.geometry("400x300")

    db_connection = db_connect()
    if db_connection is None:
        return

    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT ID_F, Name FROM faction")
        factions = cursor.fetchall()
        cursor.close()
        db_connection.close()

        if not factions:
            messagebox.showinfo("No Factions", "No factions available")
            faction_window.destroy()
            return

        faction_listbox = tk.Listbox(faction_window, selectmode=tk.SINGLE)
        for faction in factions:
            faction_listbox.insert(tk.END, faction[1])
        faction_listbox.pack(pady=10)

        def save_faction():
            selected_faction_index = faction_listbox.curselection()
            if not selected_faction_index:
                messagebox.showerror("Error", "Please select a faction")
                return

            selected_faction = factions[selected_faction_index[0]]
            global current_faction_id
            current_faction_id = selected_faction[0]

            messagebox.showinfo("Selection", f"Faction '{selected_faction[1]}' selected")
            faction_window.destroy()
            select_map()  # Proceed to map selection

        save_faction_button = tk.Button(faction_window, text="Select Faction", command=save_faction)
        save_faction_button.pack(pady=10)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Function for selecting a map
def select_map():
    map_window = tk.Toplevel()
    map_window.title("Select Map")
    map_window.geometry("400x300")

    db_connection = db_connect()
    if db_connection is None:
        return

    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT ID_Map, Map_Name FROM map")
        maps = cursor.fetchall()
        cursor.close()
        db_connection.close()

        if not maps:
            messagebox.showinfo("No Maps", "No maps available")
            map_window.destroy()
            return

        map_listbox = tk.Listbox(map_window, selectmode=tk.SINGLE)
        for map in maps:
            map_listbox.insert(tk.END, map[1])
        map_listbox.pack(pady=10)

        game_name_label = tk.Label(map_window, text="Game Name:")
        game_name_label.pack(pady=5)
        game_name_entry = tk.Entry(map_window)
        game_name_entry.pack(pady=5)

        def save_map():
            selected_map_index = map_listbox.curselection()
            if not selected_map_index:
                messagebox.showerror("Error", "Please select a map")
                return

            selected_map = maps[selected_map_index[0]]
            global current_map_id
            current_map_id = selected_map[0]
            game_name = game_name_entry.get()

            if not game_name:
                messagebox.showerror("Error", "Please enter a game name")
                return

            db_connection = db_connect()
            if db_connection is None:
                return

            try:
                cursor = db_connection.cursor()
                current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                sql_query = "INSERT INTO game (game_name, DATA, player_ID_Player) VALUES (%s, %s, %s)"
                cursor.execute(sql_query, (game_name, current_date, current_user_id,))
                db_connection.commit()

                cursor.close()
                db_connection.close()

                messagebox.showinfo("Game Creation", f"Game '{game_name}' created successfully")
                map_window.destroy()
                main_window()  # Proceed to the main game window
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        save_map_button = tk.Button(map_window, text="Select Map", command=save_map)
        save_map_button.pack(pady=10)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        
        
# Function for displaying the main game window
def main_window():
    window = tk.Tk()
    window.title("Main Game")
    window.geometry("400x300")

    resources_label = tk.Label(window, text="Resources: Gold 0, Wood 0, Stone 0, Iron 0")
    resources_label.pack(pady=5)

    buildings_label = tk.Label(window, text="Buildings: 0")
    buildings_label.pack(pady=5)

    units_label = tk.Label(window, text="Units: 0")
    units_label.pack(pady=5)

    def update_labels():
        db_connection = db_connect()
        if db_connection is None:
            return

        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT gold, wood, stone, iron FROM player WHERE ID_Player = %s", (current_user_id,))
            player_resources = cursor.fetchone()
            resources_label.config(text=f"Resources: Gold {player_resources[0]}, Wood {player_resources[1]}, Stone {player_resources[2]}, Iron {player_resources[3]}")

            cursor.execute("SELECT b.name, COUNT(*) FROM player_building pb JOIN building b ON pb.ID_Building = b.ID_Building WHERE pb.ID_Player = %s GROUP BY b.name", (current_user_id,))
            buildings = cursor.fetchall()
            buildings_text = "Buildings: " + ", ".join([f"{building[0]} x{building[1]}" for building in buildings])
            buildings_label.config(text=buildings_text)

            cursor.execute("SELECT u.Unit_Name, COUNT(*) FROM player_unit pu JOIN unit u ON pu.ID_U = u.ID_U WHERE pu.ID_Player = %s GROUP BY u.Unit_Name", (current_user_id,))
            units = cursor.fetchall()
            units_text = "Units: " + ", ".join([f"{unit[0]} x{unit[1]}" for unit in units])
            units_label.config(text=units_text)

            cursor.close()
            db_connection.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    build_building_button = tk.Button(window, text="Build Building", command=lambda: build_building(window, update_labels))
    build_building_button.pack(pady=10)

    create_unit_button = tk.Button(window, text="Create Unit", command=lambda: create_unit(window, update_labels))
    create_unit_button.pack(pady=10)



    next_turn_button = tk.Button(window, text="Next Turn", command=lambda: next_turn(update_labels))
    next_turn_button.pack(pady=10)

    update_labels()
    window.mainloop()

def build_building(parent_window, update_labels):
    building_window = tk.Toplevel(parent_window)
    building_window.title("Build Building")
    building_window.geometry("400x300")

    db_connection = db_connect()
    if db_connection is None:
        return

    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT ID_Building, name, Type, Production_of_resources FROM building")
        buildings = cursor.fetchall()

        if not buildings:
            messagebox.showinfo("No Buildings", "No buildings available")
            building_window.destroy()
            return

        building_listbox = tk.Listbox(building_window)
        for building in buildings:
            building_listbox.insert(tk.END, f"{building[1]} ({building[2]})")
        building_listbox.pack(pady=10)

        def save_building():
            selected_building_index = building_listbox.curselection()
            if not selected_building_index:
                messagebox.showerror("Error", "Please select a building")
                return

            selected_building = buildings[selected_building_index[0]]
            building_id = selected_building[0]

            db_connection = db_connect()
            if db_connection is None:
                return

            try:
                cursor = db_connection.cursor()

                # Fetch the cost of the selected building from the supplies table
                cursor.execute("""
                    SELECT s.resource_ID_R, r.Resource_Name, s.amount 
                    FROM supplies s 
                    JOIN resource r ON s.resource_ID_R = r.ID_R 
                    WHERE s.building_ID_Building = %s
                """, (building_id,))
                costs = cursor.fetchall()

                # Fetch the player's current resources
                cursor.execute("SELECT gold, wood, stone, iron FROM player WHERE ID_Player = %s", (current_user_id,))
                player_resources = cursor.fetchone()

                # Create a dictionary to hold the resource cost
                resource_cost = {'gold': 0, 'wood': 0, 'stone': 0, 'iron': 0}
                for cost in costs:
                    if cost[1] == 'gold':
                        resource_cost['gold'] = cost[2]
                    elif cost[1] == 'wood':
                        resource_cost['wood'] = cost[2]
                    elif cost[1] == 'stone':
                        resource_cost['stone'] = cost[2]
                    elif cost[1] == 'iron':
                        resource_cost['iron'] = cost[2]

                # Check if the player has enough resources
                if (player_resources[0] < resource_cost['gold'] or 
                    player_resources[1] < resource_cost['wood'] or 
                    player_resources[2] < resource_cost['stone'] or 
                    player_resources[3] < resource_cost['iron']):
                    messagebox.showerror("Error", "Insufficient resources")
                    return

                # Deduct the cost from the player's resources
                cursor.execute("""
                    UPDATE player 
                    SET gold = gold - %s, wood = wood - %s, stone = stone - %s, iron = iron - %s 
                    WHERE ID_Player = %s
                """, (resource_cost['gold'], resource_cost['wood'], resource_cost['stone'], resource_cost['iron'], current_user_id))

                # Insert the building into the player_building table
                cursor.execute("INSERT INTO player_building (ID_Player, ID_Building) VALUES (%s, %s)", (current_user_id, building_id))
                db_connection.commit()

                cursor.close()
                db_connection.close()

                messagebox.showinfo("Build Building", f"Building '{selected_building[1]}' built successfully")
                building_window.destroy()
                update_labels()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        build_button = tk.Button(building_window, text="Build", command=save_building)
        build_button.pack(pady=10)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")


def create_unit(parent_window, update_labels):
    unit_window = tk.Toplevel(parent_window)
    unit_window.title("Create Unit")
    unit_window.geometry("400x300")

    db_connection = db_connect()
    if db_connection is None:
        return

    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT ID_U, Unit_Name, Power, Health FROM unit")
        units = cursor.fetchall()
        cursor.close()
        db_connection.close()

        if not units:
            messagebox.showinfo("No Units", "No units available")
            unit_window.destroy()
            return

        unit_listbox = tk.Listbox(unit_window)
        for unit in units:
            unit_listbox.insert(tk.END, f"{unit[1]} (Strength: {unit[2]}, HP: {unit[3]})")
        unit_listbox.pack(pady=10)

        def save_unit():
            selected_unit_index = unit_listbox.curselection()
            if not selected_unit_index:
                messagebox.showerror("Error", "Please select a unit")
                return

            selected_unit = units[selected_unit_index[0]]
            unit_id = selected_unit[0]

            db_connection = db_connect()
            if db_connection is None:
                return

            try:
                cursor = db_connection.cursor()
                cursor.execute("INSERT INTO player_unit (ID_Player, ID_U) VALUES (%s, %s)", (current_user_id, unit_id))
                db_connection.commit()
                cursor.close()
                db_connection.close()

                messagebox.showinfo("Create Unit", f"Unit '{selected_unit[1]}' created successfully")
                unit_window.destroy()
                update_labels()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        create_button = tk.Button(unit_window, text="Create", command=save_unit)
        create_button.pack(pady=10)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Function for updating resources in the next turn
def next_turn(update_labels):
    db_connection = db_connect()
    if db_connection is None:
        return

    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT ID_Building FROM player_building WHERE ID_Player = %s", (current_user_id,))
        player_buildings = cursor.fetchall()

        for building in player_buildings:
            building_id = building[0]
            cursor.execute("SELECT Production_of_resources FROM building WHERE ID_Building = %s", (building_id,))
            production = cursor.fetchone()[0]

            if building_id == 1:  # Assuming building ID 1 is for gold production
                cursor.execute("UPDATE player SET gold = gold + %s WHERE ID_Player = %s", (production, current_user_id))
            elif building_id == 3:  # Assuming building ID 2 is for wood production
                cursor.execute("UPDATE player SET wood = wood + %s WHERE ID_Player = %s", (production, current_user_id))
            elif building_id == 4:  # Assuming building ID 3 is for stone production
                cursor.execute("UPDATE player SET stone = stone + %s WHERE ID_Player = %s", (production, current_user_id))
            elif building_id == 2:  # Assuming building ID 4 is for iron production
                cursor.execute("UPDATE player SET iron = iron + %s WHERE ID_Player = %s", (production, current_user_id))

            db_connection.commit()

        cursor.close()
        db_connection.close()
        
        update_labels()
        messagebox.showinfo("Next Turn", "Resources updated for the next turn")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")



# Main login window
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("400x300")

username_label = tk.Label(login_window, text="Username:")
username_label.pack(pady=5)
username_entry = tk.Entry(login_window)
username_entry.pack(pady=5)

password_label = tk.Label(login_window, text="Password:")
password_label.pack(pady=5)
password_entry = tk.Entry(login_window, show="*")
password_entry.pack(pady=5)

login_button = tk.Button(login_window, text="Login", command=authenticate)
login_button.pack(pady=10)

register_button = tk.Button(login_window, text="Register", command=register)
register_button.pack(pady=10)

login_window.mainloop()