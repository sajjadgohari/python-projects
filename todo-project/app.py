from models import ToDoList, Task

def print_task(t: Task):
    # Display a single task in a human-readable format
    done = "✓" if t.done else " "
    print(f"[{done}] {t.title} (id={t.id}) priority={t.priority} due={t.due_date}")

def main():
    # Entry point for the CLI application
    td = ToDoList()  # Create a new to-do list (loads tasks from CSV)
    while True:
        print()
        print("Commands: add, list, list_pending, remove, done, priority, exit")
        cmd = input("cmd> ").strip().lower()

        if cmd in ("exit", "quit", "q"):
            # Exit the program
            break

        if cmd == "add":
            # Add a new task
            title = input("title: ").strip()
            desc = input("description: ").strip()
            pr = input("priority (1-high,2-medium,3-low): ").strip() or "2"
            due = input("due (YYYY-MM-DD) or empty: ").strip()
            t = Task.create(title, desc, pr, due)
            td.add(t)
            print("Added", t.id)
            continue

        if cmd == "list":
            # List all tasks
            for t in td.list(show_all=True):
                print_task(t)
            continue

        if cmd == "list_pending":
            # List only pending (not completed) tasks
            for t in td.list(show_all=False):
                print_task(t)
            continue

        if cmd == "remove":
            # Remove a task by ID
            id = input("id: ").strip()
            ok = td.remove(id)
            print("Removed" if ok else "Not found")
            continue

        if cmd == "done":
            # Mark a task as completed
            id = input("id: ").strip()
            ok = td.mark_done(id)
            print("Marked done" if ok else "Not found")
            continue

        if cmd == "priority":
            # Change the priority of a task
            id = input("id: ").strip()
            pr = input("new priority (1/2/3): ").strip()
            ok = td.change_priority(id, pr)
            print("Priority changed" if ok else "Not found")
            continue

        # Handle invalid commands
        print("Unknown command")

if __name__ == "__main__":
    main()
