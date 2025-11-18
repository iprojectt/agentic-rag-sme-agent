import os
import pypdf # Make sure you have installed pypdf: pip install pypdf

# ==============================================================================
# --- CONFIGURE YOUR BOOK HERE ---
# ==============================================================================

# 1. Set the path to the PDF file you want to split.
#    (Place the book PDF in the same directory as this script for simplicity)
INPUT_PDF_FILE = "Getting Things Done.pdf"

# 2. Set the folder where the chapter PDFs will be saved.
#    This should be the same as your project's data directory.
OUTPUT_FOLDER = "data_for_finetuning_book_GTD"

# 3. Define the chapters.
#    - The "key" (e.g., "gtd_ch01_A_New_Practice") will be the output filename.
#    - The "value" is a tuple (start_page, end_page).
#    - IMPORTANT: Use the page numbers you SEE in your PDF reader.
#      For example, if Chapter 1 starts on page 3 and ends on page 23, you write (3, 23).
CHAPTERS = {
    "gtd_welcome": (10, 13),
    "gtd_ch01_A_New_Practice": (16, 36),
    "gtd_ch02_Getting_Control_of_Your_Life": (37, 66),
    "gtd_ch03_Getting_Projects_Creatively_Under_Way": (67, 94),
    "gtd_ch04_Getting_Started": (96, 114),
    "gtd_ch05_Collection": (115, 129),
    "gtd_ch06_Processing": (130, 148),
    "gtd_ch07_Organizing": (149, 191),
    "gtd_ch08_Reviewing": (192, 210),
    "gtd_ch09_Doing": (211, 222),
    "gtd_ch10_Getting_Projects_Under_Control": (222, 233),
    "gtd_ch11_The_Power_of_the_Collection_Habit": (235, 245),
    "gtd_ch12_The_Power_of_the_Next-Action_Decision": (246, 258),
    "gtd_ch13_The_Power_of_Outcome_Focusing": (259, 266),
    "gtd_conclusion": (267, 269),
}

# ==============================================================================
# --- SCRIPT LOGIC (No need to edit below this line) ---
# ==============================================================================

def split_pdf_into_chapters():
    """
    Splits the configured PDF into chapters based on the CHAPTERS dictionary.
    """
    # Create the output folder if it doesn't exist to avoid errors.
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    try:
        # Open the source PDF file in binary read mode.
        with open(INPUT_PDF_FILE, "rb") as file:
            reader = pypdf.PdfReader(file)
            total_pages = len(reader.pages)
            
            print(f"-> Starting to split '{INPUT_PDF_FILE}' which has {total_pages} pages.")
            
            # Loop through each chapter defined in the configuration dictionary.
            for chapter_name, page_range in CHAPTERS.items():
                writer = pypdf.PdfWriter()
                start_page, end_page = page_range
                
                # Validate the page range to prevent errors.
                if start_page > end_page:
                    print(f"   - WARNING: Skipping '{chapter_name}' because start page ({start_page}) is after end page ({end_page}).")
                    continue
                if end_page > total_pages:
                    print(f"   - WARNING: For '{chapter_name}', end page ({end_page}) is greater than total pages ({total_pages}). Truncating.")
                    end_page = total_pages

                print(f"  -> Processing '{chapter_name}' (Pages {start_page}-{end_page})...")

                # Loop through the specified page range.
                # We subtract 1 because pypdf uses 0-based indexing.
                for page_num in range(start_page - 1, end_page):
                    writer.add_page(reader.pages[page_num])
                
                # Construct the full path for the output file.
                output_filename = os.path.join(OUTPUT_FOLDER, f"{chapter_name}.pdf")
                
                # Write the collected pages to a new PDF file.
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