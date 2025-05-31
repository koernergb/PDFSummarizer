# PDF Summarizer

A Python-based tool for extracting and summarizing text from PDF documents using state-of-the-art transformer models.

## Features

- PDF text extraction with fallback options:
  - Primary: PyPDF2
  - Secondary: PyMuPDF (with OCR capabilities)
- Text summarization using transformer models:
  - BART (facebook/bart-large-cnn)
  - Pegasus (google/pegasus-large) [optional]
  - T5 (t5-base) [optional]
- Handles long documents through chunking and recursive summarization
- Available as both a script and Jupyter notebook

## Requirements
python
transformers
torch
PyPDF2
PyMuPDF
sentencepiece
langchain
gradio # for future UI implementation

## Usage

### Google Colab (Recommended)
Use `pdfSummarizer02.ipynb` for GPU-accelerated summarization:
1. Upload your PDF to Google Drive
2. Mount your Google Drive
3. Run the notebook cells sequentially

## Configuration

- `DESIRED_FINAL_LENGTH`: Target length for final summary (default: 1500 characters)
- `MODEL_MAX_LENGTH`: Maximum input sequence length (default: 500000 characters)
- Adjustable chunk sizes for processing long documents

## Models

The project supports multiple summarization models:
- `facebook/bart-large-cnn` (default) - Optimized for news article summarization
- `google/pegasus-large` (optional) - Alternative model with strong abstractive capabilities
- `t5-base` (optional) - Lightweight alternative

## Notes

- GPU acceleration recommended for optimal performance
- Large documents are automatically chunked and recursively summarized
- OCR fallback available for scanned PDFs

## Future Improvements

- [ ] Add Gradio web interface
- [ ] Implement batch processing for multiple PDFs
- [ ] Add support for more document formats
- [ ] Improve error handling and logging