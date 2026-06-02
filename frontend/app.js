const API_URL = "http://localhost:8000";

const form = document.getElementById("todo-form");
const input = document.getElementById("todo-input");
const list = document.getElementById("todo-list");

async function loadTodos() {
  const response = await fetch(`${API_URL}/todos`);
  const todos = await response.json();

  list.innerHTML = "";

  todos.forEach((todo) => {
    const li = document.createElement("li");
    const title = document.createElement("span");
    title.textContent = todo.title;

    const status = document.createElement("select");
    ["pending", "active", "completed"].forEach((value) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = value[0].toUpperCase() + value.slice(1);
      status.appendChild(option);
    });
    status.value = todo.status || (todo.completed ? "completed" : "pending");
    status.addEventListener("change", () => updateTodoStatus(todo.id, status.value));

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.addEventListener("click", () => deleteTodo(todo.id));

    li.append(title, status, deleteButton);
    list.appendChild(li);
  });
}

async function addTodo(title) {
  await fetch(`${API_URL}/todos`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ title }),
  });

  loadTodos();
}

async function deleteTodo(id) {
  await fetch(`${API_URL}/todos/${id}`, {
    method: "DELETE",
  });

  loadTodos();
}

async function updateTodoStatus(id, status) {
  await fetch(`${API_URL}/todos/${id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ status }),
  });

  loadTodos();
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const title = input.value.trim();

  if (!title) return;

  await addTodo(title);
  input.value = "";
});

loadTodos();
