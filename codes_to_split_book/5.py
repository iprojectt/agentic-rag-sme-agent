import os
import pypdf # Make sure you have installed pypdf: pip install pypdf

# ==============================================================================
# --- CONFIGURE YOUR BOOK HERE ---
# ==============================================================================

# 1. The name of the PDF file you want to split.
INPUT_PDF_FILE = "Eat_That_Frog.pdf"

# 2. The folder where the chapter PDFs will be saved.
OUTPUT_FOLDER = "data_for_finetuning_eat_frog"

# 3. Define the chapters with their start and end page numbers.
#    - The "key" will be the output filename.
#    - The "value" is a tuple (start_page, end_page).
#    - IMPORTANT: Use the page numbers you SEE in your PDF reader.
CHAPTERS = {
    "etf_preface": (4, 9),
    "etf_introduction_Eat_That_Frog": (10, 16),
    "etf_ch01_Set_the_Table": (17, 22),
    "etf_ch02_Plan_Every_Day_In_Advance": (23, 28),
    "etf_ch03_Apply_the_80-20_Rule": (29, 32),
    "etf_ch04_Consider_the_Consequences": (33, 41),
    "etf_ch05_Practice_Creative_Procrastination": (42, 45),
    "etf_ch06_Use_the_ABCDE_Method": (46, 49),
    "etf_ch07_Focus_on_Key_Result_Areas": (50, 55),
    "etf_ch08_The_Law_of_Three": (56, 64),
    "etf_ch09_Prepare_Thoroughly": (65, 69),
    "etf_ch10_Take_It_One_Oil_Barrel_at_a_Time": (70, 72),
    "etf_ch11_Upgrade_Your_Key_Skills": (73, 76),
    "etf_ch12_Leverage_Your_Special_Talents": (77, 79),
    "etf_ch13_Identify_Your_Key_Constraints": (80, 84),
    "etf_ch14_Put_the_Pressure_on_Yourself": (85, 87),
    "etf_ch15_Maximize_Your_Personal_Power": (88, 92),
    "etf_ch16_Motivate_Yourself_into_Action": (93, 96),
    "etf_ch17_Get_Out_of_Technological_Time_Sinks": (97, 104),
    "etf_ch18_Slice_and_Dice_the_Task": (105, 108),
    "etf_ch19_Create_Large_Chunks_of_Time": (109, 112),
    "etf_ch20_Develop_a_Sense_of_Urgency": (113, 116),
    "etf_ch21_Single_Handle_Every_Task": (117, 120),
    "etf_conclusion_Putting_It_All_Together": (121, 124),
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