import os
import fitz
import fnmatch
import datetime

def add_padding(str):
  if len(str) != 2:
    result = str.rjust(2, "0")
    return result
  else:
    return str
    
# returns section of string partition
def partition(string, search_term, result_place):
  result = string.partition(search_term)[result_place]
  return result

# converts hour value from 12-hr to 24-hr value 
def convert_24_hr(hr, value):
  if value == "PM":
    result = int(hr) 
    result += 12
    return str(result)
  else:
    return hr

# calls partition helper function to break apart strings into datetime components, calls convert_to_int helper function to convert those values all to ints, creates datetime object. 
def format_date(cal_str, time_str):
  month = partition(cal_str, "/", 0)
  formatted_month = str(add_padding(month))
  remainder_date = partition(cal_str, "/", 2)
  day = partition(remainder_date,"/", 0)
  formatted_day = str(add_padding(day))
  year = partition(remainder_date,"/", 2)
  hour = partition(time_str, ":", 0)
  remainder_time = partition(time_str, ":", 2)
  minute = partition(remainder_time, ":", 0)
  remainder_time = partition(remainder_time, ":", 2)
  second = partition(remainder_time, " ", 0)
  am_pm = partition(remainder_time, " ", 2)
  trimmed_am_pm = am_pm[:2]
  hr_24 = convert_24_hr(hour, trimmed_am_pm)
  
  converted_date = year + formatted_month + formatted_day + "_" + hr_24 + "-" + minute + "-" + second
  return converted_date

# gets line with search result from extracted PDF text, breaks out just the calendar date and the time, removing the day of the week and any timezone 
def parse_date(date_str):
  cal_date = date_str.partition(" ")[2].partition(" ")[0]
  time = date_str.partition(" ")[2].partition(" ")[2]
  print(format_date(cal_date, time))
  return format_date(cal_date, time)
    
#Create a list with the file paths
source_path = "/Users/sarahwelsh/Developer/pdf_combination/combined_families"
dest_path = "/Users/sarahwelsh/Developer/pdf_combination/FINALS"
filenames = os.listdir(source_path)

for filename in filenames:
  # find and open each pdf files in the directory.  With each file, create a Document object and extract the text from page 1
  if fnmatch.fnmatch(filename, '*.pdf'):
    document = os.path.join(source_path, filename)
    current_doc = fitz.Document(document)
    page1 = current_doc.load_page(0)
    text = page1.get_text("text")
    
    # remove "Start Time" or "Sent" text to get just time/date information
    if "Start Time" in text:
      date1 = text.partition("Start Time")[2]
      date = date1.partition("(UTC)")[0]
      file_date = parse_date(date)
      current_doc.save(f"{dest_path}{file_date} {filename}")
      print("done")
      
    elif "Sent" in text:
      date1 = text.partition("Sent")[2]
      date = date1.partition("(UTC)")[0]
      # print(f"date {date}")
      file_date = parse_date(date)
      current_doc.save(f"{dest_path}{file_date} {filename}")
      print("done")
