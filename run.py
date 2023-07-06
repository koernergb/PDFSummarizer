import PyPDF2
from transformers import pipeline

# Load the summarization pipeline
summarizer = pipeline("summarization",  model="t5-base", tokenizer="t5-base", framework="tf")

# Open the PDF file in read-binary mode
with open('./pdfs/We_Are_Electric.pdf', 'rb') as file:
  # Create a PDF object
  pdf = PyPDF2.PdfReader(file)  
  # Get the number of pages in the PDF
  page = pdf.pages[6]
  text = page.extract_text()
  print(text)


# Summarize the text
summary = summarizer(text, max_length=100, min_length=30, do_sample=False)
# Print the summary
print(summary[0]["summary_text"])