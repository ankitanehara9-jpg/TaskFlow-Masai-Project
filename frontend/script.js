const API_URL = "http://127.0.0.1:8000";

const taskForm = document.getElementById("taskForm");
const taskList = document.getElementById("taskList");
const titleError = document.getElementById("titleError");
const message = document.getElementById("message");
const refreshButton = document.getElementById("refreshButton");


// ============================================================
// LOCAL STORAGE
// ============================================================

function saveTasksToLocalStorage(tasks) {
    localStorage.setItem(
        "taskflow_tasks",
        JSON.stringify(tasks)
    );
}


function loadTasksFromLocalStorage() {
    const savedTasks =
        localStorage.getItem("taskflow_tasks");

    if (!savedTasks) {
        return [];
    }

    try {
        return JSON.parse(savedTasks);
    } catch (error) {
        console.error(
            "Unable to read localStorage:",
            error
        );

        return [];
    }
}


// ============================================================
// MESSAGE
// ============================================================

function showMessage(text, isError = false) {
    if (!message) {
        alert(text);
        return;
    }

    message.textContent = text;

    message.className = isError
        ? "error-message"
        : "success-message";
}


// ============================================================
// CREATE TASK
// ============================================================

async function createTask(event) {
    event.preventDefault();

    titleError.textContent = "";
    message.textContent = "";

    const title =
        document.getElementById("title").value.trim();

    const priority =
        document.getElementById("priority").value;

    const due_date =
        document.getElementById("due_date").value;

    const status =
        document.getElementById("status").value;

    const project_id =
        Number(
            document.getElementById("project_id").value
        );


    // Title validation
    if (!title) {
        titleError.textContent =
            "Task title is required.";

        return;
    }


    // Due date validation
    if (!due_date) {
        showMessage(
            "Please select a due date.",
            true
        );

        return;
    }


    // Project validation
    if (!project_id || project_id < 1) {
        showMessage(
            "Please enter a valid Project ID.",
            true
        );

        return;
    }


    try {
        const response = await fetch(
            `${API_URL}/tasks`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    title: title,
                    priority: priority,
                    due_date: due_date,
                    status: status,
                    project_id: project_id
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {
            showMessage(
                data.detail ||
                "Unable to create task.",
                true
            );

            return;
        }


        showMessage(
            "Task created successfully!"
        );


        taskForm.reset();


        document.getElementById(
            "priority"
        ).value = "medium";


        document.getElementById(
            "status"
        ).value = "pending";


        document.getElementById(
            "project_id"
        ).value = "1";


        await loadTasks();

    } catch (error) {
        console.error(error);

        showMessage(
            "Backend is not running. Please start the FastAPI server.",
            true
        );
    }
}


// ============================================================
// LOAD TASKS
// ============================================================

async function loadTasks() {
    try {
        const response = await fetch(
            `${API_URL}/tasks`
        );


        if (!response.ok) {
            throw new Error(
                "Failed to load tasks"
            );
        }


        const tasks = await response.json();


        saveTasksToLocalStorage(tasks);

        renderTasks(tasks);

    } catch (error) {
        console.error(error);


        const savedTasks =
            loadTasksFromLocalStorage();


        if (savedTasks.length > 0) {

            renderTasks(savedTasks);

            showMessage(
                "Showing saved tasks. Backend is currently unavailable.",
                true
            );

        } else {

            showMessage(
                "Unable to load tasks. Start the backend server.",
                true
            );
        }
    }
}


// ============================================================
// RENDER TASKS
// ============================================================

function renderTasks(tasks) {

    taskList.innerHTML = "";


    if (!tasks || tasks.length === 0) {

        const emptyMessage =
            document.createElement("li");

        emptyMessage.textContent =
            "No tasks available.";

        taskList.appendChild(
            emptyMessage
        );

        return;
    }


    tasks.forEach(task => {

        const li =
            document.createElement("li");


        const taskText =
            document.createElement("span");


        taskText.textContent =
            `${task.id} - ${task.title} | ` +
            `${task.priority} | ` +
            `${task.status} | ` +
            `Due: ${task.due_date || "Not set"} | ` +
            `Project: ${task.project_id}`;


        li.appendChild(taskText);


        // ----------------------------------------------------
        // EDIT
        // ----------------------------------------------------

        const editButton =
            document.createElement("button");

        editButton.textContent = "Edit";

        editButton.type = "button";


        editButton.addEventListener(
            "click",
            () => editTask(task)
        );


        li.appendChild(editButton);


        // ----------------------------------------------------
        // DELETE
        // ----------------------------------------------------

        const deleteButton =
            document.createElement("button");

        deleteButton.textContent = "Delete";

        deleteButton.type = "button";


        deleteButton.addEventListener(
            "click",
            () => deleteTask(task.id)
        );


        li.appendChild(deleteButton);


        taskList.appendChild(li);
    });
}


// ============================================================
// GET TASK BY ID
// ============================================================

async function getTask(taskId) {

    try {

        const response =
            await fetch(
                `${API_URL}/tasks/${taskId}`
            );


        const data =
            await response.json();


        if (!response.ok) {

            showMessage(
                data.detail ||
                "Task not found.",
                true
            );

            return null;
        }


        return data;

    } catch (error) {

        console.error(error);

        showMessage(
            "Unable to connect to backend.",
            true
        );

        return null;
    }
}


// ============================================================
// EDIT TASK
// ============================================================

async function editTask(task) {

    const newTitle =
        prompt(
            "Enter new task title:",
            task.title
        );


    if (newTitle === null) {
        return;
    }


    const trimmedTitle =
        newTitle.trim();


    if (!trimmedTitle) {

        showMessage(
            "Task title cannot be blank.",
            true
        );

        return;
    }


    const newPriority =
        prompt(
            "Enter priority: low, medium or high",
            task.priority
        );


    if (newPriority === null) {
        return;
    }


    const priority =
        newPriority.trim().toLowerCase();


    if (
        !["low", "medium", "high"]
            .includes(priority)
    ) {

        showMessage(
            "Priority must be low, medium or high.",
            true
        );

        return;
    }


    const newStatus =
        prompt(
            "Enter status: pending, in_progress or completed",
            task.status
        );


    if (newStatus === null) {
        return;
    }


    const status =
        newStatus.trim().toLowerCase();


    if (
        ![
            "pending",
            "in_progress",
            "completed"
        ].includes(status)
    ) {

        showMessage(
            "Invalid task status.",
            true
        );

        return;
    }


    const newDueDate =
        prompt(
            "Enter due date (YYYY-MM-DD), or leave blank:",
            task.due_date || ""
        );


    if (newDueDate === null) {
        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/tasks/${task.id}`,
                {
                    method: "PUT",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        title: trimmedTitle,
                        priority: priority,
                        status: status,
                        due_date:
                            newDueDate.trim() ||
                            null
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            showMessage(
                data.detail ||
                "Unable to update task.",
                true
            );

            return;
        }


        showMessage(
            "Task updated successfully!"
        );


        await loadTasks();

    } catch (error) {

        console.error(error);

        showMessage(
            "Unable to connect to backend.",
            true
        );
    }
}


// ============================================================
// DELETE TASK
// ============================================================

async function deleteTask(taskId) {

    const confirmed =
        confirm(
            "Are you sure you want to delete this task?"
        );


    if (!confirmed) {
        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/tasks/${taskId}`,
                {
                    method: "DELETE"
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            showMessage(
                data.detail ||
                "Unable to delete task.",
                true
            );

            return;
        }


        showMessage(
            "Task deleted successfully!"
        );


        await loadTasks();

    } catch (error) {

        console.error(error);

        showMessage(
            "Unable to connect to backend.",
            true
        );
    }
}


// ============================================================
// LINEAR / BINARY SEARCH
// ============================================================

async function searchTasks(algo) {

    const searchInput =
        document.getElementById(
            "searchTitle"
        );


    if (!searchInput) {

        showMessage(
            "Search input is not available.",
            true
        );

        return;
    }


    const title =
        searchInput.value.trim();


    if (!title) {

        showMessage(
            "Please enter a task title.",
            true
        );

        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/tasks/search` +
                `?title=${encodeURIComponent(title)}` +
                `&algo=${encodeURIComponent(algo)}`
            );


        const data =
            await response.json();


        if (!response.ok) {

            showMessage(
                data.detail ||
                "Task not found.",
                true
            );

            return;
        }


        renderTasks([data]);


        showMessage(
            `${algo === "linear"
                ? "Linear"
                : "Binary"} Search completed successfully.`
        );

    } catch (error) {

        console.error(error);

        showMessage(
            "Unable to connect to backend.",
            true
        );
    }
}


// ============================================================
// QUICK ADD TASK
// ============================================================

async function quickAddTask() {

    const descriptionInput =
        document.getElementById(
            "quickAddDescription"
        );


    const projectInput =
        document.getElementById(
            "quickAddProjectId"
        );


    if (
        !descriptionInput ||
        !projectInput
    ) {

        showMessage(
            "Quick Add fields are not available.",
            true
        );

        return;
    }


    const description =
        descriptionInput.value.trim();


    const projectId =
        Number(projectInput.value);


    if (!description) {

        showMessage(
            "Please enter a task description.",
            true
        );

        return;
    }


    if (!projectId || projectId < 1) {

        showMessage(
            "Please enter a valid Project ID.",
            true
        );

        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/tasks/quick-add`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        description:
                            description,
                        project_id:
                            projectId
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            showMessage(
                data.detail ||
                "Unable to create quick task.",
                true
            );

            return;
        }


        showMessage(
            "Quick task created successfully!"
        );


        descriptionInput.value = "";


        await loadTasks();

    } catch (error) {

        console.error(error);

        showMessage(
            "Unable to connect to backend.",
            true
        );
    }
}


// ============================================================
// PROJECT STATISTICS
// ============================================================

async function loadProjectStatistics() {

    try {

        const response =
            await fetch(
                `${API_URL}/projects/statistics`
            );


        const data =
            await response.json();


        if (!response.ok) {

            showMessage(
                data.detail ||
                "Unable to load project statistics.",
                true
            );

            return;
        }


        console.log(
            "Project Statistics:",
            data
        );


        return data;

    } catch (error) {

        console.error(
            "Statistics error:",
            error
        );

        return [];
    }
}


// ============================================================
// CREATE SEARCH / QUICK ADD CONTROLS
// ============================================================

function addExtraControls() {

    if (
        document.getElementById(
            "taskflowExtraControls"
        )
    ) {
        return;
    }


    if (!taskList) {
        return;
    }


    const section =
        document.createElement("section");


    section.id =
        "taskflowExtraControls";


    section.innerHTML = `
        <hr>

        <h2>Search Tasks</h2>

        <input
            type="text"
            id="searchTitle"
            placeholder="Enter task title"
        >

        <button
            type="button"
            id="linearSearchButton"
        >
            Linear Search
        </button>

        <button
            type="button"
            id="binarySearchButton"
        >
            Binary Search
        </button>


        <h2>Quick Add Task</h2>

        <input
            type="text"
            id="quickAddDescription"
            placeholder="e.g. Learn Python tomorrow"
        >

        <input
            type="number"
            id="quickAddProjectId"
            value="1"
            min="1"
            placeholder="Project ID"
        >

        <button
            type="button"
            id="quickAddButton"
        >
            Quick Add
        </button>

        <hr>
    `;


    taskList.parentElement.insertBefore(
        section,
        taskList
    );


    document
        .getElementById(
            "linearSearchButton"
        )
        .addEventListener(
            "click",
            () => searchTasks("linear")
        );


    document
        .getElementById(
            "binarySearchButton"
        )
        .addEventListener(
            "click",
            () => searchTasks("binary")
        );


    document
        .getElementById(
            "quickAddButton"
        )
        .addEventListener(
            "click",
            quickAddTask
        );
}


// ============================================================
// FORM EVENTS
// ============================================================

if (taskForm) {

    taskForm.addEventListener(
        "submit",
        createTask
    );
}


if (refreshButton) {

    refreshButton.addEventListener(
        "click",
        loadTasks
    );
}


// ============================================================
// INITIAL LOAD
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        addExtraControls();

        loadTasks();

        loadProjectStatistics();
    }
);