import platform
import wmi

#zwraca informacje o systemie
#zwracane wartości:"system","release","version"
def sys_info():
    system_name = platform.system()
    release_info = platform.release()
    version_info = platform.version()

    data = {
        "system": system_name,
        "release": release_info,
        "version": version_info
    }
    return data
# Przykładowe użycie
# info = sys_info()
# for key, value in info.items():
#     print(f"{key}: {value}")

#-----------------------------------------------------------------

#zwraca liste wpisów json (jeden procesor jeden JSON)
# Zwracane wartości:"name","description","numberOfCores","numberOfLogicalProcessors","maxClockSpeed"
def cpu_info():
    w = wmi.WMI()
    fulldata = []  
    for cpu in w.Win32_Processor():
        data = {
            "name": cpu.Name,
            "description":cpu.Description,
            "numberOfCores": cpu.NumberOfCores,
            "numberOfLogicalProcessors": cpu.NumberOfLogicalProcessors,
            "maxClockSpeed": cpu.MaxClockSpeed
            
        }
        fulldata.append(data) 
    return fulldata
# Przykładowe użycie
# info = cpu_info()
# for i in info:
#      print(i)

#-----------------------------------------------------------------

# zwraca aktualne wykorzystanie procesora
def cpu_usage():
     w = wmi.WMI()
     fulldata = []
     for cpu in w.Win32_Processor():
        usage = cpu.LoadPercentage
        fulldata.append(usage)
     return fulldata
#Przykładowe użycie :
# while True:
#         usage = system_info.cpu_usage()
#         for i, load in enumerate(usage):
#             print(f"CPU {i}: {load}% usage")
 
#-----------------------------------------------------------------
# Zwraca informacje o pamięci ram (jedna kość jeden słownik+ na końcu sumę pamięci ram)

def memory_info():
    c = wmi.WMI()
    memory_info = c.Win32_PhysicalMemory()
    memory_list = []
    total = 0  # Zainicjalizowane jako 0
    for memory in memory_info:
        capacity_gb = int(memory.Capacity) / (1024**3)  # Konwersja na GB
        total += capacity_gb
        data = {
            "capacity": f"{capacity_gb} GB",
            "speed": f"{memory.Speed} MHz",
            "type": memory.MemoryType
        }
        memory_list.append(data)
    
    return memory_list, total

# Przykład użycia
# memory_list, total_capacity = memory_info()
# print(memory_list)
# print(total_capacity)
#-----------------------------------------------------------------

# zwraca aktualne wykorzystanie pamięci Ram z dokładnością do 2 miejsc po przecinku
def memory_usage():
    w = wmi.WMI()
    for os in w.Win32_OperatingSystem():
        total = int(os.TotalVisibleMemorySize)
        free = int(os.FreePhysicalMemory)
        usage = total - free

    usage_gb = usage / 1048576
    usage_gb = round(usage_gb,2)
    return usage_gb
#przykładowe użycie:
# while True:
#          usage = memory_usage()
#          print(usage) 

#-----------------------------------------------------------------




# def check_ram_type():
#     c = wmi.WMI()
#     memory_info = c.Win32_PhysicalMemory()

#     for memory in memory_info:
#         print(f"Capacity: {int(memory.Capacity) / (1024**3)} GB")
#         print(f"Speed: {memory.Speed} MHz")
#         print(f"MemoryType: {memory.MemoryType}")

# check_ram_type()
