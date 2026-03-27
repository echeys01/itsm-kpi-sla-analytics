-- Queries prepared for XLSX export.

-- Incident KPIs: These measure incident volume, incident types, open rates, and activity events per incident.
-- Incident count by configuration item type (in descending order).
SELECT ci_type, COUNT(*) AS incident_count
FROM incidents
GROUP BY ci_type
ORDER BY incident_count DESC;

-- Incident count by configuration type and priority.
SELECT ci_type, priority, COUNT(*) AS incident_count
FROM incidents
GROUP BY priority, ci_type
ORDER BY incident_count DESC
LIMIT 100;

-- Find average number of activity events per incident.
SELECT AVG(number_of_events) AS avg_events_per_incident
FROM (
    SELECT incident_id, COUNT(*) AS number_of_events
    FROM incident_activity
    GROUP BY incident_id
);

-- Group ITSM changes by CAB approval.
SELECT cab_approval_needed, COUNT(*) as itsm_change_count
FROM itsm_changes
GROUP BY cab_approval_needed;

-- Trend queries
-- Average interaction time (in days) aggregated by priority, category, and ci_type.
-- Assumes ISO format.
SELECT priority, category, ci_type, 
    AVG(julianday(close_time) - julianday(open_time)) AS avg_interaction_duration
FROM interactions
WHERE open_time IS NOT NULL AND TRIM(open_time) <> ''
    AND close_time IS NOT NULL AND TRIM(close_time) <> ''
GROUP BY priority, category, ci_type;

-- Top service components by incident counts.
SELECT service_component, COUNT(*) AS incident_count
FROM incidents
GROUP BY service_component
ORDER BY incident_count DESC;

-- Highest count of interactions by service component.
SELECT service_component, COUNT(*) AS interaction_count
FROM interactions
GROUP BY service_component
ORDER BY interaction_count DESC;

-- Verify original date stamp format (DD-MM-YYYY).
SELECT date_stamp 
FROM incident_activity
LIMIT 20;

-- Standard queries for incident time stamps.
SELECT strftime('%Y-%W', date_stamp) AS week_label,
    COUNT(*) AS event_count
FROM incident_activity
WHERE date_stamp IS NOT NULL
    AND TRIM(date_stamp) <> ''
GROUP BY week_label;

-- Query itsm_changes, compare actual/planned starts.
SELECT strftime('%Y-%W', actual_start) AS weekly_actual_start,
    COUNT(*) AS change_event_count
FROM itsm_changes
WHERE actual_start IS NOT NULL
    AND TRIM(actual_start) <> ''
GROUP BY weekly_actual_start;

SELECT strftime('%Y-%W', planned_start) AS weekly_planned_start,
    COUNT(*) AS change_event_count
FROM itsm_changes
WHERE planned_start IS NOT NULL
    AND TRIM(planned_start) <> ''
GROUP BY weekly_planned_start;

