import get_logs
import endpoint_info



#pobieranie logów
#-----------------------------------------------------------------
server = None  # None = local machine
logTypes = ["System", "Application", "Security", "Setup"] #Jakiego rodzaju logi będą pobierane
basePath = "./logtest" #folder zapisu logów
output_format = 'json'  #format zapisu 'txt' lub 'json'
    
#-----------------------------------------------------------------
while True:
        usage = endpoint_info.cpu_usage()
        for i in usage:
            print(f"CPU {i}: % usage")


