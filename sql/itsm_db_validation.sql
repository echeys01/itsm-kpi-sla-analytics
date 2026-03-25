-- database: C:\AnalyticsProjects\ITAnalysisProjects\P2-ServiceDeskKPIAnalysis\output\itsm_bpi2014.db
-- Queries performed to assess DB readiness for KPI analysis.
PRAGMA database_list;
-- Basic row counts for each table.
SELECT COUNT(*) AS total_incidents FROM incidents;
SELECT COUNT(*) AS total_interactions FROM interactions;
SELECT COUNT(*) AS incident_activity_events FROM incident_activity;
SELECT COUNT(*) AS total_changes FROM itsm_changes;

-- Null rates for fields valuable to KPIs.
-- For 'incidents.'
SELECT 
    (COUNT(*) - COUNT(NULLIF(TRIM(incident_id), ''))) * 100.0 / COUNT(*) AS incidents_null_rate,
    (COUNT(*) - COUNT(NULLIF(TRIM(priority), ''))) * 100.0 / COUNT(*) AS priority_null_rate,
    (COUNT(*) - COUNT(NULLIF(TRIM(service_component), ''))) * 100.0 / COUNT(*) AS serv_comp_null_rate,
    (COUNT(*) - COUNT(NULLIF(TRIM(ci_name), ''))) * 100.0 / COUNT(*) AS ci_name_null_rate,
    (COUNT(*) - COUNT(NULLIF(TRIM(ci_type), ''))) * 100.0 / COUNT(*) AS ci_type_null_rate
FROM incidents;

-- For 'interactions.'
SELECT 
    (COUNT(*) - COUNT(NULLIF(TRIM(interaction_id), ''))) * 100.0 / COUNT(*) AS missing_interaction_id,
    (COUNT(*) - COUNT(NULLIF(TRIM(open_time), ''))) * 100.0 / COUNT(*) AS missing_open_times,
    (COUNT(*) - COUNT(NULLIF(TRIM(close_time), ''))) * 100.0 / COUNT(*) AS missing_close_times,
    (COUNT(*) - COUNT(NULLIF(TRIM(status), ''))) * 100.0 / COUNT(*) AS missing_interaction_status,
    (COUNT(*) - COUNT(NULLIF(TRIM(priority), ''))) * 100.0 / COUNT(*) AS null_priority,
    (COUNT(*) - COUNT(NULLIF(TRIM(category), ''))) * 100.0 / COUNT(*) AS null_categories,
    (COUNT(*) - COUNT(NULLIF(TRIM(service_component), ''))) * 100.0 / COUNT(*) AS missing_serv_comps
FROM interactions;

-- For 'incident_activity.'
SELECT 
    (COUNT(*) - COUNT(NULLIF(TRIM(incident_id), ''))) * 100.0 / COUNT(*) AS incidents_null_rate,
    (COUNT(*) - COUNT(NULLIF(TRIM(incident_activity_number), ''))) * 100.0 / COUNT(*) AS activity_no_null_rate,
    (COUNT(*) - COUNT(NULLIF(TRIM(incident_activity_type), ''))) * 100.0 / COUNT(*) AS activity_type_null_rate,
    (COUNT(*) - COUNT(NULLIF(TRIM(date_stamp), ''))) * 100.0 / COUNT(*) AS missing_date_stamps,
    (COUNT(*) - COUNT(NULLIF(TRIM(assignment_group), ''))) * 100.0 / COUNT(*) AS assign_group_null_rate,
    (COUNT(*) - COUNT(NULLIF(TRIM(interaction_id), ''))) * 100.0 / COUNT(*) AS missing_interaction_id
FROM incident_activity;

-- For 'itsm_changes.'
SELECT 
    (COUNT(*) - COUNT(NULLIF(TRIM(change_id), ''))) * 100.0 / COUNT(*) AS missing_change_id,
    (COUNT(*) - COUNT(NULLIF(TRIM(planned_start), ''))) * 100.0 / COUNT(*) AS null_planned_start,
    (COUNT(*) - COUNT(NULLIF(TRIM(planned_end), ''))) * 100.0 / COUNT(*) AS null_planned_end,
    (COUNT(*) - COUNT(NULLIF(TRIM(actual_start), ''))) * 100.0 / COUNT(*) AS null_actual_start,
    (COUNT(*) - COUNT(NULLIF(TRIM(actual_end), ''))) * 100.0 / COUNT(*) AS null_actual_end,
    (COUNT(*) - COUNT(NULLIF(TRIM(cab_approval_needed), ''))) * 100.0 / COUNT(*) AS null_cab_approval,
    (COUNT(*) - COUNT(NULLIF(TRIM(service_component), ''))) * 100.0 / COUNT(*) AS missing_serv_comps
FROM itsm_changes;

-- Additional validation queries meant to assess current state of database.
SELECT DISTINCT priority 
FROM incidents
ORDER BY priority;

-- Assess ITSM changes by CAB approval.
SELECT cab_approval_needed, COUNT(*) as itsm_change_count
FROM itsm_changes
GROUP BY cab_approval_needed;

-- Assess amount of activity per incident.
SELECT 
    COUNT(*) AS incident_activity_count,
    COUNT(DISTINCT incident_id) AS incident_count
FROM incident_activity;

-- Assess volume of events by event type.
SELECT incident_activity_type, COUNT(*) AS incident_activity_count
FROM incident_activity
GROUP BY incident_activity_type
ORDER BY incident_activity_count DESC;

-- Open, close times associated with a particular ci_type.
SELECT 
    MIN(open_time) AS min_open_time, MAX(open_time) AS max_open_time 
FROM interactions
GROUP BY ci_type;





