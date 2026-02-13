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
        print(f"File-related error encountered: {os_e}")
        if conn is None:
            return conn

    except sqlite3.Error as sql_e:
        print(f"Database connection/config error encountered: {sql_e}")
        if conn is None:
            return conn
    # try: ...

    # Load raw data first by number of CSV source files.
    incidents_csv = "data/raw/Detail_Incident.csv"
    load_incident_data(incidents_csv, conn)

    incident_activity_csv = "data/raw/Detail_Incident_Activity.csv"
    load_incident_activity_data(incident_activity_csv, conn)

    interactions_csv = "data/raw/Detail_Interaction.csv"
    load_interaction_data(interactions_csv, conn)

    csv_change_data = "data/raw/Detail_Change.csv"
    load_change_data(csv_change_data, conn)

    conn.close() # type: ignore    
# end main


def load_incident_data(incidents_csv, conn) -> None:
    y = 1 # placeholder
    df = pd.read_csv(incidents_csv, sep=';')
# end load_incident_data


def load_incident_activity_data(incident_activity_csv, conn) -> None:
    df = pd.read_csv(incident_activity_csv, sep=';')
# end load_incident_activity_data    


def load_interaction_data(interactions_csv, conn) -> None:
    pd.read_csv(interactions_csv, sep=';')
# end load_interaction_data
    

def load_change_data(csv_change_data, conn) -> None:
    df = pd.read_csv(csv_change_data, sep=';') # Create DataFrame (df) from ITSM change data.
    
    # Obtain shape of DataFrame (rows x cols).
    get_df_shape(df)

    df.info()
    print(df.isna().sum())

    print(standardize_columns(df)) # Ensure columns are lowercase, have underscore.

    df.to_sql(
        "raw_changes",
        conn,
        if_exists="replace",
        index=False,
        chunksize=5000,
        method="multi"
    ) # Create separate table to hold initial raw data.

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS incidents (
        
        
        
        )
        """
    )
              
# end load_change_data


def get_df_shape(df) -> None: # Basic helper function to check df dimensions.
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

