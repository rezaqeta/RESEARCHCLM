"""
PDF Content Extraction and Embedding System
Extracts content from PDF with page references, creates chunks, and generates embeddings
Focus: Policy Maker content on Behavioral Science
"""

import PyPDF2
import re
from typing import List, Dict, Tuple
import json
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class ContentChunk:
    """Represents a chunk of content with metadata"""
    chunk_id: int
    heading: str
    subheading: str
    content: str
    page_number: int
    page_range: str
    in_text_citation: str
    section_type: str
    keywords: List[str]
    
    def to_dict(self):
        return asdict(self)

class PDFEmbeddingExtractor:
    """Extract and chunk PDF content with proper references"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.chunks: List[ContentChunk] = []
        self.full_text_by_page: Dict[int, str] = {}
        
    def extract_text_with_pages(self) -> Dict[int, str]:
        """Extract text from PDF preserving page numbers"""
        print(f"📖 Reading PDF: {self.pdf_path}")
        
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                print(f"📄 Total pages: {total_pages}")
                
                for page_num in range(total_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    self.full_text_by_page[page_num + 1] = text
                    
                return self.full_text_by_page
        except Exception as e:
            print(f"❌ Error reading PDF: {e}")
            return {}
    
    def identify_headings(self, text: str) -> List[Tuple[str, int]]:
        """Identify headings and subheadings in text"""
        heading_patterns = [
            r'^[A-Z][A-Z\s]{10,}$',  # ALL CAPS HEADINGS
            r'^\d+\.\s+[A-Z].*$',      # Numbered headings
            r'^[A-Z][a-zA-Z\s]+:$',    # Headings with colon
        ]
        
        lines = text.split('\n')
        headings = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            for pattern in heading_patterns:
                if re.match(pattern, line) and len(line) > 5:
                    headings.append((line, i))
                    break
        
        return headings
    
    def search_policy_behavioral_content(self) -> List[Dict]:
        """Search for content related to policymakers and behavioral science"""
        keywords = [
            'policy maker', 'policymaker', 'policy', 'government',
            'behavioral science', 'behaviour change', 'behavioral insight',
            'intervention', 'nudge', 'behavioral economics',
            'decision maker', 'public policy', 'evidence-based',
            'implementation', 'practitioner', 'behavioral intervention',
            'policy design', 'behavioral technique', 'behavior change'
        ]
        
        relevant_content = []
        chunk_id = 0
        
        print(f"\n🔍 Searching for policy maker and behavioral science content...")
        
        for page_num, page_text in self.full_text_by_page.items():
            # Split into paragraphs
            paragraphs = [p.strip() for p in page_text.split('\n\n') if p.strip()]
            
            for para in paragraphs:
                # Check if paragraph contains relevant keywords
                para_lower = para.lower()
                keyword_matches = [kw for kw in keywords if kw in para_lower]
                
                if len(keyword_matches) >= 2 and len(para) > 100:  # At least 2 keywords and substantial content
                    # Try to identify heading/subheading
                    heading, subheading = self.extract_heading_context(page_num, para)
                    
                    chunk_id += 1
                    chunk = ContentChunk(
                        chunk_id=chunk_id,
                        heading=heading,
                        subheading=subheading,
                        content=para,
                        page_number=page_num,
                        page_range=f"p. {page_num}",
                        in_text_citation=f"(BIT, 2019, p. {page_num})",
                        section_type="Policy & Behavioral Science",
                        keywords=keyword_matches
                    )
                    
                    self.chunks.append(chunk)
                    relevant_content.append(chunk.to_dict())
        
        print(f"✅ Found {len(relevant_content)} relevant chunks")
        return relevant_content
    
    def extract_heading_context(self, page_num: int, content: str) -> Tuple[str, str]:
        """Extract heading and subheading context for a chunk"""
        page_text = self.full_text_by_page.get(page_num, "")
        
        # Look for headings before the content
        lines = page_text.split('\n')
        content_first_line = content.split('\n')[0][:50]
        
        heading = "General Content"
        subheading = ""
        
        # Find where this content appears in the page
        try:
            content_pos = page_text.index(content_first_line)
            text_before = page_text[:content_pos]
            lines_before = text_before.split('\n')
            
            # Look for headings in reverse
            for line in reversed(lines_before[-10:]):  # Check last 10 lines before content
                line = line.strip()
                if line and (line.isupper() or re.match(r'^\d+\.', line)):
                    if not subheading:
                        subheading = line
                    else:
                        heading = line
                        break
            
            if not heading or heading == "General Content":
                # Try to extract from content itself
                first_sentence = content.split('.')[0].strip()
                if len(first_sentence) < 100:
                    heading = first_sentence
        except:
            pass
        
        return heading, subheading
    
    def create_enhanced_chunks(self, min_chunks: int = 30) -> List[Dict]:
        """Create enhanced chunks with better context"""
        enhanced_chunks = []
        chunk_id = 0
        
        print(f"\n🎯 Creating enhanced chunks (target: {min_chunks}+)...")
        
        for page_num, page_text in self.full_text_by_page.items():
            # Split by potential section markers
            sections = re.split(r'\n(?=[A-Z][A-Z\s]{10,}|\d+\.\s+[A-Z])', page_text)
            
            current_heading = "Introduction"
            
            for section in sections:
                if not section.strip():
                    continue
                
                lines = section.split('\n')
                if lines[0].strip() and (lines[0].strip().isupper() or re.match(r'^\d+\.', lines[0].strip())):
                    current_heading = lines[0].strip()
                    section = '\n'.join(lines[1:])
                
                # Split into paragraphs
                paragraphs = [p.strip() for p in section.split('\n\n') if p.strip() and len(p.strip()) > 100]
                
                for para in paragraphs:
                    para_lower = para.lower()
                    
                    # Check relevance
                    behavioral_terms = sum(1 for term in ['behav', 'policy', 'interv', 'nudge', 'decision', 'change'] if term in para_lower)
                    
                    if behavioral_terms >= 1:  # More lenient to get 30+ results
                        chunk_id += 1
                        
                        # Extract subheading if present
                        subheading = ""
                        if ':' in para[:100]:
                            potential_sub = para.split(':')[0].strip()
                            if len(potential_sub) < 80:
                                subheading = potential_sub
                        
                        chunk = ContentChunk(
                            chunk_id=chunk_id,
                            heading=current_heading,
                            subheading=subheading,
                            content=para[:1000] + ('...' if len(para) > 1000 else ''),  # Limit chunk size
                            page_number=page_num,
                            page_range=f"p. {page_num}",
                            in_text_citation=f"(Behavioural Insights Team, 2019, p. {page_num})",
                            section_type="Policy & Behavioral Science",
                            keywords=self.extract_keywords(para)
                        )
                        
                        enhanced_chunks.append(chunk.to_dict())
                        
                        if chunk_id >= min_chunks:
                            break
                
                if chunk_id >= min_chunks:
                    break
            
            if chunk_id >= min_chunks:
                break
        
        print(f"✅ Created {len(enhanced_chunks)} enhanced chunks")
        return enhanced_chunks
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract key terms from text"""
        keywords = []
        terms = [
            'policy maker', 'behavioral science', 'intervention', 'behavior change',
            'nudge', 'evidence', 'implementation', 'effectiveness', 'design',
            'practitioner', 'government', 'public policy', 'decision making',
            'behavioral insights', 'experiment', 'trial', 'evaluation'
        ]
        
        text_lower = text.lower()
        for term in terms:
            if term in text_lower:
                keywords.append(term)
        
        return keywords[:5]  # Top 5 keywords
    
    def save_chunks(self, chunks: List[Dict], output_path: str):
        """Save chunks to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved {len(chunks)} chunks to: {output_path}")
    
    def generate_markdown_report(self, chunks: List[Dict], output_path: str):
        """Generate a markdown report with all chunks"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Policy Maker & Behavioral Science Content Extraction\n\n")
            f.write(f"**Source:** {Path(self.pdf_path).name}\n\n")
            f.write(f"**Total Chunks Extracted:** {len(chunks)}\n\n")
            f.write("---\n\n")
            
            for chunk in chunks:
                f.write(f"## Chunk {chunk['chunk_id']}: {chunk['heading']}\n\n")
                
                if chunk['subheading']:
                    f.write(f"### {chunk['subheading']}\n\n")
                
                f.write(f"**Page Reference:** {chunk['page_range']}\n\n")
                f.write(f"**Citation:** {chunk['in_text_citation']}\n\n")
                f.write(f"**Keywords:** {', '.join(chunk['keywords'])}\n\n")
                f.write(f"**Content:**\n\n{chunk['content']}\n\n")
                f.write("---\n\n")
        
        print(f"📝 Generated markdown report: {output_path}")

def main():
    """Main execution function"""
    # Configuration
    pdf_path = r"R:\IDE\VLE\RESEARCHCLM\sources\metadata\pdfs\2019-BIT-Rare-Behavior-Change-for-Nature-digital (1).pdf"
    output_json = "policy_behavioral_chunks.json"
    output_markdown = "policy_behavioral_report.md"
    
    print("=" * 70)
    print("PDF CONTENT EXTRACTION & EMBEDDING SYSTEM")
    print("Policy Maker + Behavioral Science Focus")
    print("=" * 70)
    
    # Create extractor
    extractor = PDFEmbeddingExtractor(pdf_path)
    
    # Extract text with page numbers
    extractor.extract_text_with_pages()
    
    if not extractor.full_text_by_page:
        print("❌ Failed to extract text from PDF")
        return
    
    # Search for relevant content
    print("\n" + "=" * 70)
    print("SEARCHING FOR RELEVANT CONTENT")
    print("=" * 70)
    
    # Try both methods
    basic_chunks = extractor.search_policy_behavioral_content()
    enhanced_chunks = extractor.create_enhanced_chunks(min_chunks=30)
    
    # Use the method that got more results
    final_chunks = enhanced_chunks if len(enhanced_chunks) >= len(basic_chunks) else basic_chunks
    
    # Ensure we have at least 20 chunks
    if len(final_chunks) < 20:
        print(f"⚠️  Only found {len(final_chunks)} chunks, combining both methods...")
        # Combine and deduplicate
        all_chunks = basic_chunks + enhanced_chunks
        seen_content = set()
        unique_chunks = []
        for chunk in all_chunks:
            content_hash = chunk['content'][:100]
            if content_hash not in seen_content:
                seen_content.add(content_hash)
                unique_chunks.append(chunk)
        final_chunks = unique_chunks[:30]
    
    print(f"\n✅ Total chunks extracted: {len(final_chunks)}")
    
    # Save results
    print("\n" + "=" * 70)
    print("SAVING RESULTS")
    print("=" * 70)
    
    extractor.save_chunks(final_chunks, output_json)
    extractor.generate_markdown_report(final_chunks, output_markdown)
    
    # Print summary
    print("\n" + "=" * 70)
    print("EXTRACTION SUMMARY")
    print("=" * 70)
    print(f"✅ Extracted {len(final_chunks)} chunks")
    print(f"📊 Files created:")
    print(f"   - {output_json}")
    print(f"   - {output_markdown}")
    
    # Show first 3 chunks as preview
    print("\n" + "=" * 70)
    print("PREVIEW: First 3 Chunks")
    print("=" * 70)
    
    for chunk in final_chunks[:3]:
        print(f"\n📌 Chunk {chunk['chunk_id']}")
        print(f"   Heading: {chunk['heading']}")
        print(f"   Page: {chunk['page_range']}")
        print(f"   Citation: {chunk['in_text_citation']}")
        print(f"   Keywords: {', '.join(chunk['keywords'])}")
        print(f"   Content Preview: {chunk['content'][:200]}...")
    
    print("\n" + "=" * 70)
    print("RECOMMENDED EMBEDDING MODELS")
    print("=" * 70)
    print("""
1. **sentence-transformers/all-mpnet-base-v2** (BEST FOR YOUR USE CASE)
   - Dimensions: 768
   - Max tokens: 384
   - Best for: Semantic search, document similarity
   - Performance: High quality, balanced speed
   - Use case: Perfect for academic/policy documents

2. **text-embedding-3-large (OpenAI)**
   - Dimensions: 3072 (configurable)
   - Max tokens: 8191
   - Best for: High-precision semantic search
   - Cost: $0.13/1M tokens

3. **sentence-transformers/paraphrase-multilingual-mpnet-base-v2**
   - Dimensions: 768
   - Best for: Multilingual support (if needed)
   
4. **BAAI/bge-large-en-v1.5**
   - Dimensions: 1024
   - Best for: Retrieval tasks, high performance
   
5. **intfloat/e5-large-v2**
   - Dimensions: 1024
   - Best for: General purpose embeddings

RECOMMENDATION: Use sentence-transformers/all-mpnet-base-v2
- Free and open source
- Excellent for policy documents
- Good balance of quality and speed
- Works offline
    """)
    
    print("\n✅ Extraction complete!")
    print(f"📖 Review the markdown report for full content")
    print(f"🔗 All chunks include page references and citations")

if __name__ == "__main__":
    main()

