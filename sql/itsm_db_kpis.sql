-- database: C:\AnalyticsProjects\ITAnalysisProjects\P2-ServiceDeskKPIAnalysis\output\itsm_bpi2014.db
-- Main query file for assessing predetermined ITSM KPIs.

-- Incident KPIs: These measure incident volume, incident types, open rates, and activity events per incident.
SELECT DISTINCT priority 
FROM incidents
ORDER BY priority;

-- Incident count by configuration item type (in descending order).
SELECT ci_type, COUNT(*) AS incident_count
FROM incidents
GROUP BY ci_type
ORDER BY incident_count DESC;

--Incident count by configuration type and priority.
SELECT ci_type, priority, COUNT(*) AS incident_count
FROM incidents
GROUP BY priority, ci_type
ORDER BY incident_count DESC;

-- Find average number of activity events per incident.
SELECT AVG(number_of_incidents) AS avg_events_per_incident
FROM (
    SELECT incident_id, COUNT(*) AS number_of incidents
    FROM incident_activity
    GROUP BY incident_id
);

-- Assess ITSM changes by CAB approval.
SELECT cab_approval_needed, COUNT(*) as itsm_change_count
FROM itsm_changes
GROUP BY cab_approval_needed


