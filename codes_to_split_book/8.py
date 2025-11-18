import os
import pypdf # Make sure you have installed pypdf: pip install pypdf

# ==============================================================================
# --- CONFIGURE YOUR BOOK HERE ---
# ==============================================================================

# 1. The name of the PDF file you want to split.
INPUT_PDF_FILE = "The Cirillo Pomodoro Technique.pdf"

# 2. The folder where the chapter PDFs will be saved.
OUTPUT_FOLDER = "data_for_finetuning_pomodoro"

# 3. Define the chapters with their start and end page numbers.
#    - The "key" will be the output filename.
#    - The "value" is a tuple (start_page, end_page).
#    - IMPORTANT: Use the page numbers you SEE in your PDF reader.
CHAPTERS = {
    "tpt_preface_and_introduction": (6, 9),
    "tpt_ch01_The_Context": (10, 11),
    "tpt_ch02_Material_and_Method": (12, 30),
    "tpt_ch03_Results": (31, 36),
    "tpt_ch04_Conclusions_and_Appendices": (37, 45),
}


# ==============================================================================
# --- SCRIPT LOGIC (No need to edit below this line) ---
# ==============================================================================

def split_pdf_into_chapters():
    """
    Splits the configured PDF into chapters based on the CHAPTERS dictionary.
    """
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    try:
        with open(INPUT_PDF_FILE, "rb") as file:
            reader = pypdf.PdfReader(file)
            total_pages = len(reader.pages)
            
            print(f"-> Starting to split '{INPUT_PDF_FILE}' which has {total_pages} pages.")
            
            for chapter_name, page_range in CHAPTERS.items():
                writer = pypdf.PdfWriter()
                start_page, end_page = page_range
                
                # Adjust for 0-based indexing for the range function
                start_index = start_page - 1
                end_index = end_page

                if start_page > end_page:
                    print(f"   - WARNING: Skipping '{chapter_name}' because start page ({start_page}) is after end page ({end_page}).")
                    continue
                if end_page > total_pages:
                    print(f"   - WARNING: For '{chapter_name}', end page ({end_page}) is greater than total pages ({total_pages}). Truncating.")
                    end_index = total_pages

                print(f"  -> Processing '{chapter_name}' (Pages {start_page}-{end_page})...")

                # Loop through the pages and add them to the writer
                for page_num in range(start_index, end_index):
                    if page_num < total_pages:
                        writer.add_page(reader.pages[page_num])
                
                output_filename = os.path.join(OUTPUT_FOLDER, f"{chapter_name}.pdf")
                
                with open(output_filename, "wb") as output_pdf:
                    writer.write(output_pdf)
                
            print("\n✅ Splitting complete! All chapter files have been saved.")

    except FileNotFoundError:
        print(f"❌ ERROR: The file '{INPUT_PDF_FILE}' was not found.")
        print("   Please make sure the PDF file is in the same directory as this script, or provide the full path.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    split_pdf_into_chapters()