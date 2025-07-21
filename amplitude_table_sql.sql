-- Session Table
SELECT DISTINCT
    "session_id" AS session_id,
    "user_id" AS user_id,
    MD5(CONCAT("os_version", "device_family", "device_type")) AS device_id,
    HASH("ip_address") AS location_id
FROM amplitude_events
;

-- Location Table
SELECT DISTINCT
    HASH("ip_address") AS location_id,
    "ip_address" AS ip_address,
    "session_id" AS session_id,
    HASH("city") AS city_id,
    HASH("region") AS region_id,
    HASH("country") AS country_id
FROM amplitude_events
;