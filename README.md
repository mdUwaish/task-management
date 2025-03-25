Task Management API

🚀 Project Overview
The Task Management API is built using Django and Django REST Framework (DRF) to allow managers and admins to create and assign tasks, while employees can update the task status.

📌 Features
- Admin & Manager: Create, assign, and modify tasks.
- Employees: View assigned tasks and update task status.
- Role-based permissions.
- Token-based authentication.


⚙️ Setup Instructions

1️⃣ Clone the Repository
```bash
git clone https://github.com/mdUwaish/task-management
cd task-management
```

2️⃣ Create a Virtual Environment & Activate
```bash
python -m venv venv  # Create virtual environment
source venv/bin/activate  # Activate (Mac/Linux)
venv\Scripts\activate  # Activate (Windows)
```

3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

4️⃣ Apply Migrations & Create Superuser
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Follow prompts
```

5️⃣ Run the Development Server
```bash
python manage.py runserver
```


🔑 Authentication
- The API uses JWT authentication.
- Obtain a token using the login API and pass it in the `Authorization` header as `Bearer <token>`.

Login API (to get token)
Request:
```http
POST /api/token/
```

Body:
```json
{
    "email": "admin@example.com",
    "password": "password123"
}
```

Response:
```json
{
    "access": "your-access-token",
    "refresh": "your-refresh-token"
}
```

---
📡 API Endpoints

1️⃣ Create Task (Admin & Manager Only)
Endpoint: `POST /api/tasks/`
```json
{
    "name": "Fix Database Issue",
    "description": "Resolve connection issues in PostgreSQL",
    "task_type": "Bug Fix",
    "status": "Pending",
    "assigned_users": ["employee1@example.com", "employee2@example.com"]
}
```
Response:
```json
{
    "id": 1,
    "name": "Fix Database Issue",
    "description": "Resolve connection issues in PostgreSQL",
    "task_type": "Bug Fix",
    "status": "Pending",
    "assigned_users": ["employee1@example.com", "employee2@example.com"]
}
```

2️⃣ Assign Task to Users (Admin & Manager Only)
Endpoint: `POST /api/tasks/{task_id}/assign/`
```json
{
    "assigned_users": ["employee3@example.com"]
}
```
Response:
```json
{
    "message": "Task assigned successfully"
}
```

3️⃣ Get Assigned Tasks (Employee & Manager/Admin)
Endpoint: `GET /api/tasks/`
Response:
```json
[
    {
        "id": 1,
        "name": "Fix Database Issue",
        "status": "Pending",
        "assigned_users": ["employee1@example.com"]
    }
]
```

4️⃣ Update Task Status (Employee Assigned, Admin & Manager)
Endpoint: `PATCH /api/tasks/{task_id}/status/`
```json
{
    "status": "In Progress"
}
```
Response:
```json
{
    "message": "Task status updated successfully",
    "task": {
        "id": 1,
        "name": "Fix Database Issue",
        "status": "In Progress"
    }
}
```

---
🔑 Test Credentials
| Role | Email | Password |
|-----------|----------|-------------|
| Admin | admin@example.com | password123 |
| Manager | manager@example.com | password123 |
| Employee | employee@example.com | password123 |

---
📌 Notes
- Ensure the Admin & Manager create tasks.
- Employees can only update the `status` of assigned tasks.
- Use JWT authentication for all protected routes.

---
🚀 Next Steps
- Add unit tests for API endpoints.
- Implement notifications for task updates.
- Improve frontend integration.

---
👨‍💻 Author
Md Uwaish
- LinkedIn: https://www.linkedin.com/in/md-uwaish-82a81a221/
- GitHub: https://github.com/mdUwaish

