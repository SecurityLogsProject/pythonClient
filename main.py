import get_logs
import system_info



#pobieranie logów
#-----------------------------------------------------------------
server = None  # None = local machine
logTypes = ["System", "Application", "Security", "Setup"] #Jakiego rodzaju logi będą pobierane
basePath = "./logtest" #folder zapisu logów
output_format = 'json'  #format zapisu 'txt' lub 'json'
    
 testowe4.getAllEvents(server, logTypes, basePath, output_format)
#-----------------------------------------------------------------
while True:
        usage = system_info.cpu_usage()
        for i in usage:
            print(f"CPU {i}: % usage")


