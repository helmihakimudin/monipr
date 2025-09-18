import pyodbc

def get_erp_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=192.168.3.120;"     # ganti dengan host ERP
        "DATABASE=sma107;"    # ganti nama DB ERP
        "UID=sa;"             # ganti user ERP
        "PWD=admin1234%;"         # ganti password ERP
    )
    return conn
