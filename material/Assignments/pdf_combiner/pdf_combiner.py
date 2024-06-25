import os
import subprocess
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

# Function to convert a notebook to PDF using nbconvert command line
def convert_notebook_to_pdf(notebook_path, output_pdf_path):
    output_name, _ = os.path.splitext(output_pdf_path)  # Remove the file extension from the output path
    subprocess.run([
        "jupyter", "nbconvert", "--to", "pdf", notebook_path, "--output", output_name
    ])

# Function to merge two PDFs
def merge_pdfs(pdf1_path, pdf2_path, output_pdf_path):
    merger = PdfMerger()
    merger.append(pdf1_path)
    merger.append(pdf2_path)
    merger.write(output_pdf_path)
    merger.close()

# Function to copy a PDF
def copy_pdf(source_pdf_path, output_pdf_path):
    reader = PdfReader(source_pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    with open(output_pdf_path, 'wb') as output_pdf:
        writer.write(output_pdf)

# Main script
def main():
    folder_path = '..'  # Change this to your folder path
    assignments = set()
    
    # Identify all assignments
    for filename in os.listdir(folder_path):
        if filename.endswith('_Assignment.ipynb'):
            assignment_name = filename.replace('_Assignment.ipynb', '')
            assignments.add(assignment_name)
    
    for assignment in assignments:
        assignment_notebook = os.path.join(folder_path, f'{assignment}_Assignment.ipynb')
        refsol_notebook = os.path.join(folder_path, f'{assignment}_RefSol.ipynb')
        
        assignment_pdf = os.path.join(folder_path, f'{assignment}_Assignment.pdf')
        refsol_pdf = os.path.join(folder_path, f'{assignment}_RefSol.pdf')
        combined_pdf = os.path.join(folder_path, f'{assignment}_Combined.pdf')
        
        # Convert the assignment notebook to PDF
        convert_notebook_to_pdf(assignment_notebook, assignment_pdf)
        
        if os.path.exists(refsol_notebook):
            # Convert the reference solution notebook to PDF
            convert_notebook_to_pdf(refsol_notebook, refsol_pdf)
            
            # Merge the PDFs
            merge_pdfs(assignment_pdf, refsol_pdf, combined_pdf)
            
            # Optionally, clean up the individual PDFs
            os.remove(assignment_pdf)
            os.remove(refsol_pdf)
        else:
            # Copy the assignment PDF to the combined PDF output
            copy_pdf(assignment_pdf, combined_pdf)
            
            # Optionally, clean up the individual PDF
            os.remove(assignment_pdf)

if __name__ == '__main__':
    main()
