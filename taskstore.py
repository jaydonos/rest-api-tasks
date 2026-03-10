import json
from dataclasses import dataclass, asdict
from datetime import datetime
from db import get_connection
from errors import NotFoundError


@dataclass
class Task:
    id: int
    text: str
    tags: list[str]
    due: datetime

    #Converts task object inot a plain dictionary
    def to_dict(self):
        data = asdict(self)
        data["due"] = self.due.isoformat() #converts due to iso string so json can read it "2026-03-07"
        return data


class TaskStore:
    def create_task(self, text: str, tags: list[str], due: datetime) -> int:
        tags_json = json.dumps(tags) #Convert list into json string
        with get_connection() as conn:
            cur = conn.execute("""
                                INSERT INTO TASKS (text, tags, due)
                               VALUES (?, ?, ?)
                               """, (text, tags_json, due))
            
            return cur.lastrowid #id of new task 

    def get_task(self, task_id: int) -> Task:
        with get_connection() as conn:
            row = conn.execute("""
                            SELECT * from tasks
                             where id = ?
                             """, (task_id,)).fetchone() #Gets one result or none
        if row is None:
            raise NotFoundError("Task not found")
        
        return self.row_to_task(row)
    
    def get_all_tasks(self) -> list[Task]:
        with get_connection() as conn:
            rows= conn.execute("Select * from tasks order by id").fetchall()
        
        all_tasks = []
        for row in rows:
            all_tasks.append(self.row_to_task(row))
        return all_tasks

    def delete_task(self, task_id: int) -> None:
        with get_connection() as conn:
            cur = conn.execute("DELETE from tasks where id = ?",(task_id,))
        
        if cur.rowcount == 0:
            raise NotFoundError("Task not found")
    
    def update_task(self, task_id: int, text: str, tags: list[str], due: datetime):
        tags_json = json.dumps(tags)

        with get_connection() as conn:
            cur = conn.execute(
                """
                UPDATE tasks
                SET text = ?, tags = ?, due = ?
                WHERE id = ?
                """,
                (text, tags_json, due, task_id)
            )
        if cur.rowcount == 0:
            raise NotFoundError("Task not found")

    #Gets all tasks with the same tag
    def get_tasks_by_tag(self, tag: str) -> list[Task]:
        with get_connection() as conn:
            rows = conn.execute("Select * from tasks order by id"
                                ).fetchall()
            
        all_tasks = []
        for row in rows:
            all_tasks.append(self.row_to_task(row))
        
        tagged_tasks = []
        for task in all_tasks:
            if tag in task.tags:
                tagged_tasks.append(task)
        return tagged_tasks

    def get_tasks_by_due_date(self, year: int, month: int, day: int) -> list[Task]:
        with get_connection() as conn:
            rows = conn.execute("Select * from tasks order by id"
                                ).fetchall()
        all_tasks = []
        for row in rows:
            all_tasks.append(self.row_to_task(row))
        
        date_tasks = []
        for task in all_tasks:
            if task.due.year == year and task.due.month == month and task.due.day == day:
                date_tasks.append(task)

        return date_tasks
    

    #Convert DB row into a Task
    def row_to_task(self, row):
        return Task(
            id=row["id"],
            text=row["text"],
            tags=json.loads(row["tags"]),
            due=datetime.fromisoformat(row["due"])
        )