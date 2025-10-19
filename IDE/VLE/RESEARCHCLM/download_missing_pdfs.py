import pandas as pd
import requests
import os
import time
import re
from pathlib import Path
from urllib.parse import quote, urlparse
import json

# Configuration
PDFS_FOLDER = Path("sources/metadata/pdfs")
PDFS_FOLDER.mkdir(parents=True, exist_ok=True)

def clean_filename(title):
    """Clean title to create valid filename"""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', title)
    # Replace spaces and special chars with hyphens
    filename = re.sub(r'[\s\-]+', '-', filename)
    # Limit length
    filename = filename[:150]
    # Remove trailing hyphens
    filename = filename.strip('-')
    return filename.lower()

def search_pdf_google_scholar(title, org=None):
    """Search for PDF using Google Scholar approach"""
    # Try to find PDF link from the paper link or title
    search_terms = [
        f"{title} filetype:pdf",
        f"{title} pdf",
    ]
    
    if org:
        search_terms.insert(0, f"{title} {org} filetype:pdf")
    
    return search_terms

def search_pdf_semantic_scholar(title):
    """Search using Semantic Scholar API"""
    try:
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            'query': title,
            'limit': 1,
            'fields': 'title,url,openAccessPdf'
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                paper = data['data'][0]
                if paper.get('openAccessPdf') and paper['openAccessPdf'].get('url'):
                    return paper['openAccessPdf']['url']
    except Exception as e:
        print(f"    Semantic Scholar error: {e}")
    return None

def search_pdf_unpaywall(title, doi=None):
    """Search using Unpaywall API"""
    if not doi:
        return None
    try:
        url = f"https://api.unpaywall.org/v2/{doi}"
        params = {'email': 'researcher@example.com'}
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('best_oa_location') and data['best_oa_location'].get('url_for_pdf'):
                return data['best_oa_location']['url_for_pdf']
    except Exception as e:
        print(f"    Unpaywall error: {e}")
    return None

def try_download_from_link(link):
    """Try to download PDF directly from the provided link"""
    if not link or pd.isna(link):
        return None
    
    try:
        # First, try the link as-is
        response = requests.get(link, timeout=15, allow_redirects=True, 
                              headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        
        # Check if it's a PDF
        content_type = response.headers.get('content-type', '')
        if 'application/pdf' in content_type or response.content[:4] == b'%PDF':
            return response.content
        
        # Try adding /download or .pdf
        variations = [
            f"{link}/download",
            f"{link}.pdf",
            link.replace('/abstract/', '/pdf/'),
            link.replace('/abs/', '/pdf/'),
        ]
        
        for var_link in variations:
            try:
                response = requests.get(var_link, timeout=15, allow_redirects=True,
                                      headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
                content_type = response.headers.get('content-type', '')
                if 'application/pdf' in content_type or response.content[:4] == b'%PDF':
                    return response.content
            except:
                continue
                
    except Exception as e:
        print(f"    Error downloading from link: {e}")
    
    return None

def download_pdf(url, filename):
    """Download PDF from URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
        
        if response.status_code == 200:
            # Check if it's actually a PDF
            if response.content[:4] == b'%PDF' or 'application/pdf' in response.headers.get('content-type', ''):
                filepath = PDFS_FOLDER / filename
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return True
        return False
    except Exception as e:
        print(f"    Download error: {e}")
        return False

def process_excel_file(excel_path, start_row=0, max_papers=None):
    """Process one Excel file and download missing PDFs"""
    print(f"\n{'='*80}")
    print(f"Processing: {excel_path}")
    print(f"{'='*80}\n")
    
    # Read Excel
    df = pd.read_excel(excel_path)
    
    # Find rows without PDF
    no_pdf_mask = df['PDF Available'].isin(['Not Available', 'No PDF', 'No'])
    no_pdf_df = df[no_pdf_mask].copy()
    
    print(f"Total rows: {len(df)}")
    print(f"Rows without PDF: {len(no_pdf_df)}")
    
    if start_row > 0:
        no_pdf_df = no_pdf_df.iloc[start_row:]
        print(f"Starting from row {start_row}, remaining: {len(no_pdf_df)}")
    
    if max_papers:
        no_pdf_df = no_pdf_df.head(max_papers)
        print(f"Processing first {max_papers} papers")
    
    downloaded_count = 0
    failed_count = 0
    
    for idx, row in no_pdf_df.iterrows():
        paper_no = row.get('No', idx)
        title = row.get('Paper Title', '')
        link = row.get('Link', '')
        org = row.get('Organization', '')
        
        print(f"\n[{paper_no}] {title[:80]}...")
        print(f"    Link: {link}")
        
        # Create filename
        filename = clean_filename(title) + '.pdf'
        filepath = PDFS_FOLDER / filename
        
        # Check if already downloaded
        if filepath.exists():
            print(f"    ✓ Already exists: {filename}")
            df.loc[idx, 'PDF Available'] = 'Yes'
            downloaded_count += 1
            continue
        
        # Try different methods to find and download PDF
        pdf_downloaded = False
        
        # Method 1: Try direct download from provided link
        print(f"    Trying direct download from link...")
        pdf_content = try_download_from_link(link)
        if pdf_content:
            try:
                with open(filepath, 'wb') as f:
                    f.write(pdf_content)
                print(f"    ✓ Downloaded from direct link: {filename}")
                df.loc[idx, 'PDF Available'] = 'Yes'
                downloaded_count += 1
                pdf_downloaded = True
            except Exception as e:
                print(f"    ✗ Error saving: {e}")
        
        # Method 2: Try Semantic Scholar
        if not pdf_downloaded:
            print(f"    Trying Semantic Scholar...")
            pdf_url = search_pdf_semantic_scholar(title)
            if pdf_url:
                print(f"    Found URL: {pdf_url}")
                if download_pdf(pdf_url, filename):
                    print(f"    ✓ Downloaded via Semantic Scholar: {filename}")
                    df.loc[idx, 'PDF Available'] = 'Yes'
                    downloaded_count += 1
                    pdf_downloaded = True
        
        # Method 3: Manual search prompts (we'll print these for manual intervention)
        if not pdf_downloaded:
            print(f"    ✗ Could not auto-download")
            print(f"    → Manual search needed:")
            print(f"       Google: https://www.google.com/search?q={quote(title + ' filetype:pdf')}")
            print(f"       Google Scholar: https://scholar.google.com/scholar?q={quote(title)}")
            failed_count += 1
        
        # Be nice to servers
        time.sleep(2)
        
        # Save progress every 10 papers
        if (downloaded_count + failed_count) % 10 == 0:
            print(f"\n    💾 Saving progress...")
            df.to_excel(excel_path, index=False)
    
    # Final save
    print(f"\n{'='*80}")
    print(f"Final save...")
    df.to_excel(excel_path, index=False)
    
    print(f"\n📊 Summary for {excel_path}:")
    print(f"   ✓ Downloaded: {downloaded_count}")
    print(f"   ✗ Failed: {failed_count}")
    print(f"   Total processed: {downloaded_count + failed_count}")
    
    return downloaded_count, failed_count

def main():
    """Main function"""
    print("🔍 PDF Download Manager for Research Papers")
    print("=" * 80)
    
    # Process both Excel files
    total_downloaded = 0
    total_failed = 0
    
    # Process Climate_Behavioral_Change_Papers.xlsx
    d1, f1 = process_excel_file('Climate_Behavioral_Change_Papers.xlsx', max_papers=20)
    total_downloaded += d1
    total_failed += f1
    
    # Process source_main_cb.xlsx
    d2, f2 = process_excel_file('source_main_cb.xlsx', max_papers=20)
    total_downloaded += d2
    total_failed += f2
    
    print(f"\n{'='*80}")
    print(f"🎉 FINAL SUMMARY")
    print(f"{'='*80}")
    print(f"   ✓ Total Downloaded: {total_downloaded}")
    print(f"   ✗ Total Failed: {total_failed}")
    print(f"   📁 PDF folder: {PDFS_FOLDER.absolute()}")

if __name__ == "__main__":
    main()



