# TaskFlow

TaskFlow is a task-management application with a frontend interface, FastAPI backend, SQLite database, task search algorithms, project statistics, benchmarking, and a deterministic keyless Quick-Add parser.

---

## Project Structure

```text
TaskFlow/
│
├── backend/
│   ├── __init__.py
│   ├── algorithms.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── styles.css
│
├── algorithms.py
├── check_algorithms.py
├── benchmark.py
├── requirements.txt
├── taskflow.db
├── README.md
└── .gitignore
Tech Stack
Frontend
HTML
CSS
JavaScript
LocalStorage
Backend
Python
FastAPI
Uvicorn
Pydantic
SQLAlchemy
SQLite
Algorithms
Insertion Sort
Linear Search
Binary Search
Architecture
Frontend
   │
   │ HTTP Requests
   ▼
FastAPI Backend
   │
   ├── Pydantic Validation
   │
   ├── SQLAlchemy ORM
   │
   └── SQLite Database
   │
   ▼
Algorithm Layer
   ├── Insertion Sort
   ├── Linear Search
   └── Binary Search
   The backend response is returned to the frontend and rendered in the dashboard.

Backend Flow

The frontend sends HTTP requests to the FastAPI backend.
Frontend
   ↓
HTTP Request
   ↓
FastAPI Backend
   ↓
Pydantic Validation
   ↓
SQLAlchemy ORM
   ↓
SQLite Database
   ↓
Backend Response
   ↓
Frontend Dashboard
The backend response is returned to the frontend and rendered in the dashboard.

Project Features

The core TaskFlow application includes:

Task management
Project management
Create task
Read task
Update task
Delete task
Task search
Sorted tasks
Project statistics
Insertion Sort
Linear Search
Binary Search
Algorithm comparison counting
Benchmarking
Quick-Add task parser
Pydantic validation
SQLAlchemy ORM
SQLite database
Frontend dashboard
API Endpoints
Root Endpoint
GET /
{
  "message": "TaskFlow API is running"
}
Projects
Get Projects
GET /projects
Create Project
POST /projects
Tasks
Get Tasks
GET /tasks
Create Task
POST /tasks

Example request:

{
  "title": "Complete TaskFlow Project",
  "priority": "medium",
  "due_date": "2026-08-20",
  "status": "pending",
  "project_id": 1
}
Get Task
GET /tasks/{task_id}
Update Task
PUT /tasks/{task_id}

Example:

{
  "title": "Updated TaskFlow Project",
  "priority": "high",
  "due_date": "2026-08-25",
  "status": "completed"
}
Delete Task
DELETE /tasks/{task_id}

Successful response:

{
  "message": "Task deleted successfully"
}
Task Search

TaskFlow supports searching tasks using two algorithms.

Linear Search
GET /tasks/search?title=Learn%20Python&algo=linear

Linear Search scans task records from beginning to end until a matching title is found.

Binary Search
GET /tasks/search?title=Learn%20Python&algo=binary

Binary Search works on sorted task records and searches for the matching title.

The search endpoints operate on task records from the real database.

Sorted Tasks

Tasks can be sorted by priority.

GET /tasks?sort=priority

The backend fetches the real task records and uses the project's sorting algorithm.

Project Statistics
GET /projects/statistics

The statistics response contains project information such as:

{
  "project_id": 1,
  "project_name": "TaskFlow Project",
  "task_count": 3,
  "pending_count": 2,
  "in_progress_count": 0,
  "completed_count": 1
}
HTTP Response Codes

The backend returns:

Code	Meaning
200	Successful reads and updates
201	Successful creation
404	Requested resource does not exist
409	Duplicate user email is created
422	Invalid Pydantic request data
Algorithms
Insertion Sort
insertion_sort(records, key)

insertion_sort() sorts records in place using the standard insertion-sort algorithm.

The algorithm starts from the second record, compares it with previous records, and inserts it into the correct position.

Complexity
Case	Complexity
Best Case	O(n)
Worst Case	O(n²)
Auxiliary Space	O(1)
Linear Search
linear_search(records, target_value, key)

Linear Search scans records from beginning to end and returns the matching index or record when the target value is found.

Complexity
Case	Complexity
Best Case	O(1)
Worst Case	O(n)
Auxiliary Space	O(1)
Binary Search
binary_search(sorted_records, target_value, key)

Binary Search searches a sorted list by repeatedly reducing the search range.

It returns the matching index or -1 when the value is not found.

Complexity
Time: O(log n)
Space: O(1)
Algorithm Comparison Counting

The project tracks the number of comparisons performed by the algorithms.

Example:

Linear Search:
Index: 1
Comparison count: 2


Binary Search:
Index: 1

The comparison count can be used to compare the behavior of the different search algorithms.

Algorithm Testing

The project includes:

check_algorithms.py

The automated checks cover:

Empty-list Insertion Sort
Single-element Insertion Sort
Binary Search of the first index
Binary Search of the middle index
Binary Search of the last index
Binary Search not-found case
Insertion Sort comparison counting
Binary Search comparison counting
Linear Search comparison counting

Run:

python3 check_algorithms.py
Benchmarking

The project includes:

benchmark.py

The benchmark measures algorithm performance for different input sizes.

The benchmark includes measurements for:

500   Insertion Sort
500   Linear Search
500   Binary Search


5000  Insertion Sort
5000  Linear Search
5000  Binary Search


50000 Insertion Sort
50000 Linear Search
50000 Binary Search

The measured values are used to compare algorithm performance.

Quick-Add

TaskFlow includes a deterministic, keyless Quick-Add parser.

The parser does not require:

API key
Network connection
Paid service
Quick-Add Endpoint

The endpoint accepts:

{
  "description": "<free text>",
  "project_id": 1
}

The parser determines:

title
priority
due-date hint
priority rules
Priority Rules

The lower-cased description is checked in this order:

urgent or asap → high


whenever or low priority → low


otherwise → medium

Therefore, the parser uses deterministic rules to determine the task priority.

Quick-Add Processing
Quick-Add Request
       ↓
parse_task_description()
       ↓
Determine title
       ↓
Determine priority
       ↓
Determine due-date hint
       ↓
Check project
       ↓
Create Task
       ↓
Save to Database
       ↓
Return Task

If the requested project does not exist, the backend returns a validation error.

Quick-Add Examples
Example 1

Input:

Call mom tomorrow

Expected parsed result:

{
  "title": "Call mom",
  "due_date_hint": "tomorrow"
}
Example 2

Input:

Review documentation whenever

Expected parsed result:

{
  "title": "Review documentation",
  "priority": "low"
}
Database

TaskFlow uses SQLite as its database.

Database file:

taskflow.db

SQLAlchemy is used as the ORM layer.

The main database-related files are:

backend/database.py
backend/models.py
backend/schemas.py
Pydantic Validation

Pydantic is used for request and response validation.

Invalid request data results in:

422 Unprocessable Entity

The API documentation also exposes validation schemas and HTTPValidationError.

Frontend

The frontend is located inside:

frontend/

Files:

index.html
script.js
styles.css

The frontend provides:

Task creation form
Task list
Refresh tasks
Search
Task status display
Priority display
Due date display
Project information
Success/error messages
LocalStorage

The frontend also contains LocalStorage functionality.

Tasks can be saved using:

localStorage.setItem(
  "taskflow_tasks",
  JSON.stringify(tasks)
);

Tasks can be loaded using:

localStorage.getItem("taskflow_tasks");

If stored data cannot be parsed, the frontend falls back to an empty list.

Running the Backend

Activate the virtual environment:

source .venv/bin/activate

Start the FastAPI application:

uvicorn backend.main:app --reload

The backend runs on:

http://127.0.0.1:8000

FastAPI documentation:

http://127.0.0.1:8000/docs
Running the Frontend

Open the frontend directory:

cd frontend

Start the local HTTP server:

python3 -m http.server 5500

The frontend runs on:

http://127.0.0.1:5500/
API Documentation

FastAPI automatically provides interactive API documentation.

Open:

http://127.0.0.1:8000/docs

The documentation can be used to test:

Projects
Tasks
Task updates
Task deletion
Task search
Project statistics
Quick-Add functionality
Example API Flow

Create a task:

POST /tasks

Then retrieve it:

GET /tasks/1

Update it:

PUT /tasks/1

Search tasks:

GET /tasks/search?title=Learn%20Python&algo=linear

Or:

GET /tasks/search?title=Learn%20Python&algo=binary

Finally, delete the task:

DELETE /tasks/1
Project Status

TaskFlow includes a working frontend and backend flow with:

FastAPI API
SQLite database
SQLAlchemy ORM
Pydantic validation
CRUD operations
Search algorithms
Sorting algorithm
Comparison counting
Benchmarking
Project statistics
Quick-Add parser
Interactive API documentation
Conclusion

TaskFlow combines a task-management application with algorithmic problem solving.

The project demonstrates:

Backend API development
Database integration
Request validation
CRUD operations
Sorting
Searching
Algorithm complexity
Comparison counting
Benchmarking
Deterministic text parsing
Frontend and backend integration