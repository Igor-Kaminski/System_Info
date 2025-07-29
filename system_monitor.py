from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
import psutil
import GPUtil


console = Console()

with console.status("Loading system resources..."):
    cpu_percent=psutil.cpu_percent(1)
    virtual_memory=psutil.virtual_memory()
    disk_partitions=psutil.disk_partitions(all=False)
    virtual_memory_total =  virtual_memory.total / (1024 **3)
    virtual_memory_used =  virtual_memory_total - (virtual_memory.available / (1024**3))
    
    
    try:
        temperatures = psutil.sensors_temperatures()
        cpu_temp = None
        if 'coretemp' in temperatures:
            cpu_temp = temperatures['coretemp'][0].current
        elif 'k10temp' in temperatures:
            cpu_temp = temperatures['k10temp'][0].current
        elif 'cpu_thermal' in temperatures:
            cpu_temp = temperatures['cpu_thermal'][0].current
    except:
        cpu_temp = None
    
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0] 
            gpu_usage = gpu.load * 100
            gpu_temp = gpu.temperature
        else:
            gpu_usage = None
            gpu_temp = None
    except:
        gpu_usage = None
        gpu_temp = None
    
    

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
    TextColumn(f"[bold cyan]CPU Usage: {{task.percentage:>5.1f}}%"),
    BarColumn(bar_width=40, complete_style="bright_green", finished_style="bright_green"),
    TextColumn(f"[bold white]{cpu_temp:.1f}°C" if cpu_temp else "[bold white]N/A"),
)
cpu_task = cpu_progress.add_task("", total=100)
cpu_progress.update(cpu_task, completed=cpu_percent)

cpu_panel = Panel(
    cpu_progress,
    title="[bold cyan]CPU Monitor",
    border_style="cyan",
    padding=(1, 2)
)

gpu_progress = Progress(
    TextColumn(f"[bold green]GPU Usage: {{task.percentage:>5.1f}}%"),
    BarColumn(bar_width=40, complete_style="bright_green", finished_style="bright_green"),
    TextColumn(f"[bold white]{gpu_temp:.1f}°C" if gpu_temp else "[bold white]N/A"),
)
gpu_task = gpu_progress.add_task("", total=100)
gpu_progress.update(gpu_task, completed=gpu_usage if gpu_usage else 0)

gpu_panel = Panel(
    gpu_progress,
    title="[bold green]GPU Monitor",
    border_style="green",
    padding=(1, 2)
)

memory_progress = Progress(
    TextColumn(f"[bold magenta]Memory Usage: {{task.percentage:>5.1f}}%"),
    BarColumn(bar_width=40, complete_style="bright_magenta", finished_style="bright_magenta"),
    TextColumn(f"[bold white]({virtual_memory_used:.1f}GB / {virtual_memory_total:.1f}GB)"),
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
console.print(gpu_panel)
console.print(memory_panel)



