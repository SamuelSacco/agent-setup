TABLES: dict[str, dict] = {"posts": {}}

def put(table: str, key: str, row: dict) -> None:
    TABLES[table][key] = row

def get(table: str, key: str) -> dict | None:
    return TABLES[table].get(key)
