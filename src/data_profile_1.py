from pathlib import Path 
import csv, sqlite3
import pandas as pd, numpy as np

ROOT_DIR = Path(__file__).resolve().parent.parent

DB_PATH = "ROOT_DIR / output / itsm_bpi2014.db"
XLSX_PATH = "ROOT_DIR / output / kpi_report_bpi2014.xlsx"

def main():
    conn = None

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()

    except OSError as os_e: 
        print({os_e})

    except sqlite3.Error as sql_e:
        print({sql_e})

    csv_change_data = "data/raw/Detail_Change.csv"
    load_change_data(csv_change_data, conn)

    conn.close() # type: ignore    
# end main

def load_change_data(csv_change_data, conn) -> None:
    df_change_data = pd.read_csv(csv_change_data)
    conn



# def load_incident_activity()

# def load_incident_data()

# def load_interaction_data() 







if __name__ == "__main__":
    main()

