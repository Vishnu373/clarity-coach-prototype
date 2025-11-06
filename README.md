# Clarity Coach MVP

An AI-powered career coaching platform that helps professionals enhance their resumes, assess AI automation risk, and discover growth opportunities.

## 🚀 Current Version (v1.0)

### How It Works

```
User Resume Upload (PDF/DOCX/TXT)
    ↓
📄 Document Extraction
    ├── Digital PDF → Python libraries (pdfplumber, camelot)
    └── Scanned PDF → AWS Textract
    ↓
🔄 Resume Restructuring (GPT-4o-mini)
    ├── Standardized format conversion
    └── Data extraction & organization
    ↓
🧠 AI Enhancement Pipeline
    ├── RAG (Retrieval Augmented Generation)
    │   ├── Knowledge base embedding search
    │   └── Similar role/responsibility matching
    └── GPT-4 → Generate 10 additional responsibilities/projects (resume enhancement)
    ↓
📊 Market Intelligence Analysis
    ├── Skills & Experience Categorization (GPT-4o-mini)
    ├── Industry Risk Classification
    └── Task Complexity Assessment
    ↓
🎯 AI Risk Calculator
    ├── IMF Gen-AI 2024 Report Analysis
    ├── Automation Risk Percentage
    └── Risk Level Assessment (High/Medium/Low)
    ↓
📈 Career Growth Recommendations
    ├── Future-proof Skills Suggestions
    ├── Upskilling Recommendations
    └── Job Market Search (SERP API)
    ↓
💼 Personalized Results Dashboard
```

### Tech Stack

**Frontend & Interface:**
- Streamlit (Web Interface)

**AI & Machine Learning:**
- OpenAI GPT-5 (Resume enhancement)
- OpenAI GPT-4o-mini (Restructuring & analysis)
- OpenAI text-embedding-3-small (Vector embeddings)
- Intially -> FAISS CPU (Vector similarity search), shifted to Pgvector (supabase)
- Custom RAG pipeline

**Document Processing:**
- pdfplumber (PDF text extraction)
- camelot-py (PDF table extraction)
- python-docx (Word document processing)
- pdfminer.six (PDF parsing)
- AWS Textract (OCR for scanned documents)

**Cloud Services:**
- AWS S3 (File storage)
- AWS Textract (OCR processing)

**APIs & External Services:**
- SERP API (Google jobs search api)

### Key Features

- **Multi-format Resume Support**: PDF (digital & scanned), DOCX, TXT
- **Intelligent Document Processing**: Automatic text/table extraction with OCR fallback
- **AI-Powered Enhancement**: Generate realistic additional responsibilities and projects
- **Risk Assessment**: AI automation risk analysis based on IMF GEN AI 2024 report
- **Market Intelligence**: Real-time job market analysis and recommendations
- **Skills Gap Analysis**: Identify missing skills for career growth
- **Personalized Recommendations**: Tailored upskilling and job suggestions

---
