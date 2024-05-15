import json
import codecs
import os
import time
import logging
import datetime
import win32con
import win32evtlog
import win32evtlogutil
import winerror
import requests
from dotenv import load_dotenv

load_dotenv()

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def getAllEvents(server, logtypes, basePath, format='txt'):
    serverName = server if server else "localhost"
    for logtype in logtypes:
        os.makedirs(basePath, exist_ok=True)
        if format == 'json':
            path = os.path.join(basePath, f"{serverName}_{logtype}_log.json")
        else:
            path = os.path.join(basePath, f"{serverName}_{logtype}_log.txt")
        getEventLogs(serverName, logtype, path, format)


def getEventLogs(server, logtype, logPath, format):
    logging.info(f"Logging {logtype} events in {format} format")
    buffered_entries = []
    buffer_size = 1000
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    try:
        with codecs.open(logPath, 'w', 'utf-8') as log:
            if format == 'txt':
                write_header(log, logtype)
            hand = win32evtlog.OpenEventLog(server, logtype)
            log_and_process_events(hand, log, flags, buffered_entries, buffer_size, logtype, format)
    except Exception as e:
        logging.error("Exception occurred:", exc_info=True)


def write_header(log, logtype):
    header = f"\nLog of {logtype} Events\nCreated: {time.ctime()}\n\n{'-' * 80}\n"
    log.write(header)


def log_and_process_events(hand, log, flags, buffered_entries, buffer_size, logtype, format):
    events = win32evtlog.ReadEventLog(hand, flags, 0)
    while events:
        for ev_obj in events:
            entry = format_event(ev_obj, logtype)
            buffered_entries.append(entry)
            if len(buffered_entries) >= buffer_size:
                if format == 'json':
                    buffered_entries = filter_events_by_time(buffered_entries)
                    send_data_to_api(buffered_entries)
                    buffered_entries = []
                else:
                    log.write('\n'.join(buffered_entries))
                    buffered_entries.clear()
        events = win32evtlog.ReadEventLog(hand, flags, 0)
    if buffered_entries:
        if format == 'json':
            buffered_entries = filter_events_by_time(buffered_entries)
            send_data_to_api(buffered_entries)
        else:
            log.write('\n'.join(buffered_entries))


def format_event(ev_obj, logtype):
    evt_id = str(winerror.HRESULT_CODE(ev_obj.EventID))
    evt_type = {
        win32con.EVENTLOG_AUDIT_FAILURE: 'EVENTLOG_AUDIT_FAILURE',
        win32con.EVENTLOG_AUDIT_SUCCESS: 'EVENTLOG_AUDIT_SUCCESS',
        win32con.EVENTLOG_INFORMATION_TYPE: 'EVENTLOG_INFORMATION_TYPE',
        win32con.EVENTLOG_WARNING_TYPE: 'EVENTLOG_WARNING_TYPE',
        win32con.EVENTLOG_ERROR_TYPE: 'EVENTLOG_ERROR_TYPE'
    }.get(ev_obj.EventType, "unknown")
    record = ev_obj.RecordNumber
    msg = win32evtlogutil.SafeFormatMessage(ev_obj, logtype)
    source = str(ev_obj.SourceName)
    entry = {
        "Event Date/Time": ev_obj.TimeGenerated.Format(),
        "Event ID / Type": f"{evt_id} / {evt_type}",
        "Record #": record,
        "Source": source,
        "Message": msg
    }
    return entry


def send_data_to_api(entries):
    token = os.getenv('TOKEN')
    url = os.getenv('URL')
    content = json.dumps(entries)
    data = {
        "machineId": os.getenv('MACHINE_ID'),
        "content": content
    }
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    if (len(data.get("content")) > 2):
        r = requests.post(url=url, data=json.dumps(data), headers=headers)


def filter_events_by_time(events, minutes=60):
    current_time = datetime.datetime.now()
    filtered_events = []
    for event in events:
        try:
            # Zmiana formatu na odpowiedni dla danych w logach
            event_time = datetime.datetime.strptime(event["Event Date/Time"], '%a %b %d %H:%M:%S %Y')
            if (current_time - event_time).total_seconds() / 60 <= minutes:
                filtered_events.append(event)
        except ValueError as e:
            logging.error(f"Error parsing date: {e}")
    return filtered_events


if __name__ == "__main__":
    server = None  # None = local machine
    logTypes = ["System", "Application", "Security", "Setup"]
    basePath = "./logtest"
    output_format = 'json'  # Could be 'txt' or 'json'
    getAllEvents(server, logTypes, basePath, output_format)
# This code allows the user to specify the output format ('txt' or 'json')
# when calling the function getAllEvents.
# The output format determines how the event logs are saved,
# either as plain text files or JSON files.