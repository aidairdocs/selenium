# E:\CRM\automation_project\steps_shared_utils\parse_ymd.py

def parse_ymd(date_str):
    """
    Given "YYYY-MM-DD", returns (YYYY, MM, DD) as integers.
    """
    parts = date_str.split("-")
    yyyy = int(parts[0])
    mm = int(parts[1])
    dd = int(parts[2])
    return (yyyy, mm, dd)

