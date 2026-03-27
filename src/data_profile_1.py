from pathlib import Path 
import sqlite3
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent

DB_PATH = ROOT_DIR / "output" / "itsm_bpi2014.db"
XLSX_PATH = ROOT_DIR / "output" / "kpi_report_bpi2014.xlsx"

DEBUG_RAW_COLS = False # Flag for printing initial raw columns.

def main():
    print("Database path: ", DB_PATH) # Sanity checks for working db, project directory.
    print("Working directory: ", Path.cwd())

    conn = None

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        print(conn.execute("PRAGMA database_list;").fetchall())

        # Drop table statements inserted for testing purposes.
        conn.execute("DROP TABLE IF EXISTS incident_activity;")
        conn.execute("DROP TABLE IF EXISTS incidents;")
        conn.execute("DROP TABLE IF EXISTS interactions;")
        conn.execute("DROP TABLE IF EXISTS itsm_changes;")

    except OSError as os_e: 
        print(f"File-related error encountered: {os_e}")
        if conn is None:
            return

    except sqlite3.Error as sql_e:
        print(f"Database connection/config error encountered: {sql_e}")
        if conn is None:
            return 
    # try: ...

    # Load raw data first by number of CSV source files.
    incidents_csv = ROOT_DIR / "data" / "raw" / "Detail_Incident.csv"
    load_incident_data(incidents_csv, conn)

    interactions_csv = ROOT_DIR / "data" / "raw" / "Detail_Interaction.csv"
    load_interaction_data(interactions_csv, conn)

    incident_activity_csv = ROOT_DIR / "data" / "raw" / "Detail_Incident_Activity.csv"
    load_incident_activity_data(incident_activity_csv, conn)

    csv_change_data = ROOT_DIR / "data" / "raw" / "Detail_Change.csv"
    load_change_data(csv_change_data, conn)

    conn.close() # type: ignore    
# end main


def load_incident_data(incidents_csv, conn) -> None:
    df = pd.read_csv(incidents_csv, sep=';', low_memory=False) # Create DataFrame (df) from ITSM change data.

    # Obtain shape of DataFrame (rows x cols).
    get_df_shape(df)
    df = standardize_columns(df) # Ensure columns are lowercase, snake_case.
    #print(df.columns)

    df = normalize_id_columns(df, ["incident_id"])
    df = normalize_datetime_columns(df, ["open_time", "reopen_time", "resolved_time", "close_time"])

    df.to_sql(
        "raw_incidents",
        conn,
        if_exists="replace",
        index=False,
        chunksize=1000,
    ) # Create separate table to hold initial raw data.

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS incidents (
            incident_id TEXT NOT NULL PRIMARY KEY,  
            ci_name TEXT,
            ci_type TEXT,
            priority TEXT,
            service_component TEXT
        );
        """
    ) 

    conn.execute(
        """
        INSERT OR REPLACE INTO incidents (
            incident_id, 
            ci_name, 
            ci_type, 
            priority, 
            service_component
        )

        SELECT 
            incident_id, 
            ci_name_aff AS ci_name, 
            ci_type_aff AS ci_type, 
            priority, 
            service_component_wbs_aff AS service_component
        FROM raw_incidents
        WHERE NULLIF(TRIM(incident_id), '') IS NOT NULL;
        """
    )    

    print_modeled_schema(conn, "incidents")
    conn.commit()
# end load_incident_data    


def load_interaction_data(interactions_csv, conn) -> None:
    df = pd.read_csv(interactions_csv, sep=';', low_memory=False)

    get_df_shape(df)
    df = standardize_columns(df) # Assign returned copy of DataFrame. 
    #print(df.columns)

    df = normalize_id_columns(df, ["interaction_id"])
    df = normalize_datetime_columns(df, ["open_time_first_touch", "close_time"])
    
    df.to_sql(
        "raw_interactions",
        conn,
        if_exists="replace",
        index=False,
        chunksize=1000
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS interactions (
            interaction_id TEXT NOT NULL,
            ci_name TEXT NOT NULL,
            ci_type TEXT NOT NULL,
            service_component TEXT,
            open_time TEXT NOT NULL,
            close_time TEXT NOT NULL,
            status TEXT NOT NULL,
            priority TEXT,
            category TEXT,
            PRIMARY KEY (interaction_id)
        );
        """
    )

    conn.execute(
        """
        INSERT OR REPLACE INTO interactions (
            interaction_id,
            ci_name, 
            ci_type,
            service_component,
            open_time,
            close_time,
            status,
            priority,
            category
        )

        SELECT 
            interaction_id, 
            ci_name_aff AS ci_name, 
            ci_type_aff AS ci_type, 
            service_comp_wbs_aff AS service_component, 
            open_time_first_touch AS open_time,
            close_time, 
            status, 
            priority, 
            category

        FROM raw_interactions;
        """
    )

    print_modeled_schema(conn, "interactions")
    conn.commit()
# end load_interaction_data


def load_incident_activity_data(incident_activity_csv, conn) -> None:
    df = pd.read_csv(incident_activity_csv, sep=';', low_memory=False)

    get_df_shape(df)
    df = standardize_columns(df)

    df = normalize_id_columns(df, ["incident_id", "interaction_id"])
    df = normalize_datetime_columns(df, ["datestamp"])

    df.to_sql(
        "raw_incident_activity",
        conn,
        if_exists="replace",
        index=False,
        chunksize=1000
    ) # Initial incident activity table (child of raw_incidents).

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS incident_activity (
            incident_id TEXT NOT NULL,
            interaction_id TEXT,
            incident_activity_number TEXT NOT NULL,
            incident_activity_type TEXT NOT NULL,
            date_stamp TEXT,
            assignment_group TEXT,
            FOREIGN KEY (incident_id) 
                REFERENCES incidents(incident_id),
            PRIMARY KEY (incident_id, incident_activity_number)
        );
        """
    )

    conn.execute(
        """
        INSERT OR REPLACE INTO incident_activity (
            incident_id,
            interaction_id,
            incident_activity_number,
            incident_activity_type,
            date_stamp,
            assignment_group
        )

        SELECT 
            incident_id, 
            interaction_id, 
            incidentactivity_number AS incident_activity_number, 
            incidentactivity_type AS incident_activity_type,
            datestamp as date_stamp, 
            assignment_group

        FROM raw_incident_activity AS ri
        WHERE ri.incident_id IN (SELECT incident_id FROM incidents); 
        """
    ) # Ensure presence of written entries for incident_id.
    
    print_modeled_schema(conn, "incident_activity")
    conn.commit()
# end load_incident_activity_data
    

def load_change_data(csv_change_data, conn) -> None:
    df = pd.read_csv(csv_change_data, sep=';', low_memory=False) 
    
    get_df_shape(df)
    df = standardize_columns(df)

    df = normalize_id_columns(df, ["change_id"])
    df = normalize_datetime_columns(df, ["planned_start", "planned_end", "actual_start", "actual_end"])

    df.to_sql(
        "raw_changes",
        conn,
        if_exists="replace",
        index=False,
        chunksize=1000
    ) 

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS itsm_changes (
            change_id TEXT NOT NULL,
            ci_name TEXT,
            ci_type TEXT,
            service_component TEXT,
            planned_start TEXT,
            planned_end TEXT,
            actual_start TEXT,
            actual_end TEXT,
            cab_approval_needed TEXT,
            related_interactions TEXT,
            related_incidents TEXT,
            PRIMARY KEY (change_id)
        )
        """
    )

    conn.execute (
        """
        INSERT OR REPLACE INTO itsm_changes (
            change_id,
            ci_name,
            ci_type,
            service_component,
            planned_start,
            planned_end,
            actual_start,
            actual_end,
            cab_approval_needed,
            related_interactions,
            related_incidents
        )

        SELECT 
            change_id, 
            ci_name_aff AS ci_name, 
            ci_type_aff AS ci_type, 
            service_component_wbs_aff AS service_component, 
            planned_start,
            planned_end, 
            actual_start, 
            actual_end, 
            cab_approval_needed,
            related_interactions, 
            related_incidents

        FROM raw_changes;
        """
    )

    print_modeled_schema(conn, "itsm_changes")
    conn.commit()          
# end load_change_data


def get_df_shape(df) -> None: # Basic helper function to check DataFrame dimensions.
    row_count = df.shape[0]
    col_count = df.shape[1]

    #print(f"Number of rows: ", row_count)
    #print(f"Number of columns: ", col_count)
# end get_df_shape    


def standardize_columns(df) -> pd.DataFrame: # Ensure collapse of additional underscores. 
    df = df.copy()
    
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r'[^\w]', "_", regex=True)
        .str.replace(r"_+", "_", regex=True)
        .str.strip("_")
    )

    df = df.loc[:, ~df.columns.str.contains(r"^unnamed")]
    return df
# end standardize_columns


# Basic helper for printing schema for each modeled table (to be expanded).
def print_modeled_schema(conn, table_name) -> None:
    schema = conn.execute(f"PRAGMA table_info({table_name});")
    print(table_name)
    print([col[1] for col in schema])
# end print_schema


# Helper functions for ISO date format normalization and invalid checks. 
def normalize_datetime_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    df = df.copy()
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")
            df[col] = df[col].dt.strftime("%Y-%m-%d %H:%M:%S")
    return df
# end normalize_datetime_columns


def normalize_id_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    df = df.copy()
    for col in columns:
        if col in df.columns:
            df[col] = df[col].where(df[col].notna(), str(None))
            df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
            df.loc[df[col] == "", col] = None
    return df
# end normalize_id_columns


if __name__ == "__main__":
    main()

