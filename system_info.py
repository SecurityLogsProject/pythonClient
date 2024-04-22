import platform
import wmi


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
#zwraca liste wpisów json (jeden procesor jeden JSON)
def cpu_info():
    w = wmi.WMI()
    fulldata = []  # Inicjalizacja zmiennej jako pustej listy
    for cpu in w.Win32_Processor():
        data = {
            "name": cpu.Name,
            "description":cpu.Description,
            "numberOfCores": cpu.NumberOfCores,
            "numberOfLogicalProcessors": cpu.NumberOfLogicalProcessors,
            "maxClockSpeed": cpu.MaxClockSpeed
            
        }
        fulldata.append(data)  # Dodanie słownika do listy
    
    return fulldata

def cpu_usage():
     w = wmi.WMI()
     fulldata = []
     for cpu in w.Win32_Processor():
        usage = cpu.LoadPercentage
        fulldata.append(usage)
     return fulldata

def memory_info():
    for os in w.Win32_OperatingSystem():
        return os.TotalVisibleMemorySize
    
def memory_usage():
    w = wmi.WMI()
    for os in w.Win32_OperatingSystem():
        total = int(os.TotalVisibleMemorySize)
        free = int(os.FreePhysicalMemory)
        usage = total - free

    usage_gb = usage / 1048576  # Konwersja z KB na GiB
    return usage_gb