# Tiny in-memory stand-in for the users database.
TABLES: dict[str, dict] = {"users": {}}

def put(table: str, key: str, row: dict) -> None:
    TABLES[table][key] = row

def get(table: str, key: str) -> dict | None:
    return TABLES[table].get(key)

def delete(table: str, key: str) -> None:
    TABLES[table].pop(key, None)
