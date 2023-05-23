import os
import re
import fitz

# convert string filename to int version of numerical portion only so sorting works as desired with parents being directly ahead of respective children
def convert_to_int(entry):
  # string non-number characters
  digits_file_name = entry[7:-4]
  # remove all punctuation
  digits_no_punc_file_name = re.sub(r'[^\w\s]', '', digits_file_name)
  # pad with 0 on right side to account for different lengths of numerical portions of file name to keep parents as a bigger number than children
  digits_no_punc_file_name_32 = digits_no_punc_file_name.ljust(32, "0")
  # convert to int for sorting
  int_digits_no_punc_file_name_32 = int(digits_no_punc_file_name_32)
  return int_digits_no_punc_file_name_32
 
# takes final sorted array and retrieves corresponding original filename associated with each 32-digit numerical entry in sorted order and creates array with original file names in sorted order 
def final_order(numerical_version, numerical_dict):
  final_order = []
  for item in numerical_version:
    curr_item_path = numerical_dict[item]
    final_order.append(curr_item_path)
  return final_order

# gets array of string filenames in a given family, passes them to helper function to convert to numerical versions and sort, receives final sorted array of original file names  
def sort_family(arr):
  numerical_dict = {}
  numerical_version = []
  for item in arr:
    converted_item = convert_to_int(item)
    
    numerical_version.append(converted_item)
    numerical_dict[converted_item] = item
  numerical_version.sort()
  return final_order(numerical_version, numerical_dict)

# def get_filenames():
#Create a list with the file paths
source_path = "/Users/sarahwelsh/Developer/pdf_combination/PDFs/"
dest_path = "/Users/sarahwelsh/Developer/pdf_combination/combined_families/"
filenames = os.listdir(source_path)

while len(filenames) > 0:
  temp_prefix = filenames[0]
  prefix = temp_prefix[:18]
  pdf_filepaths = []
  remove = []

  filenames.sort()

  for filename in filenames:
    if filename[0] == ".":
      remove.append(filename)
    elif prefix == filename[:18]:
      pdf_filepaths.append(filename)
      remove.append(filename)
  pdf_filepaths.reverse()

  if len(pdf_filepaths) > 2:
    pdf_filepaths = sort_family(pdf_filepaths)
    
  for item in remove:
    filenames.remove(item)

  final = fitz.open()      
      
  # Iterate over the list of the file paths
  for pdf_filepath in pdf_filepaths:
    full_filepath = f"{source_path}/{pdf_filepath}"
    with fitz.open(full_filepath) as mfile:
      final.insert_pdf(mfile)
      
  #Write out the merged PDF file
  final.save(f"{dest_path}{prefix}.pdf")
  print("done")
  

