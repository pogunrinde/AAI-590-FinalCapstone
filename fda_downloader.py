# FDA Document PDF Downloader and Text Extractor
# Simple pipeline to download PDFs and extract text

# Delay between document downloads (in seconds)
DOWNLOAD_DELAY = .5

# Setup and Imports

# Install required libraries
# pip install -q pandas requests PyPDF2 pdfplumber pymupdf

# Import libraries
import pandas as pd
import requests
import re
import json
import os
from pathlib import Path
from datetime import datetime

# Document processing
import PyPDF2

print("All libraries imported successfully!")


# Document Downloader Class


class FDADocumentProcessor:
    def __init__(self, pdf_dir="./fda_output/raw", text_dir="./fda_output/text"):
        self.documents = []
        self.pdf_dir = pdf_dir
        self.text_dir = text_dir
        # Create both directories if they don't exist
        os.makedirs(pdf_dir, exist_ok=True)
        os.makedirs(text_dir, exist_ok=True)
        
    def parse_csv_links(self, csv_content):
        """Parse CSV content and extract markdown links from the second column (PDF URLs)"""
        import io
        df = pd.read_csv(io.StringIO(csv_content))
        
        links_data = []
        markdown_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        
        # Check if we have at least 2 columns
        if len(df.columns) < 2:
            print("Warning: CSV has fewer than 2 columns, cannot extract PDF URLs from second column")
            return links_data
        
        for row_idx, row in df.iterrows():
            # Get the second column (index 1) for PDF URLs
            pdf_cell_value = row.iloc[1] if len(row) > 1 else None
            
            if pd.isna(pdf_cell_value):
                continue
            
            # Extract markdown links from the second column
            matches = re.findall(markdown_pattern, str(pdf_cell_value))
            
            for link_text, link_url in matches:
                link_data = {
                    'row_index': row_idx,
                    'column_name': df.columns[1] if len(df.columns) > 1 else 'col_1',
                    'link_text': link_text.strip(),
                    'link_url': link_url.strip(),
                    'context': str(pdf_cell_value)
                }
                links_data.append(link_data)
        
        return links_data
    
    def save_pdf_file(self, pdf_content, filename, doc_title):
        """Save downloaded PDF to file"""
        try:
            # Clean filename
            safe_filename = re.sub(r'[^\w\s-]', '', filename).strip()
            safe_filename = re.sub(r'[-\s]+', '-', safe_filename)
            
            # Add timestamp to avoid conflicts
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_filename = f"{safe_filename}_{timestamp}.pdf"
            pdf_path = os.path.join(self.pdf_dir, pdf_filename)
            
            with open(pdf_path, 'wb') as f:
                f.write(pdf_content)
            
            return pdf_path
        except Exception as e:
            print(f"Error saving PDF file: {e}")
            return None
    
    def extract_text_from_content(self, pdf_content):
        """Extract text from PDF content"""
        try:
            # Try PyPDF2 first
            try:
                import io
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
                text = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    try:
                        page = pdf_reader.pages[page_num]
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    except Exception as page_error:
                        print(f"Error extracting page {page_num}: {page_error}")
                        continue
                
                if text.strip():
                    return text
                    
            except Exception as pdf_error:
                print(f"PyPDF2 failed: {pdf_error}")
            
            # Try alternative methods with content
            try:
                import pdfplumber
                import io
                with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
                    text = ""
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    if text.strip():
                        return text
            except ImportError:
                print("pdfplumber not available, trying PyMuPDF")
            except Exception as plumber_error:
                print(f"pdfplumber failed: {plumber_error}")
            
            # Try PyMuPDF (fitz) as another alternative
            try:
                import fitz  # PyMuPDF
                doc = fitz.open(stream=pdf_content, filetype="pdf")
                text = ""
                for page_num in range(doc.page_count):
                    page = doc[page_num]
                    page_text = page.get_text()
                    if page_text:
                        text += page_text + "\n"
                doc.close()
                if text.strip():
                    return text
            except ImportError:
                print("PyMuPDF not available")
            except Exception as fitz_error:
                print(f"PyMuPDF failed: {fitz_error}")
            
            return ""
            
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
            return ""
    
    def download_document(self, url, filename):
        """Download a single document with improved headers and error handling"""
        try:
            # Create session with realistic headers
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0'
            })
            
            # Add delay to be respectful
            import time
            time.sleep(DOWNLOAD_DELAY)
            
            response = session.get(url, timeout=30, allow_redirects=True)
            
            # Check if we got redirected to abuse detection
            if 'abuse-detection' in response.url or 'apology' in response.url:
                print(f"Blocked by FDA abuse detection: {response.url}")
                return None, None
            
            # Check if response is actually a document
            content_type = response.headers.get('content-type', '').lower()
            if 'text/html' in content_type and 'pdf' not in url.lower():
                print(f"Got HTML instead of document: {content_type}")
                return None, None
            
            response.raise_for_status()
            
            # Return the PDF content instead of saving to temp file
            return response.content, response.headers.get('content-type', '')
            
        except requests.exceptions.RequestException as e:
            print(f"Request error downloading {url}: {e}")
            return None, None
        except Exception as e:
            print(f"General error downloading {url}: {e}")
            return None, None
    
    def extract_text_from_pdf(self, file_path):
        """Extract text from PDF file with better error handling"""
        try:
            with open(file_path, 'rb') as file:
                # Try PyPDF2 first
                try:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    
                    for page_num in range(len(pdf_reader.pages)):
                        try:
                            page = pdf_reader.pages[page_num]
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                        except Exception as page_error:
                            print(f"Error extracting page {page_num}: {page_error}")
                            continue
                    
                    if text.strip():
                        return text
                        
                except Exception as pdf_error:
                    print(f"PyPDF2 failed: {pdf_error}")
                
                # Try alternative PDF extraction methods
                try:
                    # Try pdfplumber if available
                    import pdfplumber
                    with pdfplumber.open(file_path) as pdf:
                        text = ""
                        for page in pdf.pages:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                        if text.strip():
                            return text
                except ImportError:
                    print("pdfplumber not available, trying PyMuPDF")
                except Exception as plumber_error:
                    print(f"pdfplumber failed: {plumber_error}")
                
                # Try PyMuPDF (fitz) as another alternative
                try:
                    import fitz  # PyMuPDF
                    doc = fitz.open(file_path)
                    text = ""
                    for page_num in range(doc.page_count):
                        page = doc[page_num]
                        page_text = page.get_text()
                        if page_text:
                            text += page_text + "\n"
                    doc.close()
                    if text.strip():
                        return text
                except ImportError:
                    print("PyMuPDF not available, trying basic text extraction")
                except Exception as fitz_error:
                    print(f"PyMuPDF failed: {fitz_error}")
                
                # Last resort: try to extract any readable text
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        # Look for text patterns
                        import re
                        text_patterns = re.findall(r'[A-Za-z]{3,}', content)
                        if len(text_patterns) > 50:  # If we found enough text
                            return ' '.join(text_patterns)
                except:
                    pass
                
                return ""
                
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
            return ""
    
    def extract_text_from_file(self, file_path, content_type):
        """Extract text based on file type - PDF only for now"""
        if content_type == 'application/pdf' or file_path.endswith('.pdf'):
            return self.extract_text_from_pdf(file_path)
        else:
            # Try to read as plain text
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()
            except:
                return ""
    
    def save_text_to_file(self, text, filename, doc_title):
        """Save extracted text to a file"""
        try:
            # Clean filename
            safe_filename = re.sub(r'[^\w\s-]', '', filename).strip()
            safe_filename = re.sub(r'[-\s]+', '-', safe_filename)
            
            # Add timestamp to avoid conflicts
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{safe_filename}_{timestamp}.txt"
            output_path = os.path.join(self.output_dir, output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"Document Title: {doc_title}\n")
                f.write(f"Extracted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                f.write(text)
            
            return output_path
        except Exception as e:
            print(f"Error saving text to file: {e}")
            return None

print("FDADocumentProcessor class defined!")

# Main Processing Function

def process_fda_documents(csv_content, max_documents=50, pdf_dir="./fda_output/raw", text_dir="./fda_output/text", reprocess=False):
    """
    Main function to process FDA documents and extract text to files
    
    Args:
        csv_content: CSV content as string
        max_documents: Maximum number of documents to process
        pdf_dir: Directory to save downloaded PDF files
        text_dir: Directory to save extracted text files
        reprocess: If False, skip documents that already have PDF and text files
    """
    
    processor = FDADocumentProcessor(pdf_dir=pdf_dir, text_dir=text_dir)
    
    print("Parsing CSV links...")
    links_data = processor.parse_csv_links(csv_content)
    
    print(f"🔗 Found {len(links_data)} links")
    
    # Limit documents for processing
    if max_documents:
        links_data = links_data[:max_documents]
        print(f"Processing first {len(links_data)} documents")
    
    processed_documents = []
    failed_downloads = []
    
    for i, link_data in enumerate(links_data):
        print(f"\n\nProcessing document {i+1}/{len(links_data)}: {link_data['link_text']}")
        
        # Check if files already exist (when reprocess=False)
        if not reprocess:
            # Generate expected filenames based on link text
            safe_filename = re.sub(r'[^\w\s-]', '', link_data['link_text']).strip()
            safe_filename = re.sub(r'[-\s]+', '-', safe_filename)
            
            # Check for existing PDF and text files (look for any timestamp variation)
            existing_pdfs = [f for f in os.listdir(pdf_dir) if f.startswith(safe_filename) and f.endswith('.pdf')]
            existing_texts = [f for f in os.listdir(text_dir) if f.startswith(safe_filename) and f.endswith('.txt')]
            
            if existing_pdfs and existing_texts:
                print(f"Skipping - files already exist:")
                print(f"PDF: {existing_pdfs[0]}")
                print(f"Text: {existing_texts[0]}")
                continue
        
        # Try to find direct PDF links in the context
        direct_pdf_urls = []
        context = link_data['context']
        
        # Look for direct PDF download links
        pdf_patterns = [
            r'https://www\.fda\.gov/media/\d+/download',
            r'https://www\.fda\.gov/files/\d+/[^"]*\.pdf',
            r'https://[^"]*\.pdf',
            r'https://www\.fda\.gov/[^"]*\.pdf'
        ]
        
        for pattern in pdf_patterns:
            matches = re.findall(pattern, context)
            direct_pdf_urls.extend(matches)
        
        # Try original URL first, then direct PDF URLs
        urls_to_try = [link_data['link_url']] + direct_pdf_urls
        
        success = False
        for url_idx, url in enumerate(urls_to_try):
            if url_idx > 0:
                print(f"Trying alternative URL {url_idx}: {url}")
            
            filename = f"doc_{i}_{hash(url) % 10000}"
            print(f"Downloading PDF from: {url}")
            pdf_content, content_type = processor.download_document(url, filename)
            
            if pdf_content:
                print(f"PDF downloaded successfully ({len(pdf_content)} bytes)")
                # Save PDF file
                print(f"Saving PDF file...")
                pdf_path = processor.save_pdf_file(pdf_content, link_data['link_text'], link_data['link_text'])
                
                if pdf_path:
                    print(f"PDF saved to: {pdf_path}")
                    # Extract text from PDF content
                    print(f"Extracting text from PDF...")
                    text = processor.extract_text_from_content(pdf_content)
                    
                    if text and len(text) > 100:  # Only process if we got meaningful text
                        print(f"Text extracted successfully ({len(text)} characters)")
                        
                        # Save text file with matching name
                        print(f"Saving text file...")
                        text_filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".txt"
                        text_path = os.path.join(text_dir, text_filename)
                        
                        with open(text_path, 'w', encoding='utf-8') as f:
                            f.write(f"Document Title: {link_data['link_text']}\n")
                            f.write(f"Extracted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                            f.write("=" * 80 + "\n\n")
                            f.write(text)
                        
                        print(f"Text file saved to: {text_path}")
                        
                        # Create document record
                        doc_record = {
                            'id': i,
                            'title': link_data['link_text'],
                            'url': url,  # Use the successful URL
                            'original_url': link_data['link_url'],
                            'context': link_data['context'],
                            'column_name': link_data['column_name'],
                            'text_length': len(text),
                            'pdf_path': pdf_path,
                            'text_path': text_path,
                            'success': True
                        }
                        processed_documents.append(doc_record)
                        print(f"Document processing complete!")
                        print(f"PDF: {pdf_path}")
                        print(f"Text: {text_path}")
                        success = True
                        break
                    else:
                        print(f"Text extraction failed or insufficient text")
                else:
                    print(f"Failed to save PDF for: {link_data['link_text']}")
            else:
                print(f"Failed to download {url}")
        
        if not success:
            failed_downloads.append(link_data)
            print(f"All download attempts failed for: {link_data['link_text']}")
        
        # Add delay between documents to be respectful
        if i < len(links_data) - 1:
            import time
            time.sleep(DOWNLOAD_DELAY)  # Use constant delay between documents
    
    print(f"\nProcessing complete!")
    print(f"Successfully processed: {len(processed_documents)} documents")
    print(f"Failed downloads: {len(failed_downloads)} documents")
    print(f"PDF files saved to: {pdf_dir}")
    print(f"Text files saved to: {text_dir}")
    
    if failed_downloads:
        print(f"\nFailed downloads summary:")
        for failed in failed_downloads[:5]:  # Show first 5 failures
            print(f"  - {failed['link_text']}")
        if len(failed_downloads) > 5:
            print(f"  ... and {len(failed_downloads) - 5} more")
    
    # Save processing summary
    summary_path = os.path.join(text_dir, "processing_summary.json")
    with open(summary_path, 'w') as f:
        json.dump({
            'total_processed': len(processed_documents),
            'total_failed': len(failed_downloads),
            'processed_documents': processed_documents,
            'failed_downloads': failed_downloads
        }, f, indent=2, default=str)
    
    print(f"Processing summary saved to: {summary_path}")
    
    return processed_documents

print("Main processing function defined!")

# Usage Example

"""
# Set CSV file path:
csv_file_path = "/path/to/your/fda_documents.csv"

# Read the CSV file
with open(csv_file_path, 'r', encoding='utf-8') as file:
    csv_content = file.read()

# Process documents and extract text to files
processed_docs = process_fda_documents(csv_content, max_documents=10, output_dir="fda_extracted_texts")

# Check the results
print(f"\nSummary:")
print(f"Successfully processed: {len(processed_docs)} documents")
print(f"Text files saved in: fda_extracted_texts/")
print(f"Processing summary: fda_extracted_texts/processing_summary.json")

# List the extracted text files
import os
text_files = [f for f in os.listdir("fda_extracted_texts") if f.endswith('.txt')]
print(f"\nExtracted text files:")
for file in text_files[:5]:  # Show first 5 files
    print(f"  - {file}")
if len(text_files) > 5:
    print(f"  ... and {len(text_files) - 5} more files")
"""

# Quick start function for easy usage
def quick_start(csv_file_path, max_documents=10, base_folder="./fda_output", pdf_dir="raw", text_dir="text", reprocess=False):
    """
    Quick start function to process FDA documents from a CSV file
    
    Args:
        csv_file_path: Path to your CSV file containing FDA document links
        max_documents: Maximum number of documents to process (default: 10)
        pdf_dir: Directory to save downloaded PDF files (default: "./fda_output/raw")
        text_dir: Directory to save extracted text files (default: "./fda_output/text")
        reprocess: If False, skip documents that already have PDF and text files (default: False)
    """
    print(f"Starting FDA document processing...")
    print(f"CSV file: {csv_file_path}")
    print(f"Max documents: {max_documents}")
    print(f"PDF directory: {base_folder}/{pdf_dir}")
    print(f"Text directory: {base_folder}/{text_dir}")
    print(f"Reprocess existing files: {reprocess}")
    
    # Read the CSV file
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_content = file.read()
        print(f"CSV file loaded successfully")
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_file_path}")
        return None
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None
    
    # Process documents
    processed_docs = process_fda_documents(csv_content, max_documents, f"{base_folder}/{pdf_dir}", f"{base_folder}/{text_dir}", reprocess)
    
    return processed_docs

print("Quick start function defined!")

print("FDA Document PDF Downloader and Text Extractor Ready!")
print("Copy the cells above into your notebook or run directly")
print("Set your CSV file path and run the processing pipeline")
print("All extracted text will be saved as individual .txt files")
print("\nQuick usage:")
print("   processed_docs = quick_start('./fda_documents.csv', max_documents=1000)")

# Run the script if executed directly
if __name__ == "__main__":
    biologics_docs = quick_start('./fda_documents_Biologics.csv', base_folder="./fda_output/Biologics", max_documents=1000)
    drugs_docs = quick_start('./fda_documents_Drugs.csv', base_folder="./fda_output/Drugs", max_documents=1000)
    medical_devices_docs = quick_start('./fda_documents_MedicalDevices.csv', base_folder="./fda_output/MedicalDevices", max_documents=1000)
