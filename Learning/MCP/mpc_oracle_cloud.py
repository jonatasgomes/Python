from mcp.server.fastmcp import FastMCP
import oracledb
import env

mcp = FastMCP(name="Oracle Cloud Connection")
_connection = None

def connect_to_db():
  global _connection
  _connection = oracledb.connect(user=env.USER, password=env.PASSWORD, dsn=env.DSN, tcp_connect_timeout=160, expire_time=4, retry_count=6, retry_delay=5)
  print('Connection created.')


@mcp.tool()
def hello_oracle_cloud(name: str) -> str:
    return f"Hello, {name}! Welcome to Oracle Cloud."


@mcp.tool()
def get_schemas() -> list[str]:
    """
    Return a list of all accessible Oracle schemas for the user.
    """
    global _connection
    if _connection is None:
        connect_to_db()
    try:
        with _connection.cursor() as cursor:
            cursor.execute("SELECT username FROM all_users ORDER BY username")
            rows = cursor.fetchall()
            return [row[0] for row in rows]
    except Exception as e:
        return [f"Error: {str(e)}"]


@mcp.tool()
def get_tables(schema: str) -> list[str]:
    """
    Return a list of all table names for the given schema.
    """
    global _connection
    if _connection is None:
        connect_to_db()
    try:
        with _connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name
                FROM all_tables
                WHERE owner = :schema
                ORDER BY table_name
            """, {"schema": schema.upper()})
            rows = cursor.fetchall()
            return [row[0] for row in rows]
    except Exception as e:
        return [f"Error: {str(e)}"]


@mcp.tool()
def describe_table(schema: str, table: str) -> list[dict]:
    """
    Returns the structure of a specified table (columns, data types, nullable).
    Args:
        schema: The schema name.
        table: The table name.
    Returns:
        List of dictionaries with column details or an error message.
    """
    global _connection
    if _connection is None:
        connect_to_db()
    try:
        with _connection.cursor() as cursor:
            cursor.execute("""
                SELECT column_name, data_type, nullable
                FROM all_tab_columns
                WHERE owner = :schema AND table_name = :table
                ORDER BY column_id
            """, {"schema": schema.upper(), "table": table.upper()})
            rows = cursor.fetchall()
            return [{"column_name": row[0], "data_type": row[1], "nullable": row[2]} for row in rows]
    except Exception as e:
        return [{"error": f"Error: {str(e)}"}]


@mcp.tool()
def get_table_row_count(schema: str, table_name: str) -> dict:
    """Get the approximate row count for a table"""
    global _connection
    if _connection is None:
        connect_to_db()
    try:
        with _connection.cursor() as cursor:
            cursor.execute("""
                SELECT num_rows, last_analyzed
                FROM all_tables
                WHERE owner = :schema AND table_name = :table_name
            """, {"schema": schema.upper(), "table_name": table_name.upper()})
            row = cursor.fetchone()
            if row:
                return {
                    "table": f"{schema}.{table_name}",
                    "num_rows": row[0],
                    "last_analyzed": str(row[1]) if row[1] else None,
                    "note": "Statistics may be outdated if last_analyzed is old"
                }
            else:
                return {"error": "Table not found"}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def execute_query(query: str) -> list[dict]:
    """
    Executes a custom SELECT SQL query and returns the results.
    Args:
        query: The SQL SELECT query to execute.
    Returns:
        List of dictionaries with query results or an error message.
    """
    global _connection
    if _connection is None:
        connect_to_db()
    if not query.strip().upper().startswith("SELECT"):
        return [{"error": "Only SELECT queries are allowed."}]
    try:
        with _connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        return [{"error": f"Error: {str(e)}"}]


@mcp.tool()
def list_tools() -> list[dict]:
    """
    Returns a list of available tools and their descriptions.
    Returns:
        List of dictionaries with tool names and descriptions.
    """
    tools = mcp.get_tools()
    return [{"name": name, "description": tool.__doc__.strip() if tool.__doc__ else "No description available"} for name, tool in tools.items()]


if __name__ == "__main__":
    mcp.run(transport='stdio')
