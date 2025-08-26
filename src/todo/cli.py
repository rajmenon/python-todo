from __future__ import annotations

import time

import typer
from rich.console import Console
from rich.table import Table

from .models import Status, TodoItem, TodoList

# in-memory store instance
store = TodoList()

app = typer.Typer(add_completion=False, help="A clean, type-safe todo CLI.")
console = Console()


@app.command()
def add(
    title: str = typer.Argument(..., help="Todo title"),
) -> None:
    todo: TodoItem = TodoItem(title=title, status=Status.INCOMPLETE)
    store.add_item(todo)
    console.print(f"[green]Added:[/green] {todo}")

@app.command("list")
def list_cmd() -> None:
    items: list[TodoItem]
    items = store.get_items()
    table = Table(title="Todos")
    table.add_column("ID", style="cyan", overflow="fold")
    table.add_column("Title", style="white")
    table.add_column("Priority", style="magenta")
    table.add_column("Done", style="green")

    for t in items:
        table.add_row(str(t.id), t.title, t.datemodified, "✓" if t.done else " ")
    console.print(table)


@app.command()
def done(todo_id: str = typer.Argument(..., help="UUID of the todo")) -> None:
    try:
        changed = store.mark_complete(todo_id)
        # get title for nicer output
        title = store.get_items()
        title = next((t.title for t in title if str(t.id) == todo_id), todo_id)
        if changed:
            console.print(f"[green]Done:[/green] {title}")
        else:
            console.print(f"[yellow]Already done:[/yellow] {title}")
    except KeyError:
        console.print(f"[red]Not found:[/red] {todo_id}", style="red")
        raise typer.Exit(code=1) from None

@app.command()
def delete(todo_id: str = typer.Argument(..., help="UUID of the todo")) -> None:
    try:
        store.delete(todo_id)
        console.print(f"[yellow]Deleted:[/yellow] {todo_id}")
    except KeyError as e:
        console.print(f"[red]{e}[/red]")
    raise typer.Exit(code=1) from None

if __name__ == "__main__":
    app()
