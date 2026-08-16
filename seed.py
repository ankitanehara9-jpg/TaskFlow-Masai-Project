from backend.database import SessionLocal
from backend.models import Project, Task, User


db = SessionLocal()

try:
    user = db.query(User).first()

    if not user:
        user = User(email="demo@taskflow.com")
        db.add(user)
        db.commit()
        db.refresh(user)

    project = db.query(Project).first()

    if not project:
        project = Project(
            name="TaskFlow Project",
            owner_id=user.id
        )
        db.add(project)
        db.commit()
        db.refresh(project)

    tasks = [
        Task(
            title="Learn Python",
            priority="high",
            status="pending",
            project_id=project.id
        ),
        Task(
            title="Practice Algorithms",
            priority="medium",
            status="pending",
            project_id=project.id
        ),
        Task(
            title="Complete TaskFlow",
            priority="low",
            status="completed",
            project_id=project.id
        )
    ]

    for task in tasks:
        db.add(task)

    db.commit()

    print("Seed data inserted successfully!")

finally:
    db.close()