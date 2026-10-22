Based on your handwritten notes, I have transcribed the schema into markdown tables. I have standardized the data types (e.g., using `ID`, `String`, `Text`, `DateTime`, `Integer`, `Boolean`) and identified references based on the naming conventions and the explicit "FOREIGN KEY" notes in your drawing.

### Issues

| name | type | is_reference |
| :--- | :--- | :--- |
| id | ID | False |
| key | String | False |
| assignee_id | ID | True |
| created | DateTime | False |
| creator_id | ID | True |
| description | Text | False |
| duedate | DateTime | False |
| issuetype | String | True |
| priority | String | True |
| project_id | ID | True |
| reporter_id | ID | True |
| resolution_date | DateTime | False |
| resolution_description | Text | False |
| resolution_name | String | False |
| status | String | False |
| summary | Text | False |
| votes | Integer | False |
| watcher_count | Integer | False |
| updated | DateTime | False |

### Person

| name | type | is_reference |
| :--- | :--- | :--- |
| displayname | String | False |
| email | String | False |
| id | ID | False |

### Project

| name | type | is_reference |
| :--- | :--- | :--- |
| id | ID | False |
| key | String | False |
| name | String | False |
| type_key | String | True |

### Projects

| name | type | is_reference |
| :--- | :--- | :--- |
| id | ID | False |
| key | String | False |
| archived | Boolean | False |
| assignee_type | String | False |
| description | Text | False |
| lead_display_name | String | False |
| lead_key | ID | True |
| lead_name | String | False |
| name | String | False |
| project_type_key | String | True |

### IssueLinks

| name | type | is_reference |
| :--- | :--- | :--- |
| id | ID | False |
| issue_id | ID | True |
| issue_key | String | True |
| inward | String | False |
| outward | String | False |
| issue_id_ref | ID | True |
| issue_key_ref | String | True |
| issue_priority | String | True |
| issue_status | String | False |
| issue_status_description | Text | False |
| issue_summary | Text | False |
| issue_type | String | False |

### Subtasks

| name | type | is_reference |
| :--- | :--- | :--- |
| id | ID | False |
| issue_id | ID | True |
| issue_key | String | True |
| key | String | False |
| priority | String | True |
| status | String | False |
| status_description | Text | False |
| summary | Text | False |

### Labels

| name | type | is_reference |
| :--- | :--- | :--- |
| issue_id | ID | True |
| issue_key | String | True |
| value | String | False |

### Attachment

| name | type | is_reference |
| :--- | :--- | :--- |
| id | ID | False |
| issue_id | ID | True |
| issue_key | String | True |
| author_id | ID | True |
| created_at | DateTime | False |
| file_name | String | False |
| file_size_bytes | Integer | False |
| local_path | String | False |
| mime_type | String | False |

### Web_links

| name | type | is_reference |
| :--- | :--- | :--- |
| id | ID | False |
| issue_id | ID | True |
| issue_key | String | True |
| application | String | False |
| relationship | String | False |
| title | String | False |
| url | String | False |

### Comment

| name | type | is_reference |
| :--- | :--- | :--- |
| id | ID | False |
| issue_id | ID | True |
| issue_key | String | True |
| author_id | ID | True |
| body | Text | False |
| created_at | DateTime | False |
| updated_at | DateTime | False |
| updated_author_id | ID | True |

### Changelog

| name | type | is_reference |
| :--- | :--- | :--- |
| id | ID | False |
| issue_id | ID | True |
| issue_key | String | True |
| author_id | ID | True |
| created_at | DateTime | False |
| field | String | False |
| field_type | String | False |
| from | String | False |
| from_string | String | False |
| to | String | False |
| to_string | String | False |

### Project_issue_types

| name | type | is_reference |
| :--- | :--- | :--- |
| id | ID | False |
| project_id | ID | True |
| project_key | String | True |
| description | Text | False |
| name | String | False |
| subtask | Boolean | False |

### Project_roles

| name | type | is_reference |
| :--- | :--- | :--- |
| project_id | ID | True |
| project_key | String | True |
| name | String | False |