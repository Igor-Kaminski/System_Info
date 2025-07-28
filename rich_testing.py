from rich.console import Console
import time

def do_work():
    print("test")
    time.sleep(5)

console = Console()
console.print("Hello, [bold magenta]World[/]!", ":vampire:")

console.rule("[bold red]CPU Status Bar")

with console.status("Working..."):
    do_work()