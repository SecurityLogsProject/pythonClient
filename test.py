import codecs
import os
import sys
import time
import traceback
import win32con
import win32evtlog
import win32evtlogutil
import winerror

#----------------------------------------------------------------------
def getAllEvents(server, logtypes, basePath):
    if not server:
        serverName = "localhost"
    else: 
        serverName = server
    for logtype in logtypes:
        # Ensure the directory exists before creating the log file
        if not os.path.exists(basePath):
            os.makedirs(basePath)
        path = os.path.join(basePath, "%s_%s_log.txt" % (serverName, logtype))
        getEventLogs(server, logtype, path)

#----------------------------------------------------------------------
def getEventLogs(server, logtype, logPath):
    print ("Logging %s events" % logtype)
    with codecs.open(logPath, encoding='utf-8', mode='w') as log:
        line_break = '-' * 80
        
        log.write("\n%s Log of %s Events\n" % (server, logtype))
        log.write("Created: %s\n\n" % time.ctime())
        log.write("\n" + line_break + "\n")
        hand = win32evtlog.OpenEventLog(server,logtype)
        total = win32evtlog.GetNumberOfEventLogRecords(hand)
        print ("Total events in %s = %s" % (logtype, total))

        
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
        events = win32evtlog.ReadEventLog(hand,flags,0)
        evt_dict={win32con.EVENTLOG_AUDIT_FAILURE:'EVENTLOG_AUDIT_FAILURE',
                  win32con.EVENTLOG_AUDIT_SUCCESS:'EVENTLOG_AUDIT_SUCCESS',
                  win32con.EVENTLOG_INFORMATION_TYPE:'EVENTLOG_INFORMATION_TYPE',
                  win32con.EVENTLOG_WARNING_TYPE:'EVENTLOG_WARNING_TYPE',
                  win32con.EVENTLOG_ERROR_TYPE:'EVENTLOG_ERROR_TYPE'}
        
        try:
            while events:
                for ev_obj in events:
                    the_time = ev_obj.TimeGenerated.Format() #'12/23/99 15:54:09'
                    evt_id = str(winerror.HRESULT_CODE(ev_obj.EventID))
                    record = ev_obj.RecordNumber
                    msg = win32evtlogutil.SafeFormatMessage(ev_obj, logtype)
                    
                    source = str(ev_obj.SourceName)
                    evt_type = evt_dict.get(ev_obj.EventType, "unknown")
                    
                    
                    # To przerobić tak żeby generowało JSON


                    log.write("Event Date/Time: %s\n" % the_time)
                    log.write("Event ID / Type: %s / %s\n" % (evt_id, evt_type))
                    log.write("Record #%s\n" % record)
                    log.write("Source: %s\n\n" % source)
                    log.write(msg)
                    log.write("\n\n")
                    log.write(line_break)
                    log.write("\n\n")
                events = win32evtlog.ReadEventLog(hand,flags,0)
        except Exception as e:
            print("Exception occurred:", e)
            traceback.print_exc(file=sys.stdout)
    print ("Log creation finished. Location of log is %s" % logPath)


if __name__ == "__main__":
    server = None  # None = local machine
    logTypes = ["System", "Application", "Security", "Setup"]
    getAllEvents(server, logTypes, "logtest.txt")
