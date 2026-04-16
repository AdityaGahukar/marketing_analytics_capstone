import sqlparse

ALLOWED_TABLE = "gold_sales"
ALLOWED_COLUMNS = [
    "order_id",
    "sales_amount",
    "country",
    "product_category",
    "order_date"
]


def validate_sql(query):

    query_upper = query.upper()

   
    if not query_upper.startswith("SELECT"):
        return False, "Only SELECT queries allowed"

   
    forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", ";"]

    for word in forbidden:
        if word in query_upper:
            return False, f"Forbidden keyword: {word}"

    
    if "LIMIT" not in query_upper:
        return False, "LIMIT is required"

   
    if ALLOWED_TABLE not in query:
        return False, "Invalid table used"

    return True, "Valid query"