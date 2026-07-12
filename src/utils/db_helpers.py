from db import get_connection


def fetch_one(sql: str, params: tuple = ()):
    con = get_connection()
    row = con.execute(sql, params).fetchone()
    con.close()
    return dict(row) if row else None


def fetch_all(sql: str, params: tuple = ()) -> list:
    con = get_connection()
    rows = con.execute(sql, params).fetchall()
    con.close()
    return [dict(r) for r in rows]


def execute(sql: str, params: tuple = ()):
    con = get_connection()
    con.execute(sql, params)
    con.commit()
    con.close()


def upsert(table: str, data: dict, conflict_cols: list):
    cols = list(data.keys())
    placeholders = ', '.join(['?'] * len(cols))
    col_names = ', '.join(cols)
    updates = ', '.join([f"{c}=excluded.{c}" for c in cols if c not in conflict_cols])
    conflict = ', '.join(conflict_cols)
    sql = (
        f"INSERT INTO {table} ({col_names}) VALUES ({placeholders}) "
        f"ON CONFLICT({conflict}) DO UPDATE SET {updates}"
    )
    con = get_connection()
    con.execute(sql, list(data.values()))
    con.commit()
    con.close()
