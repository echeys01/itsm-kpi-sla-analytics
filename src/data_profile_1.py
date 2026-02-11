from pathlib import Path 
import csv, sqlite3
import pandas as pd, numpy as np

ROOT_DIR = Path(__file__).resolve().parent.parent

DB_PATH = ROOT_DIR / "output" / "itsm_bpi2014.db"
XLSX_PATH = ROOT_DIR / "output" / "kpi_report_bpi2014.xlsx"

def main():
    print("Database path: ", DB_PATH) # Sanity checks for working db, project directory.
    print("Working directory: ", Path.cwd())

    conn = None

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()

    except OSError as os_e: 
        print({os_e})
        if conn is None:
            return conn

    except sqlite3.Error as sql_e:
        print({sql_e})
        if conn is None:
            return conn

    csv_change_data = "data/raw/Detail_Change.csv"
    load_csv_data(csv_change_data, conn)

    conn.close() # type: ignore    
# end main


def load_csv_data(csv_data, conn) -> None:
    df = pd.read_csv(csv_data, sep=';') # Create DataFrame (df) from ITSM change data.
    
    # Obtain shape of DataFrame.
    get_df_shape(df)

    df.info()
    print(df.isna().sum())

    print(standardize_columns(df))
    
    
# end load_csv_data
    

# def load_incident_activity()

# def load_incident_data()

# def load_interaction_data() 


def get_df_shape(df) -> None:
    row_count = df.shape[0]
    col_count = df.shape[1]

    print(f"Number of rows: ", row_count)
    print(f"Number of columns: ", col_count)
# end get_df_shape    


def standardize_columns(df) -> pd.DataFrame:
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_", regex=True)
    return df
# end standardize_columns

if __name__ == "__main__":
    main()

