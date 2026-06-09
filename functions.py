import os
from validations import (
    valid_roles,
    validate_name,
    validate_email_format,
    validate_unique_email,
    validate_role_selection,
    get_role_by_index,
    read_single_key,
)

RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"

users = [
    {"id": 1, "name": "Ana García",     "email": "ana.garcia@gmail.com",     "role": "Backend"},
    {"id": 2, "name": "Luis Pérez",     "email": "luis.perez@gmail.com",     "role": "Frontend"},
    {"id": 3, "name": "María López",    "email": "maria.lopez@gmail.com",    "role": "Designer UX"},
    {"id": 4, "name": "Julian Alvarez", "email": "alvarez.julian@gmail.com", "role": "Designer UI"},
    {"id": 5, "name": "Santi Tilin",   "email": "santi.tilin@gmail.com",     "role": "Backend"},
    {"id": 6, "name": "Ezequiel Kaczuba", "email": "kaczuba-eze@gmail.com", "role": "Backend"},
]

#   Support functions

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def _next_id():
    return max((u["id"] for u in users), default=0) + 1

def _find_user(user_id):
    for u in users:
        if u["id"] == user_id:
            return u
    return None

def _request_field(prompt, validator=None, error_message="Valor inválido.", required=True):
    while True:
        value = input(prompt).strip()
        
        if value.lower() in ['salir', 's'] and (required or value):
            confirm = input(f"{YELLOW}¿Deseas cancelar la operación actual? (s/n): {RESET}").strip().lower()
            if confirm == 's':
                raise ValueError("Operación cancelada.")
            else:
                continue

        if required and not value:
            print(f"{RED}Este campo no puede estar vacío.{RESET}")
            continue
        if not value and not required:
            return value
        if value and validator and not validator(value):
            print(f"{RED}{error_message}{RESET}")
            continue
        return value

#   Key functions

def list_users(filtered_list=None, title="LISTADO DE USUARIOS"):
    target_list = users if filtered_list is None else filtered_list
    page_size = 5
    current_page = 0
    
    while True:
        clear_screen()
        total_users = len(target_list)
        total_pages = (total_users + page_size - 1) // page_size if total_users > 0 else 1
        
        print(f"{CYAN}┌───────────────────────────────────────────────────────────────┐{RESET}")
        print(f"{CYAN}│{RESET}{BOLD}{title.center(63)}{RESET}{CYAN}│{RESET}")
        print(f"{CYAN}└───────────────────────────────────────────────────────────────┘{RESET}")
        
        if not target_list:
            print(f"  {YELLOW}⚠ No se encontraron usuarios registrados.{RESET}\n")
            input("  Presione Enter para continuar...")
            break
        else:
            print(f"  {CYAN}┌──────┬──────────────────────┬──────────────────────────┬──────────────┐{RESET}")
            print(f"  {CYAN}│{RESET} {BOLD}{'ID':<4}{RESET} {CYAN}│{RESET} {BOLD}{'Nombre':<20}{RESET} {CYAN}│{RESET} {BOLD}{'Email':<24}{RESET} {CYAN}│{RESET} {BOLD}{'Rol':<12}{RESET} {CYAN}│{RESET}")
            print(f"  {CYAN}├──────┼──────────────────────┼──────────────────────────┼──────────────┤{RESET}")
            
            start_idx = current_page * page_size
            end_idx = start_idx + page_size
            page_users = target_list[start_idx:end_idx]
            
            for u in page_users:
                short_name = u['name'] if len(u['name']) <= 20 else u['name'][:17] + "..."
                short_email = u['email'] if len(u['email']) <= 24 else u['email'][:21] + "..."
                
                print(f"  {CYAN}│{RESET} {u['id']:<4} {CYAN}│{RESET} {short_name:<20} {CYAN}│{RESET} {short_email:<24} {CYAN}│{RESET} {u['role']:<12} {CYAN}│{RESET}")
            
            print(f"  {CYAN}└──────┴──────────────────────┴──────────────────────────┴──────────────┘{RESET}")
            print(f"   {BOLD}Página:{RESET} {current_page + 1} / {total_pages}  {CYAN}│{RESET}  {BOLD}Total:{RESET} {total_users} usuarios")
            print(f"  {CYAN}───────────────────────────────────────────────────────────────{RESET}")
            
            options = []
            if current_page < total_pages - 1:
                options.append(f"{GREEN}[S]{RESET} Siguiente")
            if current_page > 0:
                options.append(f"{GREEN}[A]{RESET} Anterior")
            options.append(f"{RED}[M]{RESET} Volver al menú")
            
            print(f"  Controles: {' • '.join(options)}")
            print("  Presioná una tecla de control...")
            
            nav = read_single_key()
            
            if nav == 's' and current_page < total_pages - 1:
                current_page += 1
            elif nav == 'a' and current_page > 0:
                current_page -= 1
            elif nav == 'm':
                break

def search_users():
    clear_screen()
    print(f"{CYAN}{BOLD}--- BUSCAR USUARIOS ---{RESET}\n")
    query = input("Ingresá tu término de búsqueda (nombre, email o rol): ").strip().lower()
    
    if not query:
        print(f"\n{YELLOW}Búsqueda cancelada por término vacío.{RESET}\n")
        input("Presione Enter para continuar...")
        return

    results = [
        u for u in users 
        if query in u["name"].lower() or query in u["email"].lower() or query in u["role"].lower()
    ]
    
    list_users(filtered_list=results, title=f"RESULTADOS DE: '{query.upper()}'")

def create_user():
    clear_screen()
    print(f"{GREEN}{BOLD}--- ALTA DE USUARIO ---{RESET}")
    print(f"{YELLOW}(Escribe 'salir' en cualquier momento para cancelar){RESET}\n")

    try:
        name = _request_field(
            "Ingrese un nombre: ",
            validator=validate_name,
            error_message="El nombre no es válido (letras, espacios y sin patrones repetidos).",
        )

        email = _request_field(
            "Ingrese un email: ",
            validator=lambda e: validate_email_format(e) and validate_unique_email(e, users),
            error_message="El email no tiene un formato válido o ya está registrado.",
        )

        print(f"\n{BOLD}Roles disponibles:{RESET}")
        for i, r in enumerate(valid_roles, 1):
            print(f"  {i}. {r}")
            
        role_input = _request_field(
            f"Seleccione el número de rol (1-{len(valid_roles)}): ",
            validator=validate_role_selection,
            error_message="Selección inválida. Elija un número de la lista.",
        )
        role = get_role_by_index(role_input)

        new_user = {"id": _next_id(), "name": name, "email": email, "role": role}
        users.append(new_user)
        print(f"\n{GREEN}✔ Usuario '{name}' dado de alta con ID {new_user['id']}.{RESET}\n")
        
    except ValueError as e:
        print(f"\n{RED}❌ {e}{RESET}\n")
    
    input("Presione Enter para continuar...")

def update_user():
    clear_screen()
    print(f"{YELLOW}{BOLD}--- MODIFICAR USUARIO ---{RESET}")
    print(f"{YELLOW}(Escribe 'salir' en cualquier momento para cancelar){RESET}\n")
    
    print("Usuarios disponibles:")
    for u in users:
        print(f"  ID: {u['id']} | {u['name']}")
    print()
    
    try:
        user_id_input = input("ID del usuario a modificar: ").strip()
        if user_id_input.lower() in ['salir', 's']:
            print(f"\n{RED}Operación cancelada.{RESET}\n")
            input("Presione Enter para continuar...")
            return
            
        user_id = int(user_id_input)
    except ValueError:
        print(f"{RED}ID inválido.{RESET}\n")
        input("Presione Enter para continuar...")
        return

    user = _find_user(user_id)
    if not user:
        print(f"{RED}No existe un usuario con ID {user_id}.{RESET}\n")
        input("Presione Enter para continuar...")
        return

    print(f"\nEditando: {BOLD}{user['name']}{RESET} | {user['email']} | {user['role']}")
    print(f"  {YELLOW}(Dejá en blanco los campos que no querés cambiar){RESET}\n")

    try:
        name = _request_field(
            f"Nuevo nombre  [{user['name']}]: ",
            validator=validate_name,
            error_message="El nombre no es válido.",
            required=False,
        )

        email = _request_field(
            f"Nuevo email   [{user['email']}]: ",
            validator=lambda e: validate_email_format(e) and validate_unique_email(e, users, exclude_id=user_id),
            error_message="El email no es válido o ya está registrado.",
            required=False,
        )

        print(f"\n{BOLD}Roles disponibles:{RESET}")
        for i, r in enumerate(valid_roles, 1):
            print(f"  {i}. {r}")
            
        role_input = _request_field(
            f"Nuevo rol     [{user['role']}] (Seleccione 1-{len(valid_roles)}): ",
            validator=validate_role_selection,
            error_message="Selección inválida. Elija un número de la lista.",
            required=False,
        )

        changes = []
        if name:
            user["name"] = name
            changes.append("nombre")
        if email:
            user["email"] = email
            changes.append("email")
        if role_input:
            user["role"] = get_role_by_index(role_input)
            changes.append("rol")

        if changes:
            print(f"\n{GREEN}✔ Campos actualizados: {', '.join(changes)}.{RESET}\n")
        else:
            print(f"\n{YELLOW}No se realizaron cambios.{RESET}\n")
            
    except ValueError as e:
        print(f"\n{RED}❌ {e}{RESET}\n")
    
    input("Presione Enter para continuar...")

def delete_user():
    clear_screen()
    print(f"{RED}{BOLD}--- BAJA DE USUARIO ---{RESET}\n")
    
    print("Usuarios disponibles:")
    for u in users:
        print(f"  ID: {u['id']} | {u['name']}")
    print()
    
    try:
        user_id_input = input("ID del usuario a eliminar: ").strip()
        if user_id_input.lower() in ['salir', 's']:
            print(f"\n{RED}❌ Operación cancelada.{RESET}\n")
            input("Presione Enter para continuar...")
            return
            
        user_id = int(user_id_input)
    except ValueError:
        print(f"{RED}ID inválido.{RESET}\n")
        input("Presione Enter para continuar...")
        return

    user = _find_user(user_id)
    if not user:
        print(f"{RED}No existe un usuario con ID {user_id}.{RESET}\n")
        input("Presione Enter para continuar...")
        return

    confirm = input(f"¿Seguro que querés eliminar a '{RED}{user['name']}{RESET}'? (s/n): ").strip().lower()
    if confirm == "s":
        users.remove(user)
        print(f"\n{GREEN}✔ Usuario '{user['name']}' eliminado.{RESET}\n")
    else:
        print(f"\n{YELLOW}Operación cancelada.{RESET}\n")
        
    input("Presione Enter para continuar...")