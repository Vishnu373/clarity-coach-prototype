## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Vishnu373/clarity-coach-prototype.git
cd clarity-coach-prototype
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your OpenAI API key

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Run the app

```bash
streamlit run main.py
```
