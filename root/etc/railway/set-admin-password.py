"""
Railway template: replaces the admin user's default password (admin123).

- Does nothing if ADMIN_PASSWORD is empty.
- Only changes the password while it is still the default 'admin123'. If the
  user has changed it in the app, it is left alone, so restarts never
  overwrite the user's own password.
"""
import os
import sqlite3
import sys

from werkzeug.security import check_password_hash, generate_password_hash

DEFAULT_PASSWORD = "admin123"
DB_PATH = os.environ.get("RAILWAY_APP_DB", "/config/app.db")
TAG = "[railway-admin-password]"


def main() -> int:
    new_password = os.environ.get("ADMIN_PASSWORD", "")
    if not new_password:
        print(f"{TAG} ADMIN_PASSWORD is not set; the default password (admin123) is still active. Change it now!")
        return 0
    if new_password == DEFAULT_PASSWORD:
        print(f"{TAG} ADMIN_PASSWORD equals the default password; nothing changed.")
        return 0
    if not os.path.exists(DB_PATH):
        print(f"{TAG} {DB_PATH} not found; skipping.")
        return 0

    con = sqlite3.connect(DB_PATH, timeout=30)
    try:
        row = con.execute(
            "SELECT id, password FROM user WHERE lower(name) = 'admin'"
        ).fetchone()
        if row is None:
            print(f"{TAG} No 'admin' user found; skipping.")
            return 0
        user_id, current_hash = row
        if not current_hash or not check_password_hash(str(current_hash), DEFAULT_PASSWORD):
            print(f"{TAG} Admin password was already changed; leaving it alone.")
            return 0
        con.execute(
            "UPDATE user SET password = ? WHERE id = ?",
            (generate_password_hash(new_password), user_id),
        )
        con.commit()
        print(f"{TAG} Admin password set from ADMIN_PASSWORD.")
        return 0
    finally:
        con.close()


if __name__ == "__main__":
    sys.exit(main())
