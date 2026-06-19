from pathlib import Path
import pandas as pd
import sqlite3

ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / "output" / "itsm_bpi2014.db"
EXCEL_PATH = ROOT_DIR / "output" / "kpi_report_bpi2014.xlsx"

def main():
    conn = None
    
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")

        # Construct dictionary 'kpi_output' of DataFrames to be written to Excel.
        kpi_output = {}
        kpi_output.update(read_incident_queries(conn))
        kpi_output.update(read_event_queries(conn))
        kpi_output.update(read_interaction_queries(conn))
        kpi_output.update(read_change_queries(conn))

        # Call Excel writer.
        write_to_excel(kpi_output, EXCEL_PATH)

    except OSError as os_e: 
        print(f"File-related error encountered: {os_e}")

    except sqlite3.Error as sql_e:
        print(f"Database connection/config error encountered: {sql_e}")
    
    except Exception as e:
        print(f"Unexpected error: {e}")

    finally:
        if conn is None:
            conn.close() # type: ignore
    # try: ...  
# end main


def read_incident_queries(conn):
    inc_query_1 = """
        SELECT ci_type, COUNT(*) AS incident_count
        FROM incidents
        GROUP BY ci_type
        ORDER BY incident_count DESC;
        """
    df1 = pd.read_sql_query(inc_query_1, conn)
    
    inc_query_2 = """
        SELECT ci_type, priority, COUNT(*) AS incident_count
        FROM incidents
        GROUP BY priority, ci_type
        ORDER BY incident_count DESC
        LIMIT 100;
        """
    df2 = pd.read_sql_query(inc_query_2, conn)

    inc_query_3 = """
        SELECT service_component, COUNT(*) AS incident_count
        FROM incidents
        GROUP BY service_component
        ORDER BY incident_count DESC;
        """
    df3 = pd.read_sql_query(inc_query_3, conn)
    
    return {
        "incident_by_ci_type": df1,
        "incident_by_priority": df2,
        "incident_by_service_component": df3
    }
# end read_incident_queries    
        

def read_event_queries(conn):
    ev_query_1 = """
        SELECT AVG(number_of_events) AS avg_events_per_incident
        FROM (
            SELECT incident_id, COUNT(*) AS number_of_events
            FROM incident_activity
            GROUP BY incident_id
        );
    """
    df1 = pd.read_sql_query(ev_query_1, conn)

    ev_query_2 = """
        SELECT strftime('%Y-%W', date_stamp) AS week_label,
            COUNT(*) AS event_count
        FROM incident_activity
        WHERE date_stamp IS NOT NULL
            AND TRIM(date_stamp) <> ''
        GROUP BY week_label
        ORDER BY week_label;
    """    
    df2 = pd.read_sql_query(ev_query_2, conn)
    
    return {
        "avg_events_per_incident": df1,
        "weekly_incident_events": df2,
    }
# end read_event_queries


def read_interaction_queries(conn):
    int_query_1 = """
        SELECT priority, category, ci_type, 
            AVG(julianday(close_time) - julianday(open_time)) AS avg_interaction_duration
        FROM interactions
        WHERE open_time IS NOT NULL AND TRIM(open_time) <> ''
            AND close_time IS NOT NULL AND TRIM(close_time) <> ''
        GROUP BY priority, category, ci_type;
        """
    df1 = pd.read_sql_query(int_query_1, conn)

    int_query_2 = """
        SELECT service_component, COUNT(*) AS interaction_count
        FROM interactions
        GROUP BY service_component
        ORDER BY interaction_count DESC;
        """    
    df2 = pd.read_sql_query(int_query_2, conn)
    
    return {
        "avg_interaction_duration": df1,
        "interactions_by_service": df2,
    }
# end read_interaction_queries


def read_change_queries(conn):
    itc_query_1 = """
        SELECT cab_approval_needed, COUNT(*) as itsm_change_count
        FROM itsm_changes
        GROUP BY cab_approval_needed;
        """
    df1 = pd.read_sql_query(itc_query_1, conn)

    itc_query_2 = """
        SELECT strftime('%Y-%W', actual_start) AS weekly_actual_start,
            COUNT(*) AS change_event_count
        FROM itsm_changes
        WHERE actual_start IS NOT NULL
            AND TRIM(actual_start) <> ''
        GROUP BY weekly_actual_start;
        """
    df2 = pd.read_sql_query(itc_query_2, conn)

    itc_query_3 = """
        SELECT strftime('%Y-%W', planned_start) AS weekly_planned_start,
            COUNT(*) AS change_event_count
        FROM itsm_changes
        WHERE planned_start IS NOT NULL
            AND TRIM(planned_start) <> ''
        GROUP BY weekly_planned_start;
        """
    df3 = pd.read_sql_query(itc_query_3, conn)
    
    return {
        "changes_by_cab_approval": df1,
        "weekly_actual_changes": df2,
        "weekly_planned_changes": df3,
    }
# end read_change_queries


def write_to_excel(kpi_output, path):
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for sheet_name, df in kpi_output.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
# end write_to_excel


if __name__ == "__main__":
    main()












