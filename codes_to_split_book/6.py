import os
import pypdf # Make sure you have installed pypdf: pip install pypdf

# ==============================================================================
# --- CONFIGURE YOUR BOOK HERE ---
# ==============================================================================

# 1. The name of the PDF file you want to split.
INPUT_PDF_FILE = "Deep Work _ Rules for Focused Success in a Distracted World -- Newport, Cal.pdf"

# 2. The folder where the chapter PDFs will be saved.
OUTPUT_FOLDER = "data_for_finetuning_deep_work-1"

# 3. Define the chapters with their start and end page numbers.
#    - The "key" will be the output filename.
#    - The "value" is a tuple (start_page, end_page).
#    - IMPORTANT: Use the page numbers you SEE in your PDF reader.
CHAPTERS = {
    "dw_introduction": (5, 48),
    "dw_part1_ch01_Deep_Work_Is_Valuable": (50, 119),
    "dw_part1_ch02_Deep_Work_Is_Rare": (120, 177),
    "dw_part1_ch03_Deep_Work_Is_Meaningful": (178, 231),
    "dw_part2_rule01_Work_Deeply": (233, 387),
    "dw_part2_rule02_Embrace_Boredom": (388, 453),
    "dw_part2_rule03_Quit_Social_Media": (454, 539),
    "dw_part2_rule04_Drain_the_Shallows": (540, 645),
    "dw_conclusion": (646, 663),
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