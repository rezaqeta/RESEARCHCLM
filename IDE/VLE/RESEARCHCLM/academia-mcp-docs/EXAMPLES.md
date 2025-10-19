# Academia MCP - Usage Examples

## Complete Examples for Each Tool

### 1. ArXiv Search Examples

#### Example 1: Basic Keyword Search

**Goal**: Find recent papers on transformer architectures

**Query**: "transformer attention mechanisms"

**Expected Results**:
- Paper titles and authors
- Abstract summaries
- ArXiv IDs (e.g., 2103.14030)
- Publication dates
- PDF download links
- Categories (cs.CL, cs.LG, etc.)

**AI Assistant Prompt**:
```
"Search arXiv for papers about transformer attention mechanisms published in the last 2 years"
```

#### Example 2: Author-Specific Search

**Goal**: Find papers by a specific researcher

**Query**: "author:Yoshua Bengio deep learning"

**AI Assistant Prompt**:
```
"Find papers by Yoshua Bengio on arXiv related to deep learning"
```

#### Example 3: Category-Specific Search

**Goal**: Find computer vision papers

**Query**: "cat:cs.CV object detection"

**AI Assistant Prompt**:
```
"Search arXiv category cs.CV for papers about object detection"
```

#### Example 4: Time-Bound Search

**Query**: Papers from specific year

**AI Assistant Prompt**:
```
"Find arXiv papers about GANs published in 2023"
```

---

### 2. Semantic Scholar Examples

#### Example 1: Citation Analysis

**Goal**: Find who is citing a specific paper

**Paper**: "BERT: Pre-training of Deep Bidirectional Transformers"

**AI Assistant Prompt**:
```
"Find all papers that cite the BERT paper and show me the most influential ones"
```

**What you'll get**:
- Citing papers
- Citation context (how they use BERT)
- Influence scores
- Publication venues
- Authors

#### Example 2: Paper Recommendations

**Goal**: Find related papers

**AI Assistant Prompt**:
```
"Given this paper on graph neural networks, what are similar papers I should read?"
```

#### Example 3: Author Profile

**Goal**: Explore an author's work

**AI Assistant Prompt**:
```
"Show me the most cited papers by Yann LeCun and their citation counts"
```

#### Example 4: Field Overview

**Goal**: Understand a research area

**AI Assistant Prompt**:
```
"What are the most influential papers in reinforcement learning from the last 5 years?"
```

---

### 3. ACL Anthology Examples

#### Example 1: Conference Paper Search

**Goal**: Find papers from specific NLP conferences

**AI Assistant Prompt**:
```
"Search ACL Anthology for papers about named entity recognition presented at ACL 2024"
```

#### Example 2: Author Search in NLP

**Goal**: Find NLP papers by author

**AI Assistant Prompt**:
```
"Find papers by Christopher Manning in the ACL Anthology"
```

#### Example 3: Topic-Specific Search

**Goal**: Papers on specific NLP topics

**AI Assistant Prompt**:
```
"Find papers about machine translation in the ACL Anthology from EMNLP conferences"
```

---

### 4. HuggingFace Datasets Examples

#### Example 1: Task-Specific Dataset Search

**Goal**: Find datasets for sentiment analysis

**AI Assistant Prompt**:
```
"Find sentiment analysis datasets on HuggingFace Hub"
```

**Expected Results**:
- Dataset names (e.g., IMDB, SST-2)
- Sizes (number of examples)
- Languages
- Tasks
- Licenses
- Download statistics

#### Example 2: Language-Specific Datasets

**Goal**: Find datasets in a specific language

**AI Assistant Prompt**:
```
"Show me German language datasets for question answering on HuggingFace"
```

#### Example 3: Multimodal Datasets

**Goal**: Find vision-language datasets

**AI Assistant Prompt**:
```
"Find image captioning datasets on HuggingFace"
```

#### Example 4: Dataset Details

**Goal**: Get comprehensive dataset information

**AI Assistant Prompt**:
```
"Tell me about the GLUE benchmark dataset - size, tasks, and how to use it"
```

---

### 5. Document Q&A Examples

**Note**: Requires OPENROUTER_API_KEY to be set

#### Example 1: Extract Main Contribution

**Setup**: Have a paper PDF or text

**AI Assistant Prompt**:
```
"What is the main contribution of this paper? [paper content or path]"
```

**Expected Response**:
- Summary of key innovation
- Novel aspects
- Comparison to previous work

#### Example 2: Methodology Questions

**AI Assistant Prompt**:
```
"Explain the methodology used in this paper step by step"
```

**Expected Response**:
- Detailed method explanation
- Architecture diagrams (if described)
- Training procedures
- Hyperparameters

#### Example 3: Results Analysis

**AI Assistant Prompt**:
```
"What were the main results? How do they compare to baselines?"
```

**Expected Response**:
- Performance metrics
- Comparison tables
- Statistical significance
- Ablation study results

#### Example 4: Limitations and Future Work

**AI Assistant Prompt**:
```
"What limitations do the authors acknowledge? What future work do they suggest?"
```

#### Example 5: Multi-Paper Comparison

**AI Assistant Prompt**:
```
"Compare the approaches in these three papers about image segmentation"
```

---

### 6. Web Search Examples

#### Example 1: Academic Blog Posts

**Goal**: Find expert blog posts on a topic

**AI Assistant Prompt**:
```
"Search the web for blog posts explaining attention mechanisms in transformers"
```

#### Example 2: Code Repositories

**Goal**: Find implementations

**AI Assistant Prompt**:
```
"Find GitHub repositories implementing YOLO object detection"
```

#### Example 3: Dataset Documentation

**Goal**: Find dataset documentation and usage guides

**AI Assistant Prompt**:
```
"Search for documentation and tutorials on using the COCO dataset"
```

#### Example 4: Recent News

**Goal**: Stay updated on AI developments

**AI Assistant Prompt**:
```
"What are recent developments in large language models? Search the web"
```

---

### 7. Page Crawler Examples

#### Example 1: Extract Paper from Website

**Goal**: Get paper content from a webpage

**URL**: https://arxiv.org/abs/2103.14030

**AI Assistant Prompt**:
```
"Crawl this arXiv page and extract the paper abstract and information"
```

#### Example 2: Conference Proceedings

**Goal**: Extract information from conference websites

**AI Assistant Prompt**:
```
"Crawl the ICML 2024 accepted papers page and list the titles"
```

#### Example 3: Research Lab Pages

**Goal**: Get information from research group websites

**AI Assistant Prompt**:
```
"Extract the list of publications from this research lab's website"
```

---

## Complete Workflow Examples

### Workflow 1: Literature Review for New Topic

```
Step 1: Broad Search
"Search arXiv for papers about federated learning"

Step 2: Narrow Down
"From these results, which papers are most cited according to Semantic Scholar?"

Step 3: Explore Citations
"For the top 3 papers, show me what papers they cite and what cites them"

Step 4: Deep Dive
"Download PDFs for the top 5 papers"

Step 5: Q&A
"For each paper, what is the main innovation?"

Step 6: Find Datasets
"What datasets are commonly used for federated learning research?"

Step 7: Find Code
"Search the web for GitHub repos implementing federated learning algorithms"
```

### Workflow 2: Dataset Selection

```
Step 1: Define Task
"I need datasets for multilingual sentiment analysis"

Step 2: Search HuggingFace
"Find sentiment analysis datasets on HuggingFace that support multiple languages"

Step 3: Compare Options
"Compare the size, languages, and licenses of these datasets"

Step 4: Check Usage
"Search the web for papers that use these datasets"

Step 5: Get Documentation
"Find tutorials on how to use the XYZ dataset"
```

### Workflow 3: Understanding a Paper

```
Step 1: Find Paper
"Search arXiv for the Vision Transformer paper"

Step 2: Get Context
"What papers does ViT cite? What's the historical context?"

Step 3: Ask Questions
"What is the key innovation in ViT compared to CNNs?"

Step 4: Check Impact
"How many papers cite ViT? What are the main follow-up works?"

Step 5: Find Implementations
"Search for PyTorch implementations of Vision Transformer"

Step 6: Find Related Datasets
"What datasets are used to evaluate Vision Transformers?"
```

### Workflow 4: Research Trend Analysis

```
Step 1: Identify Topic
"I want to understand trends in graph neural networks"

Step 2: Historical View
"Find the seminal papers in graph neural networks from 2015-2020"

Step 3: Recent Developments
"What are the most cited GNN papers from 2023-2024?"

Step 4: Sub-Topics
"What are the main sub-areas in GNN research?"

Step 5: Key Researchers
"Who are the most prolific authors in GNN research?"

Step 6: Datasets
"What benchmark datasets are used for GNN evaluation?"
```

### Workflow 5: Reproducing Results

```
Step 1: Find Paper
"Search for the paper 'XYZ' on arXiv"

Step 2: Understand Method
"Explain the training procedure and hyperparameters used"

Step 3: Find Code
"Search the web for official or third-party implementations"

Step 4: Find Dataset
"What dataset did they use? Find it on HuggingFace if available"

Step 5: Check Citations
"Are there papers that reproduced or extended these results?"

Step 6: Community Discussion
"Search for blog posts or forum discussions about implementing this"
```

---

## Advanced Query Patterns

### Boolean Operators

```
"transformer AND attention NOT vision"
"(GAN OR adversarial) AND image generation"
"deep learning AND (medical OR healthcare)"
```

### Field-Specific Searches

```
"title:BERT"  # Search in title only
"author:Hinton"  # Search by author
"cat:cs.CV"  # Search in category
```

### Time-Based Queries

```
"submittedDate:[202401 TO 202412]"  # 2024 papers
"lastUpdated:[20230101 TO *]"  # Updated since 2023
```

### Sorting and Filtering

```
"Sort by citation count, show only papers with code available"
"Filter by conference: ACL, EMNLP, NAACL"
"Show only papers with datasets"
```

---

## Tips for Effective Use

### 1. Start Broad, Then Narrow

❌ Bad: "machine learning"
✅ Good: "transformer architectures for computer vision" → "vision transformer variants 2023"

### 2. Use Multiple Sources

```
"Search arXiv, Semantic Scholar, and ACL Anthology for papers on few-shot learning"
```

### 3. Combine Tools

```
1. Search → 2. Explore Citations → 3. Q&A → 4. Find Datasets → 5. Find Code
```

### 4. Leverage Context

```
"Based on the papers we just found, what are common datasets mentioned?"
```

### 5. Ask Follow-Up Questions

```
"From that list, which paper has the most novel approach?"
"Which of these datasets is largest?"
"What are the limitations of this method?"
```

---

## Integration with Research Workflow

### Morning Routine: Stay Updated

```
"What are the latest papers on arXiv in category cs.LG from this week?"
"Show me the trending papers on Semantic Scholar in my field"
```

### Literature Review

```
"Build a citation network for these 5 papers"
"Find common themes and methods across these papers"
```

### Experiment Planning

```
"What datasets should I use for image classification?"
"What are the standard baselines for this task?"
```

### Writing Papers

```
"Find papers that cite these methods"
"What are the key references I should include?"
```

---

## Next Steps

After trying these examples:

1. ⬜ Customize queries for your research area
2. ⬜ Create your own workflow patterns
3. ⬜ Integrate with your note-taking system
4. ⬜ Set up automated alerts for new papers
5. ⬜ Build a personal paper database

---

**Last Updated**: October 10, 2025
**Version**: academia-mcp 1.8.1






