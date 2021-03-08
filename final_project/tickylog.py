#!/usr/bin/env python3
import re
import csv
import collections

def get_error_message_type(log):
    if re.search(r"ERROR", log):
        return "ERROR"
    if re.search(r"INFO", log):
        return "INFO"
        
def find_errors():
    error_dict = {}
    with open("syslog.log", "r") as logfile:        
        for line in logfile:
            if re.search(r"ERROR", line):
                print(line)
                print("FOUND AN ERROR")
                error_message = str(re.search(r"(ticky).*?\s*\(", line).group(0)).replace(" (", "").replace("ticky: ERROR ", "")
                if error_message not in error_dict:
                    error_dict[error_message] = 0
                error_dict[error_message] += 1 
            if re.search(r"INFO", line):
                pass

    return error_dict

def get_per_user_errors():
    per_user_errors = {}
    with open("syslog.log", "r") as logfile:
        for line in logfile:
            username = str(re.search(r"\(.*\)", line).group(0)).replace("(", "").replace(")", "")
            if username not in per_user_errors:
                per_user_errors[username] = {"INFO": 0, "ERROR": 0}
            per_user_errors[username][get_error_message_type(line)] +=1

    return per_user_errors

def write_per_user_dict_to_csv(d):    
    with open('user_statistics.csv','w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        header = ["Username", "INFO", "ERROR"]
        w.writerow(header)
        od = collections.OrderedDict(sorted(d.items()))
        for k, v in od.items():
            row = [k, v["INFO"], v["ERROR"]]
            w.writerow(row)

def write_error_dict_to_csv(d):
    with open("error_message.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        header = ["Error", "Count"]
        od = sorted(d.items(), key=lambda x: x[1], reverse=True)
        w.writerow(header)
        for row in od:
            w.writerow(row)

if __name__ == '__main__':
    different_error_messages_dict = find_errors()
    write_error_dict_to_csv(different_error_messages_dict)
    
    per_user_errors = get_per_user_errors()
    write_per_user_dict_to_csv(per_user_errors)
