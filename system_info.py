import psutil
import platform
#from rich import print


system_info = {
    "OS": platform.system(),
    "Release": platform.release(),
    "Version": platform.version(),
    "Machine" : platform.machine(),
    "Processor": platform.processor(),
    "Python Version": platform.python_version(),

}

cpu_info = platform.processor()
cpu_count = psutil.cpu_count(logical=False)
logical_cpu_count = psutil.cpu_count(logical=True)


print ("\n========================================\n")



for key,value in system_info.items():
    print(f"{key}: {value}YO")



print ("\n========================================\n")
print("\nCPU Information:")
print(f"Processor: {cpu_info}")
print(f"Physical Cores: {cpu_count}")
print(f"Logical Cores: {logical_cpu_count}")

print ("\n========================================\n")

memory_info = psutil.virtual_memory()

print("\nMemory Information:")
print(f"Total Memory: {memory_info.total} bytes")
print(f"Available Memory: {memory_info.available} bytes")
print(f"Used Memory: {memory_info.used} bytes")
print(f"Memory Utilization: {memory_info.percent}%")

print ("\n========================================\n")

disk_info = psutil.disk_usage('/')

print("\nDisk Information:")
print(f"Total Disk Space: {disk_info.total} bytes")
print(f"Used Disk Space: {disk_info.used} bytes")
print(f"Free Disk Space: {disk_info.free} bytes")
print(f"Disk Space Utilization: {disk_info.percent}%")


