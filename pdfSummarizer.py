# Install required libraries if not already installed
!pip install PyMuPDF
!pip install PyPDF2
!pip install torch
!pip install transformers
!pip install pytesseract

import PyPDF2
import fitz
from transformers import pipeline



def pdf_to_string(path):
  
  pdf_text_string = ''

  try:
    
    # Try opening with PyPDF2
    with open(path, 'rb') as f:
        pdf = PyPDF2.PdfReader(f)
        # Do something with the PDF opened by PyPDF2 extract
        for page_num in range(len(pdf.numPages)):
          # extract that page and append to string
          page_text = pdf.page[page_num].extract_text()
          pdf_text_string += page_text
        
  except PyPDF2.utils.PdfReadError:
    
    try:
      
      # Try opening with PyMuPDF (fitz)
      doc = fitz.open(path)
      # Do something with the PDF opened by PyMuPDF - add it to string
      for page in range(doc.page_count):
        # page is the page number
        # loaded_page = doc.load_page() # loads a Page

        try: 
          page = loaded_page.get_text() # if it doesnt work do ocr
          # that loads a Page object, now do Page.get_text()
          page_text = page.get_text()
          pdf_text_string += page_text
          
        except Exception as e:
          
          print(f"Regular text extraction failed for page {page_num + 1}. Using OCR.")
            
          try:
            ocr_text_page = loaded_page.get_textpage_ocr()
            page_text = ocr_text_page.extractText()
            pdf_text_string += page_text
          except Exception as e:
            print(f"OCR failed for page {page_num + 1}.")

          # now you have added that page to the pdf_text_string

        # now you have a page added to odf)text)string, exit for loop with a string full of all the pages. level of ocr exception
      # now you have finished the exception triggered by pupdf2 failing, you have the string or empty string. this is the for loop level
    # this is the try pymupdf level
    except Exception as e:
      print('Pymupdf failed')
  # this is the level of the pymupdf exception at this point both readers may have failed
  # print('Both PyPDF and PyMuPDF failed')
  return pdf_text_string
  



def summarize_long_string(pdf_text, summarizer, max_length):

  if len(pdf_text) >= max_length:

    # Divide text into chunks
    chunks = [pdf_text[i:i+max_length] for i in range(0, len(pdf_text), max_length)]
    # chunks is now a list of strings with a string for each chunk of length max_length
    
    chunk_summaries = {}
    for chunk_idx, chunk in enumerate(chunks):
      # Now summarize the chunk
      chunk_summary = summarizer(chunk, max_length=400, min_length=175, do_sample=False)
      # Store the summary in the chunk_summaries list using the chunk index
      chunk_summaries[chunk_idx] = chunk_summary
    
    # now chunk_summaries is full, concatenate it 
    concatenated_summary = " ".join([chunk_summary[chunk_idx] for chunk_idx in enumerate(chunk_summaries)])
    
    # now feed it back in to check if its reached a final length
    if (len(concatenated_summary) >= max_length):
      # the summary is still longer than the max_length, feed back in it can still be summarized. otherwise, it is done being summarized so return
      summarize_long_string(pdf_text=concatenated_summary, summarizer=summarizer, max_length=max_length)
    else:
      # print(f'Summary: {concatenated_summary}')
      return concatenated_summary
  else:
    return pdf_text

   
          




if __name__ == '__main__':
  
  DESIRED_FINAL_LENGTH = 1500 # about 300 words
  MODEL_MAX_LENGTH = 500000 # technically 100k tokens

  # read pdf into long string
  filename = ''
  filefolder = ''
  path = f'{filefolder}{filename}'
  long_string = pdf_to_string(path)

  # define summarizer
  summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
  # call the summarizing function on the long_string
  final_summary = summarize_long_string(pdf_text=long_string, summarizer=summarizer, max_length=DESIRED_FINAL_LENGTH)
  print(f'The PDF with filename {filename} \n was summmarized as follows: \n {final_summary}')
  print('Halt.')
  
  # further extensions should have the possibility to read multiple files? or you could just call it from elsewhere in a pipeline??
  

'''
MISCELLANEOUS NOTES

# assume input_string, max_length, summarizer type
While (len(input_pdf) >= max_seq_length:
   # divide the input_pdf into chunks of max length
   # for chunk in chunks: summarize the chunk, add it to the string to to be returned back to 
   # summarize each chunk, add them all together into one long string
   # feed that string back into the summarize function
   # the beginning checks if len(input_text) >= max_seq_length
   # assuming that it is, we again divide into chunks
   # for chunk in chunks, summarize the chunk, add to the string
   # feedback into summarize function
   # checks if len(input_text) >= max_seq_length: this time it’s not triggered
   # the input_text has been summarized bc the text is no longer equal to or shorter than the max_seq_length





      # use bart in pytorch
      summarizer(chunk, min_length=10, max_length=max_length) # max_length is based on what? is it the  
      
  # do we need different max_lengths? it should be the maximum amount of tokens or characters the summarizer can handle right? or is it the max_length of the output? 

  
  # Summarize each chunk
  summaries = [summarize_pdf(chunk) for chunk in chunks]  


  # you have the long string, the summarizer, and its max_length
  # the 


  
  if len(pdf_text) <= max_length:
    return summarizer(pdf_text)[0]['summary_text']
  
  # Divide text into chunks
  chunks = [pdf_text[i:i+max_length] for i in range(0, len(pdf_text), max_length)]
  
  # Summarize each chunk
  summaries = [summarize_pdf(chunk) for chunk in chunks]
  
  # Join chunk summaries together
  pdf_summary = " ".join(summaries)
  
  # Recursively summarize joined summary if still too long
  if len(pdf_summary) > max_length:
    return summarize_pdf(pdf_summary)
  else:
    return pdf_summary


'''
  
