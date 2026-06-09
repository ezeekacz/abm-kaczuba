from functions import list_users, search_users, create_user, update_user, delete_user, clear_screen, CYAN, BOLD, RESET
from validations import read_single_key

def menu():
    while True:
        clear_screen()
        print(f"{CYAN}{'=' * 46}{RESET}")
        print(f"{CYAN}{BOLD}       PANEL ADMINISTRATIVO DE USUARIOS{RESET}")
        print(f"{CYAN}{'=' * 46}{RESET}")
        print("1. Listar usuarios")
        print("2. Buscar / Filtrar usuarios")
        print("3. Dar de alta un usuario")
        print("4. Modificar un usuario")
        print("5. Eliminar un usuario")
        print("0. Salir")
        print()
        print("Elegí una opción (presioná la tecla): ")

        option = read_single_key()

        if option == "1":
            list_users() 
        elif option == "2":
            search_users() 
        elif option == "3":
            create_user()
        elif option == "4":
            update_user()
        elif option == "5":
            delete_user()
        elif option == "0":
            print("\nSaliendo del sistema...\n")
            break

if __name__ == "__main__":
    menu()