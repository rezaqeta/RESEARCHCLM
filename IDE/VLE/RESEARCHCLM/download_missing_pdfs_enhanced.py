import pandas as pd
import requests
import os
import time
import re
from pathlib import Path
from urllib.parse import quote, urlparse, urljoin
import json
from bs4 import BeautifulSoup

# Configuration
PDFS_FOLDER = Path("sources/metadata/pdfs")
PDFS_FOLDER.mkdir(parents=True, exist_ok=True)

def clean_filename(title):
    """Clean title to create valid filename"""
    filename = re.sub(r'[<>:"/\\|?*]', '', title)
    filename = re.sub(r'[\s\-]+', '-', filename)
    filename = filename[:150]
    filename = filename.strip('-')
    return filename.lower()

def extract_doi_from_url(url):
    """Extract DOI from URL"""
    if not url:
        return None
    doi_patterns = [
        r'doi\.org/(10\.\d+/[^\s]+)',
        r'doi/(10\.\d+/[^\s]+)',
        r'(10\.\d+/[^\s]+)'
    ]
    for pattern in doi_patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1).rstrip('.,;')
    return None

def try_pmc_download(link):
    """Try to download from PMC (PubMed Central)"""
    if 'pmc.ncbi.nlm.nih.gov' in link or 'pubmed' in link:
        try:
            # Extract PMC ID
            pmc_match = re.search(r'PMC(\d+)', link)
            if pmc_match:
                pmc_id = pmc_match.group(1)
                pdf_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/pdf/"
                
                response = requests.get(pdf_url, timeout=20, allow_redirects=True,
                                      headers={'User-Agent': 'Mozilla/5.0'})
                
                if response.status_code == 200 and response.content[:4] == b'%PDF':
                    return response.content
                
                # Try alternative URL
                pdf_url2 = f"https://europepmc.org/articles/PMC{pmc_id}?pdf=render"
                response = requests.get(pdf_url2, timeout=20, allow_redirects=True,
                                      headers={'User-Agent': 'Mozilla/5.0'})
                
                if response.status_code == 200 and response.content[:4] == b'%PDF':
                    return response.content
        except Exception as e:
            pass
    return None

def try_arxiv_download(link):
    """Try to download from arXiv"""
    if 'arxiv.org' in link:
        try:
            arxiv_id = re.search(r'(\d+\.\d+)', link)
            if arxiv_id:
                pdf_url = f"https://arxiv.org/pdf/{arxiv_id.group(1)}.pdf"
                response = requests.get(pdf_url, timeout=20,
                                      headers={'User-Agent': 'Mozilla/5.0'})
                if response.status_code == 200 and response.content[:4] == b'%PDF':
                    return response.content
        except:
            pass
    return None

def try_unpaywall(doi):
    """Try Unpaywall API"""
    if not doi:
        return None
    try:
        url = f"https://api.unpaywall.org/v2/{doi}"
        params = {'email': 'research@example.com'}
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('best_oa_location') and data['best_oa_location'].get('url_for_pdf'):
                pdf_url = data['best_oa_location']['url_for_pdf']
                return download_pdf_content(pdf_url)
    except Exception as e:
        pass
    return None

def try_semantic_scholar(title):
    """Search using Semantic Scholar API"""
    try:
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            'query': title,
            'limit': 3,
            'fields': 'title,url,openAccessPdf,externalIds'
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                for paper in data['data']:
                    # Try open access PDF
                    if paper.get('openAccessPdf') and paper['openAccessPdf'].get('url'):
                        pdf_url = paper['openAccessPdf']['url']
                        content = download_pdf_content(pdf_url)
                        if content:
                            return content
                    
                    # Try DOI via Unpaywall
                    if paper.get('externalIds') and paper['externalIds'].get('DOI'):
                        doi = paper['externalIds']['DOI']
                        content = try_unpaywall(doi)
                        if content:
                            return content
    except Exception as e:
        pass
    return None

def try_core_api(title):
    """Try CORE API for open access papers"""
    try:
        url = "https://core.ac.uk/api-v2/search/"
        params = {
            'q': title,
            'pageSize': 3,
            'apiKey': 'DEMO-API-KEY'  # Use demo key
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                for paper in data['data']:
                    if paper.get('downloadUrl'):
                        content = download_pdf_content(paper['downloadUrl'])
                        if content:
                            return content
    except:
        pass
    return None

def download_pdf_content(url):
    """Download PDF content from URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
        
        if response.status_code == 200:
            if response.content[:4] == b'%PDF' or 'application/pdf' in response.headers.get('content-type', ''):
                return response.content
    except:
        pass
    return None

def try_download_from_link(link):
    """Try multiple strategies to download from link"""
    if not link or pd.isna(link):
        return None
    
    # Strategy 1: Try PMC
    content = try_pmc_download(link)
    if content:
        return content
    
    # Strategy 2: Try arXiv
    content = try_arxiv_download(link)
    if content:
        return content
    
    # Strategy 3: Try direct link
    content = download_pdf_content(link)
    if content:
        return content
    
    # Strategy 4: Try DOI via Unpaywall
    doi = extract_doi_from_url(link)
    if doi:
        content = try_unpaywall(doi)
        if content:
            return content
    
    # Strategy 5: Try variations of the link
    variations = []
    
    if 'sciencedirect.com' in link:
        variations.append(link.replace('/abs/', '/pdfExtended/'))
        variations.append(link.replace('/article/', '/pdf/'))
    
    if 'springer.com' in link:
        variations.append(link.replace('/article/', '/content/pdf/') + '.pdf')
    
    if 'nature.com' in link:
        variations.append(link + '.pdf')
    
    if 'tandfonline.com' in link:
        variations.append(link.replace('/full/', '/pdf/'))
    
    if 'sagepub.com' in link:
        variations.append(link.replace('/doi/', '/doi/pdf/'))
    
    if 'oup.com' in link:
        variations.append(link.replace('/article/', '/article-pdf/'))
    
    if 'apa.org' in link:
        # Link already ends in .pdf sometimes
        content = download_pdf_content(link)
        if content:
            return content
    
    for var_link in variations:
        content = download_pdf_content(var_link)
        if content:
            return content
    
    return None

def process_paper(row, idx, df):
    """Process a single paper"""
    paper_no = row.get('No', idx)
    title = row.get('Paper Title', '')
    link = row.get('Link', '')
    org = row.get('Organization', '')
    
    print(f"\n[{paper_no}] {title[:80]}...")
    
    # Create filename
    filename = clean_filename(title) + '.pdf'
    filepath = PDFS_FOLDER / filename
    
    # Check if already downloaded
    if filepath.exists():
        print(f"    ✓ Already exists")
        df.loc[idx, 'PDF Available'] = 'Yes'
        return True
    
    # Try different methods
    pdf_content = None
    
    print(f"    Trying direct download from link...")
    pdf_content = try_download_from_link(link)
    
    if not pdf_content:
        print(f"    Trying Semantic Scholar...")
        pdf_content = try_semantic_scholar(title)
    
    if not pdf_content:
        print(f"    Trying CORE API...")
        pdf_content = try_core_api(title)
    
    if pdf_content:
        try:
            with open(filepath, 'wb') as f:
                f.write(pdf_content)
            print(f"    ✓ Downloaded: {filename}")
            df.loc[idx, 'PDF Available'] = 'Yes'
            return True
        except Exception as e:
            print(f"    ✗ Error saving: {e}")
    else:
        print(f"    ✗ Could not download")
        print(f"       Search: https://www.google.com/search?q={quote(title + ' filetype:pdf')}")
    
    return False

def process_excel_file(excel_path, start_index=0):
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
    
    if start_index > 0:
        no_pdf_df = no_pdf_df.iloc[start_index:]
        print(f"Starting from index {start_index}, remaining: {len(no_pdf_df)}")
    
    downloaded_count = 0
    failed_count = 0
    
    for count, (idx, row) in enumerate(no_pdf_df.iterrows(), 1):
        success = process_paper(row, idx, df)
        
        if success:
            downloaded_count += 1
        else:
            failed_count += 1
        
        # Be nice to servers
        time.sleep(1)
        
        # Save progress every 5 papers
        if count % 5 == 0:
            print(f"\n    💾 Saving progress... ({downloaded_count} downloaded, {failed_count} failed)")
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
    print("🔍 Enhanced PDF Download Manager")
    print("=" * 80)
    
    total_downloaded = 0
    total_failed = 0
    
    # Process Climate_Behavioral_Change_Papers.xlsx - ALL papers
    print("\n" + "="*80)
    print("FILE 1: Climate_Behavioral_Change_Papers.xlsx")
    print("="*80)
    d1, f1 = process_excel_file('Climate_Behavioral_Change_Papers.xlsx')
    total_downloaded += d1
    total_failed += f1
    
    # Process source_main_cb.xlsx - ALL papers
    print("\n" + "="*80)
    print("FILE 2: source_main_cb.xlsx")
    print("="*80)
    d2, f2 = process_excel_file('source_main_cb.xlsx')
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



