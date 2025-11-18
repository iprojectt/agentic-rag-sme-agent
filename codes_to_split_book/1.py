# split_book.py
# This script splits a single PDF of a book into multiple PDFs, one for each chapter.
# It uses the pypdf library, which must be installed (`pip install pypdf`).

import pypdf
import os

# --- STEP 1: CONFIGURE YOUR BOOK AND OUTPUT ---

# The exact filename of the source book PDF.
# Place this file in the same directory as this script.
INPUT_PDF_FILE = "atomic_habits_source.pdf"

# The folder where the generated chapter PDFs will be saved.
# This will be created automatically if it doesn't exist.
OUTPUT_FOLDER = "data_for_finetuning"

# --- STEP 2: DEFINE THE CHAPTERS AND THEIR PAGE RANGES ---

# This dictionary contains the desired filename for each chapter and its (start, end) page numbers.
# The page numbers are the numbers you see in your PDF reader.
# I have meticulously found these page numbers for "Atomic Habits" from the provided PDF.
chapters = {
    "Introduction_My_Story": (9, 18),
    "ch01_The_Surprising_Power_of_Atomic_Habits": (20, 35),
    "ch02_How_Your_Habits_Shape_Your_Identity": (36, 49),
    "ch03_How_to_Build_Better_Habits_in_4_Simple_Steps": (50, 62),
    "ch04_The_Man_Who_Didnt_Look_Right": (64, 72),
    "ch05_The_Best_Way_to_Start_a_New_Habit": (73, 84),
    "ch06_Motivation_Is_Overrated_Environment_Often_Matters_More": (85, 95),
    "ch07_The_Secret_to_Self-Control": (96, 101),
    "ch08_How_to_Make_a_Habit_Irresistible": (103, 115),
    "ch09_The_Role_of_Family_and_Friends_in_Shaping_Your_Habits": (116, 126),
    "ch10_How_to_Find_and_Fix_the_Causes_of_Your_Bad_Habits": (127, 137),
    "ch11_Walk_Slowly_but_Never_Backward": (139, 145),
    "ch12_The_Law_of_Least_Effort": (146, 155),
    "ch13_How_to_Stop_Procrastinating_by_Using_the_Two-Minute_Rule": (156, 164),
    "ch14_How_to_Make_Good_Habits_Inevitable_and_Bad_Habits_Impossible": (165, 173),
    "ch15_The_Cardinal_Rule_of_Behavior_Change": (175, 185),
    "ch16_How_to_Stick_with_Good_Habits_Every_Day": (186, 195),
    "ch17_How_an_Accountability_Partner_Can_Change_Everything": (196, 203),
    "ch18_The_Truth_About_Talent": (205, 216),
    "ch19_The_Goldilocks_Rule": (217, 225),
    "ch20_The_Downside_of_Creating_Good_Habits": (226, 237),
    "Conclusion_The_Secret_to_Results_That_Last": (238, 240)
}

# --- STEP 3: SCRIPT LOGIC (NO NEED TO EDIT BELOW) ---

def split_pdf_into_chapters():
    """
    Reads the input PDF, loops through the chapter definitions,
    and creates a separate PDF for each chapter.
    """
    # Create the output folder if it doesn't already exist
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    try:
        # Open the source PDF file in binary read mode
        with open(INPUT_PDF_FILE, "rb") as file:
            reader = pypdf.PdfReader(file)
            
            print(f"--> Starting to split '{INPUT_PDF_FILE}' into {len(chapters)} chapters...")
            
            # Loop through each chapter defined in the dictionary
            for chapter_name, page_range in chapters.items():
                writer = pypdf.PdfWriter()
                start_page, end_page = page_range
                
                print(f"    -> Processing '{chapter_name}' (Pages {start_page}-{end_page})")
                
                # Add all pages within the specified range to the new PDF writer.
                # The script subtracts 1 because pypdf uses a 0-based index for pages.
                for page_num in range(start_page - 1, end_page):
                    writer.add_page(reader.pages[page_num])
                
                # Construct the full output path and filename
                output_filename = os.path.join(OUTPUT_FOLDER, f"{chapter_name}.pdf")
                
                # Write the new, single-chapter PDF to a file
                with open(output_filename, "wb") as output_pdf:
                    writer.write(output_pdf)

            print(f"\n--> Splitting complete! All files are saved in the '{OUTPUT_FOLDER}' directory.")

    except FileNotFoundError:
        print(f"--> ERROR: The file '{INPUT_PDF_FILE}' was not found.")
        print("    Please make sure it's in the same folder as this script and the name matches exactly.")
    except Exception as e:
        print(f"--> An unexpected error occurred: {e}")

# This ensures the script runs when you execute it from the command line
if __name__ == "__main__":
    split_pdf_into_chapters()