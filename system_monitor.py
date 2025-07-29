from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.console import Group
import psutil
import GPUtil
import time



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
    
    

disk_table = Table(title="[cyan]Disk Partitions", title_justify="center")

disk_table.add_column("[red]Device", justify="center", style="cyan", no_wrap=True)
disk_table.add_column("[red]Mount", justify="center", style="green", no_wrap=True)
disk_table.add_column("[red]File System", justify="center", style="magenta", no_wrap=True)
disk_table.add_column("[red]Total", justify="center", style="yellow", no_wrap=True)
disk_table.add_column("[red]Used", justify="center", style="cyan", no_wrap=True)
disk_table.add_column("[red]Free", justify="center", style="green", no_wrap=True)
disk_table.add_column("[red]Percent Used", justify="center", style="magenta", no_wrap=True)

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


cpu_progress = Progress(
    TextColumn("[bold cyan]CPU Usage: {task.percentage:>5.1f}%"),
    BarColumn(bar_width=40, complete_style="bright_green", finished_style="bright_green"),
    TextColumn("[bold white]{task.description}"),
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
    TextColumn("[bold green]GPU Usage: {task.percentage:>5.1f}%"),
    BarColumn(bar_width=40, complete_style="bright_green", finished_style="bright_green"),
    TextColumn("[bold white]{task.description}"),
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
    TextColumn("[bold magenta]Memory Usage: {task.percentage:>5.1f}%"),
    BarColumn(bar_width=40, complete_style="bright_magenta", finished_style="bright_magenta"),
    TextColumn("[bold white]{task.description}"),
)
memory_task = memory_progress.add_task("", total=100)
memory_progress.update(memory_task, completed=virtual_memory.percent)

memory_panel = Panel(
    memory_progress,
    title="[bold magenta]Memory Monitor",
    border_style="magenta",
    padding=(1, 2)
)

def update_display():
    current_cpu = psutil.cpu_percent(1)
    cpu_progress.update(cpu_task, completed=current_cpu)
    
    try:
        temperatures = psutil.sensors_temperatures()
        current_cpu_temp = None
        if 'coretemp' in temperatures:
            current_cpu_temp = temperatures['coretemp'][0].current
        elif 'k10temp' in temperatures:
            current_cpu_temp = temperatures['k10temp'][0].current
        elif 'cpu_thermal' in temperatures:
            current_cpu_temp = temperatures['cpu_thermal'][0].current
    except:
        current_cpu_temp = None
    
    cpu_temp_text = f"{current_cpu_temp:.1f}°C" if current_cpu_temp else "N/A"
    cpu_progress.update(cpu_task, description=cpu_temp_text)
    
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]
            current_gpu_usage = gpu.load * 100
            current_gpu_temp = gpu.temperature
            gpu_progress.update(gpu_task, completed=current_gpu_usage)
        else:
            current_gpu_usage = 0
            current_gpu_temp = None
    except:
        current_gpu_usage = 0
        current_gpu_temp = None
    
    gpu_temp_text = f"{current_gpu_temp:.1f}°C" if current_gpu_temp else "N/A"
    gpu_progress.update(gpu_task, description=gpu_temp_text)
    
    current_memory = psutil.virtual_memory()
    current_memory_total = current_memory.total / (1024 ** 3)
    current_memory_used = current_memory_total - (current_memory.available / (1024 ** 3))
    memory_progress.update(memory_task, completed=current_memory.percent)
    
    memory_text = f"({current_memory_used:.1f}GB / {current_memory_total:.1f}GB)"
    memory_progress.update(memory_task, description=memory_text)


def generate_display():
    title_panel = Panel("[bold red]System Monitor", padding=(0, 0), title_align="center")
    
    return Group(
        title_panel,
        disk_table,
        cpu_panel,
        gpu_panel,
        memory_panel
    )

with Live(generate_display(), console=console, auto_refresh=False) as live:
    try:
        while True:
            update_display()
            live.update(generate_display(), refresh=True)
            time.sleep(1)
    except KeyboardInterrupt:
        pass

console.print("\n[bold red]System Monitor stopped.[/bold red]")



