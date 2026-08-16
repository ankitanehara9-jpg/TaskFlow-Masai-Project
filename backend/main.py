import re
import time

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Project, Task, User
from .algorithms import insertion_sort, linear_search, binary_search
from .schemas import (
    ProjectCreate,
    ProjectResponse,
    TaskCreate,
    TaskResponse,
    TaskUpdate,
    UserCreate,
    UserResponse,
    QuickAddRequest,
)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API")


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type"],
)


# ============================================================
# REQUEST TIMING MIDDLEWARE
# ============================================================

@app.middleware("http")
async def request_logger(request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    print(
        f"{request.method} {request.url.path} "
        f"- {elapsed_ms:.2f} ms"
    )

    return response


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {"message": "TaskFlow API is running"}


# ============================================================
# USERS
# ============================================================

@app.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )

    new_user = User(email=user.email)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get(
    "/users",
    response_model=list[UserResponse],
)
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# ============================================================
# PROJECTS
# ============================================================

@app.post(
    "/projects",
    response_model=ProjectResponse,
    status_code=201,
)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
):
    owner = (
        db.query(User)
        .filter(User.id == project.owner_id)
        .first()
    )

    if owner is None:
        raise HTTPException(
            status_code=404,
            detail="Owner user not found",
        )

    new_project = Project(
        name=project.name,
        owner_id=project.owner_id,
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@app.get(
    "/projects",
    response_model=list[ProjectResponse],
)
def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()


# ============================================================
# TASKS - CREATE
# ============================================================

@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=201,
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(Project.id == task.project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    new_task = Task(
        title=task.title,
        priority=task.priority,
        due_date=task.due_date,
        status=task.status,
        project_id=task.project_id,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# ============================================================
# TASKS - LIST + INSERTION SORT
# ============================================================

@app.get(
    "/tasks",
    response_model=list[TaskResponse],
)
def get_tasks(
    sort: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    tasks = db.query(Task).all()

    if sort == "priority":
        priority_rank = {
            "low": 1,
            "medium": 2,
            "high": 3,
        }

        records = [
            {
                "id": task.id,
                "title": task.title,
                "priority": task.priority,
                "due_date": task.due_date,
                "status": task.status,
                "project_id": task.project_id,
            }
            for task in tasks
        ]

        insertion_sort(
            records,
            key=lambda record: priority_rank[record["priority"]],
        )

        return records

    return tasks


# ============================================================
# TASKS - SEARCH
# ============================================================

@app.get("/tasks/search")
def search_tasks(
    title: str,
    algo: str = Query(default="binary"),
    db: Session = Depends(get_db),
):
    tasks = db.query(Task).all()

    if not tasks:
        raise HTTPException(
            status_code=404,
            detail="No tasks found",
        )

    target = title.lower()

    if algo == "linear":
        index = linear_search(
            tasks,
            target,
            key=lambda task: task.title.lower(),
        )

    elif algo == "binary":
        sorted_tasks = tasks.copy()

        insertion_sort(
            sorted_tasks,
            key=lambda task: task.title.lower(),
        )

        index = binary_search(
            sorted_tasks,
            target,
            key=lambda task: task.title.lower(),
        )

        if index != -1:
            return sorted_tasks[index]

        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    else:
        raise HTTPException(
            status_code=422,
            detail="algo must be 'binary' or 'linear'",
        )

    if index == -1:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return tasks[index]


# ============================================================
# TASKS - GET BY ID
# ============================================================

@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task


# ============================================================
# TASKS - UPDATE
# ============================================================

@app.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    update_data = task_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


# ============================================================
# TASKS - DELETE
# ============================================================

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully",
        "task_id": task_id,
    }


# ============================================================
# PROJECT STATISTICS
# ============================================================

@app.get("/projects/statistics")
def project_statistics(
    db: Session = Depends(get_db),
):
    results = (
        db.query(
            Project.id.label("project_id"),
            Project.name.label("project_name"),
            func.count(Task.id).label("task_count"),
            func.coalesce(
                func.sum(
                    case(
                        (Task.status == "pending", 1),
                        else_=0,
                    )
                ),
                0,
            ).label("pending_count"),
            func.coalesce(
                func.sum(
                    case(
                        (Task.status == "in_progress", 1),
                        else_=0,
                    )
                ),
                0,
            ).label("in_progress_count"),
            func.coalesce(
                func.sum(
                    case(
                        (Task.status == "completed", 1),
                        else_=0,
                    )
                ),
                0,
            ).label("completed_count"),
        )
        .outerjoin(Task, Project.id == Task.project_id)
        .group_by(Project.id, Project.name)
        .all()
    )

    return [
        {
            "project_id": row.project_id,
            "project_name": row.project_name,
            "task_count": row.task_count,
            "pending_count": row.pending_count,
            "in_progress_count": row.in_progress_count,
            "completed_count": row.completed_count,
        }
        for row in results
    ]


# ============================================================
# AI QUICK-ADD MOCK PARSER
# ============================================================

def parse_task_description(description: str):
    working_text = description.lower()

    # Priority
    if "urgent" in working_text or "asap" in working_text:
        priority = "high"
    elif "whenever" in working_text or "low priority" in working_text:
        priority = "low"
    else:
        priority = "medium"

    # Due-date phrases
    date_phrases = [
        "today",
        "tomorrow",
        "next week",
        "next monday",
        "next tuesday",
        "next wednesday",
        "next thursday",
        "next friday",
        "next saturday",
        "next sunday",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]

    due_date_hint = None

    for phrase in date_phrases:
        if phrase in working_text:
            due_date_hint = phrase
            break

    # Remove all priority keywords
    title = description

    priority_keywords = [
        "urgent",
        "asap",
        "whenever",
        "low priority",
    ]

    for keyword in priority_keywords:
        title = re.sub(
            re.escape(keyword),
            "",
            title,
            flags=re.IGNORECASE,
        )

    # Remove all occurrences of selected date phrase
    if due_date_hint:
        title = re.sub(
            re.escape(due_date_hint),
            "",
            title,
            flags=re.IGNORECASE,
        )

    title = title.strip()

    if not title:
        title = "Untitled task"

    return {
        "title": title,
        "priority": priority,
        "due_date_hint": due_date_hint,
    }


# ============================================================
# AI QUICK-ADD
# ============================================================

@app.post(
    "/tasks/quick-add",
    response_model=TaskResponse,
    status_code=201,
)
def quick_add_task(
    request: QuickAddRequest,
    db: Session = Depends(get_db),
):
    system_message = (
        "Parse the task description into title, priority, "
        "and due_date_hint using the TaskFlow deterministic rules."
    )

    user_message = request.description

    messages = [
        {
            "role": "system",
            "content": system_message,
        },
        {
            "role": "user",
            "content": user_message,
        },
    ]

    # Required keyless mock parser.
    parsed = parse_task_description(request.description)

    project = (
        db.query(Project)
        .filter(Project.id == request.project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=422,
            detail="Project does not exist",
        )

    task_data = TaskCreate(
        title=parsed["title"],
        priority=parsed["priority"],
        due_date=parsed["due_date_hint"],
        status="pending",
        project_id=request.project_id,
    )

    new_task = Task(
        title=task_data.title,
        priority=task_data.priority,
        due_date=task_data.due_date,
        status=task_data.status,
        project_id=task_data.project_id,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task