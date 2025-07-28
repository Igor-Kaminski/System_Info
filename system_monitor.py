from rich.console import Console
from rich.table import Table
import time
import psutil


console = Console()

with console.status("Loading system resources..."):
    cpu_percent=psutil.cpu_percent(1)
    virtual_memory=psutil.virtual_memory()
    disk_partitions=psutil.disk_partitions(all=False)
    
    

console.rule("[bold red]System Monitor")
console.print(f"\n[bold]CPU Usage:[/bold] {cpu_percent} %")

virtual_memory_total =  virtual_memory.total / (1024 **3)
virtual_memory_used =  virtual_memory_total - (virtual_memory.available / (1024**3))
console.print(f"[bold]Memory Usage Percentage:[/bold] {virtual_memory.percent:.1f}% ({virtual_memory_used:.1f}GB) used of {virtual_memory_total:.1f} GB \n ")





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





console.print(disk_table)