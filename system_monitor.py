from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
import psutil


console = Console()

with console.status("Loading system resources..."):
    cpu_percent=psutil.cpu_percent(1)
    virtual_memory=psutil.virtual_memory()
    disk_partitions=psutil.disk_partitions(all=False)
    virtual_memory_total =  virtual_memory.total / (1024 **3)
    virtual_memory_used =  virtual_memory_total - (virtual_memory.available / (1024**3))
    
    

console.rule("[bold red]System Monitor") 

console.print()

disk_table = Table(title="[cyan]Disk Partitions")

disk_table.add_column("[red]Device", justify="right", style="cyan", no_wrap=True)
disk_table.add_column("[red]Mount", justify="right", style="green", no_wrap=True)
disk_table.add_column("[red]File System", justify="right", style="magenta", no_wrap=True)
disk_table.add_column("[red]Total", justify="right", style="yellow", no_wrap=True)
disk_table.add_column("[red]Used", justify="right", style="cyan", no_wrap=True)
disk_table.add_column("[red]Free", justify="right", style="green", no_wrap=True)
disk_table.add_column("[red]Percent Used", justify="right", style="magenta", no_wrap=True)


for partition in disk_partitions:
    try:
        usage = psutil.disk_usage(partition.mountpoint)
        disk_table.add_row(
            partition.device,
            partition.mountpoint,
            partition.fstype,
            f"{usage.total // (1024 ** 3)} GB",
            f"{usage.used // (1024 ** 3)} GB",
            f"{usage.free // (1024 ** 3)} GB",
            f"{usage.percent} %"
        )
    except PermissionError:
        continue 
console.print(disk_table, justify="center")

console.print()

cpu_progress = Progress(
    TextColumn(f"[bold cyan]CPU Usage: {{task.percentage:>5.1f}}% (Current: {cpu_percent:.1f}%)"),
    BarColumn(bar_width=40, complete_style="bright_green", finished_style="bright_green"),
    TextColumn("[bold white]{task.percentage:>5.1f}%"),
    console=console
)
cpu_task = cpu_progress.add_task("", total=100)
cpu_progress.update(cpu_task, completed=cpu_percent)

cpu_panel = Panel(
    cpu_progress,
    title="[bold cyan]CPU Monitor",
    border_style="cyan",
    padding=(1, 2)
)

memory_progress = Progress(
    TextColumn(f"[bold magenta]Memory Usage: {{task.percentage:>5.1f}}% ({virtual_memory_used:.1f}GB) / {virtual_memory_total:.1f}GB"),
    BarColumn(bar_width=40, complete_style="bright_magenta", finished_style="bright_magenta"),
    TextColumn("[bold white]{task.percentage:>5.1f}%"),
    console=console
)
memory_task = memory_progress.add_task("", total=100)
memory_progress.update(memory_task, completed=virtual_memory.percent)

memory_panel = Panel(
    memory_progress,
    title="[bold magenta]Memory Monitor",
    border_style="magenta",
    padding=(1, 2)
)

console.print(cpu_panel)
console.print(memory_panel)



