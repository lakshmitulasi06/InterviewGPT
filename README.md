# 🤖 InterviewGPT

An AI-powered interview coaching platform that helps candidates prepare for technical interviews using Retrieval-Augmented Generation (RAG) and advanced language models.

## Features

✨ **AI Interview Coach**
- Resume parsing and skill extraction
- AI-generated interview questions based on candidate profile
- Real-time answer evaluation with feedback
- Performance metrics tracking (technical & communication scores)
- Chat history for review and improvement

🎯 **Core Capabilities**
- **Resume Analysis**: Extract skills and qualifications from PDF resumes
- **Skill-based Questions**: Generate relevant interview questions based on extracted skills
- **Answer Evaluation**: Get instant feedback on technical accuracy and communication clarity
- **Performance Tracking**: Monitor your progress with trending scores

## Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) - Interactive web UI
- **LLM**: [Groq](https://groq.com/) - Fast inference for question generation and evaluation
- **RAG Framework**: [LangChain](https://python.langchain.com/) - For context-aware question generation
- **Vector DB**: [ChromaDB](https://www.trychroma.com/) - Semantic search for resume content
- **Embeddings**: [Sentence-Transformers](https://www.sbert.net/) - Text embeddings
- **PDF Processing**: [pdfplumber](https://github.com/jamesturk/pdfplumber) & [PyPDF](https://pypdf.readthedocs.io/)

## Project Structure

```
InterviewGPT/
├── app.py                 # Main Streamlit application
├── resume_parser.py       # Extract text and skills from resumes
├── skill_extractor.py     # Parse and categorize technical skills
├── rag.py                 # RAG pipeline for question generation
├── evaluator.py           # Answer evaluation and scoring
├── requirement.txt        # Project dependencies
└── README.md             # This file
```

## Installation

### Prerequisites
- Python 3.8+
- Git

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/lakshmitulasi06/InterviewGPT.git
cd InterviewGPT
```

2. **Create virtual environment**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirement.txt
```

4. **Set up environment variables**
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get your Groq API key from [https://console.groq.com/](https://console.groq.com/)

## Usage

1. **Start the Streamlit app**
```bash
streamlit run app.py
```

2. **Upload your resume**
   - Click the file uploader to select your PDF resume
   - The app will extract your skills automatically

3. **Begin your interview**
   - Click "Generate Question" to get AI-generated interview questions
   - Answer each question thoughtfully
   - Click "Evaluate Answer" to receive instant feedback

4. **Track your progress**
   - View your technical and communication scores
   - See trends in your performance metrics
   - Review chat history for improvement areas

## Key Modules

### `resume_parser.py`
- Extracts text from PDF files
- Preprocesses and cleans resume content
- Returns raw resume text for skill extraction

### `skill_extractor.py`
- Parses extracted resume text
- Identifies technical skills, programming languages, frameworks
- Categorizes skills by expertise level

### `rag.py`
- Creates vector store from resume content using ChromaDB
- Generates contextual interview questions based on candidate profile
- Uses LangChain for semantic search and retrieval

### `evaluator.py`
- Evaluates candidate answers on multiple dimensions
- Provides technical accuracy scoring
- Assesses communication clarity
- Generates actionable feedback

### `app.py`
- Streamlit UI application
- Manages user session state
- Orchestrates all components
- Displays performance dashboard

## How It Works

```
1. Resume Upload → 2. Skill Extraction → 3. Vector Store Creation
                           ↓
4. AI Question Generation ← Resume Context
                           ↓
5. User Answer Input → 6. LLM Evaluation
                           ↓
7. Score & Feedback → 8. Performance Tracking
```

## Configuration

### Environment Variables
- `GROQ_API_KEY`: Your Groq API key for LLM access

### Model Settings
- LLM Model: Groq's fast inference models
- Embedding Model: Sentence-Transformers (all-MiniLM-L6-v2)
- Vector DB: ChromaDB with in-memory storage

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [LangChain](https://python.langchain.com/) for RAG capabilities
- [Groq](https://groq.com/) for fast LLM inference
- [ChromaDB](https://www.trychroma.com/) for vector database

## Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the maintainers.

---

**Happy interviewing! 🚀**
