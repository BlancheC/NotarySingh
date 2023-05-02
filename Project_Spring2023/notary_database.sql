Use notary_database;

-- A list of users combined with their form data
SELECT u.id as user_id, u.first_name, u.last_name, u.email, fd.addr, fd.city, fd.st, fd.zipcode, fd.document_type, fd.uploaded_file
FROM user u
LEFT JOIN form_data fd ON u.id = fd.user_id;

-- Add a status column
ALTER TABLE user_document ADD status VARCHAR(50) NOT NULL DEFAULT 'pending';
ALTER TABLE notary_document ADD status VARCHAR(50) NOT NULL DEFAULT 'pending';

-- Update status once the document has been notarized
UPDATE user_document SET status = 'notarized' WHERE document_id = 1;
UPDATE notary_document SET status = 'notarized' WHERE document_id = 1;
SELECT u.id as user_id, u.first_name, u.last_name, d.document_id, d.status
FROM user u
JOIN user_document d ON u.id = d.id;

-- Count the amount of documents that were notarized versus pending.
-- Calculate the percentage notarized
WITH document_status_count AS (
    SELECT
        COUNT(CASE WHEN status = 'notarized' THEN 1 END) as notarized_count,
        COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_count
    FROM user_document
)
SELECT
    notarized_count,
    pending_count,
    notarized_count * 100.0 / (notarized_count + pending_count) as notarized_percentage
FROM document_status_count;

-- A list of users along with the number of documents they submited
SELECT
    u.id as user_id,
    u.first_name,
    u.last_name,
    u.email,
    COUNT(ud.document_id) as document_count
FROM user u
LEFT JOIN user_document ud ON u.id = ud.user_id
GROUP BY u.id, u.first_name, u.last_name, u.email;

-- a list of document types along with the number of documents for each type
SELECT
    fd.document_type,
    COUNT(fd.document_type) as document_count
FROM form_data fd
GROUP BY fd.document_type;

