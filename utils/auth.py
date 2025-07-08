from utils.db import get_db_connection, hash_password


def authenticate_user(email: str, password: str, role: str) -> bool:
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("SELECT password, role FROM users WHERE email = ?", (email,))
    result = c.fetchone()
    conn.close()

    if not result:
        print(f"No user found with email: {email}")
        return False

    stored_hash, stored_role = result
    input_hash = hash_password(password)

    print(f"Auth Check: {input_hash == stored_hash} (pwd), {role.strip() == stored_role.strip()} (role)")
    return input_hash == stored_hash and role.strip() == stored_role.strip()