import streamlit as st
import json
import os

FILENAME = "tasks.json"

# Load tasks
def load_tasks():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            return json.load(f)
    return {"tasks": [], "points": 0}

# Save tasks
def save_tasks(data):
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)

def main():
    st.title("🎮 To-Do List Game")
    st.write("Complete tasks and earn points!")

    data = load_tasks()
    tasks = data["tasks"]
    points = data["points"]

    st.sidebar.header("🏆 Your Progress")
    st.sidebar.write(f"**Points:** {points}")
    level = points // 10 + 1
    st.sidebar.write(f"**Level:** {level}")

    # Add new task
    new_task = st.text_input("Enter a new task")
    if st.button("➕ Add Task"):
        if new_task.strip():
            tasks.append({"title": new_task, "done": False})
            save_tasks(data)
            st.success("Task added!")
            st.rerun()
        else:
            st.warning("Task cannot be empty!")

    st.subheader("📋 Your Tasks")
    if tasks:
        for i, task in enumerate(tasks):
            col1, col2, col3 = st.columns([5, 1, 1])
            with col1:
                st.write(f"{'✔️' if task['done'] else '❌'} {task['title']}")
            with col2:
                if not task["done"]:
                    if st.button("✅ Done", key=f"done_{i}"):
                        tasks[i]["done"] = True
                        data["points"] += 5   # give points for completing
                        save_tasks(data)
                        st.balloons()
                        st.success("Great job! You earned 5 points 🎉")
                        st.rerun()
            with col3:
                if st.button("🗑️ Delete", key=f"delete_{i}"):
                    tasks.pop(i)
                    save_tasks(data)
                    st.warning("Task deleted!")
                    st.rerun()
    else:
        st.info("No tasks yet. Add one above!")

if __name__ == "__main__":
    main()
