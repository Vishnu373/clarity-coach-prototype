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

## 🔮 Improved Version (Under Development)

### How It Works (Enhanced Pipeline)

```
User Resume Upload + Target Job Description
    ↓
📄 Document Extraction
    ├── Digital PDF → Python libraries (pdfplumber, camelot)
    └── Scanned PDF → AWS Textract
    ↓
🧠 Smart Field Identification & Classification
    ├── Smaller LLM Model → Identify required fields
    ├── Skills Classification
    ├── Job Responsibilities/Bullet Points Analysis
    └── Industry Details Extraction
    ↓
🗄️ MongoDB Storage
    ├── Flexible schema for varying resume fields
    └── Identified required fields (for RAG) & classified data (for AI risk anaylsis)
    ↓
🎯 Context-Aware Resume Tailoring
    ├── Identified Fields + Job Description
    ├── RAG (Retrieval Augmented Generation)
    └── GPT-5 → Tailored Resume + 10 Additional Projects/Responsibilities
    ↓
📊 Enhanced AI Risk Analysis
    ├── Classified Details → AI Risk Calculator
    ├── IMF Gen-AI 2024 Report Analysis
    └── Risk Score
    ↓
🎓 Context-Aware Upskilling
    ├── Current Skills + Bullet Points Analysis
    ├── LLM Context-Aware Prompting
    ├── Suggested Upskills
    └── Recommended Courses
    ↓
💼 Advanced Job Matching
    ├── Current Skills + Upskills Analysis
    ├── Google Cloud Talent Solution
    ├── Intelligent Filtering & Ranking
    └── Personalized Job Recommendations
```

### Enhanced Tech Stack

**Frontend & Interface:**
- Streamlit (Enhanced UI/UX)

**AI & Machine Learning:**
- OpenAI GPT-5 (Resume tailoring & enhancement)
- Smaller LLM Model (Field identification & classification)
- OpenAI text-embedding-3-small (Vector embeddings)
- Advanced RAG pipeline with context awareness

**Document Processing:**
- pdfplumber (PDF text extraction)
- camelot-py (PDF table extraction)
- python-docx (Word document processing)
- pdfminer.six (PDF parsing)
- AWS Textract (OCR for scanned documents)

**Database & Storage:**
- MongoDB (Flexible document storage for varying resume structures)

**Cloud Services:**
- AWS Textract (OCR processing)
- Google Cloud Talent Solution (Advanced job matching)

**APIs & External Services:**
- Google Cloud Talent Solution API
- Course recommendation APIs (planned)


### Key Improvements

**🎯 Enhanced Personalization:**
- Job description-aware resume tailoring
- Context-sensitive skill recommendations
- Dynamic field identification for varied resume formats

**🧠 Smarter AI Processing:**
- Multi-model approach (smaller LLM for identification and classification + GPT-5 for generation)
- Context-aware prompting for better upskilling suggestions

**🗄️ Flexible Data Management:**
- MongoDB for handling diverse resume structures
- Support for publications, awards, certifications, and custom fields
- Scalable document-based storage

**💼 Advanced Job Matching:**
- Google Cloud Talent Solution api integration
- Intelligent job filtering and ranking algorithms
- Skills gap analysis with upskilling pathways

