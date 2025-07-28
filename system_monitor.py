from rich.console import Console
import time
import psutil


console = Console()

with console.status("Loading system resources..."):
    cpu_percent=psutil.cpu_percent(1)
    virtual_memory=psutil.virtual_memory()
    disk_partitions=psutil.disk_partitions(all=False)
    
    

console.rule("[bold red]System Monitor")
console.print(f"[bold]CPU Usage:[/bold] {cpu_percent} %")
console.print(f"[bold]Memory Usage:[/bold] {virtual_memory.percent} % used of {virtual_memory.total // (1024**3)} GB\n")

