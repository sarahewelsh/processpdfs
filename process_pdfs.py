import pdf_combiner
import extract_date

source_path = "/Users/sarahwelsh/Developer/pdf_combination/PDFs/"
fam_dest_path = "/Users/sarahwelsh/Developer/pdf_combination/combined_families/"
final_dest_path = "/Users/sarahwelsh/Developer/pdf_combination/FINALS/"

pdf_combiner.combine_PDFs(source_path, fam_dest_path)
extract_date.extract_date(fam_dest_path, final_dest_path)