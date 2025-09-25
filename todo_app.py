import streamlit as st
import json
import os

FILENAME = "tasks.json"

# Load tasks
def load_tasks():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            return json.load(f)
    return []

# Save tasks
def save_tasks(tasks):
    with open(FILENAME, "w") as f:
        json.dump(tasks, f, indent=4)

# App
def main():
    st.title("📝 To-Do List App")
    st.write("Manage your daily tasks easily!")

    tasks = load_tasks()

    # Add new task
    new_task = st.text_input("Enter a new task")
    if st.button("➕ Add Task"):
        if new_task.strip():
            tasks.append({"title": new_task, "done": False})
            save_tasks(tasks)
            st.success("Task added!")
            st.experimental_rerun()
        else:
            st.warning("Task cannot be empty!")

    st.subheader("📋 Your Tasks")
    if tasks:
        for i, task in enumerate(tasks):
            col1, col2, col3 = st.columns([5, 1, 1])
            with col1:
                st.write(f"{'✔️' if task['done'] else '❌'} {task['title']}")
            with col2:
                if st.button("✅ Done", key=f"done_{i}"):
                    tasks[i]["done"] = True
                    save_tasks(tasks)
                    st.experimental_rerun()
            with col3:
                if st.button("🗑️ Delete", key=f"delete_{i}"):
                    tasks.pop(i)
                    save_tasks(tasks)
                    st.experimental_rerun()
    else:
        st.info("No tasks yet. Add one above!")

if __name__ == "__main__":
    main()
