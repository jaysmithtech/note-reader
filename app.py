from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass

# LangChain core
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# OpenAI integrations
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Vector store
from langchain_community.vectorstores import FAISS

# Document loaders / splitters
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")

# ---- Model knobs ----
# Use "gpt-5" if you have access; else "gpt-4o"
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o")
TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.2"))

llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE, api_key=OPENAI_API_KEY)
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

@dataclass
class NotesConfig:
    notes_dir: str = "./notes"   # change to your path
    glob_pattern: str = "**/*.md"
    chunk_size: int = 1200
    chunk_overlap: int = 150

config = NotesConfig(notes_dir="./notes")  # <-- set your folder
Path(config.notes_dir).mkdir(parents=True, exist_ok=True)  # ensure exists

def load_any_notes(notes_dir: Path):
    docs = []

    # .md / .txt
    for ext in ("*.md", "*.txt"):
        for fp in notes_dir.rglob(ext):
            docs.extend(TextLoader(str(fp), encoding="utf-8").load())

    # .pdf
    for fp in notes_dir.rglob("*.pdf"):
        docs.extend(PyPDFLoader(str(fp)).load())

    # .docx (optional)
    for fp in notes_dir.rglob("*.docx"):
        docs.extend(Docx2txtLoader(str(fp)).load())

    return docs

class NoteReader:
    def __init__(self):
        self.vectorstore = None
        self.retriever = None
        self.rag_chain = None
        self.notes_content = ""
        self.initialize_notes()
    
    def initialize_notes(self):
        """Initialize the notes system by loading and processing documents"""
        try:
            # Load raw documents
            raw_docs = load_any_notes(Path(config.notes_dir))
            
            if not raw_docs:
                print(f"No documents found under: {config.notes_dir}. Add some .md, .txt, .pdf, or .docx files and re-run.")
                self.notes_content = "No notes found. Please add some documents to the ./notes folder."
                return
            
            print(f"Loaded {len(raw_docs)} documents from {config.notes_dir}")
            
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=config.chunk_size,
                chunk_overlap=config.chunk_overlap,
                separators=["\n\n", "\n", " ", ""],
            )
            
            docs = text_splitter.split_documents(raw_docs)
            print(f"Created {len(docs)} chunks")
            
            # Create vector store
            self.vectorstore = FAISS.from_documents(docs, embeddings)
            self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})
            
            # Store notes content for display
            self.notes_content = self.format_notes_for_display(raw_docs)
            
            # Setup RAG chain
            self.setup_rag_chain()
            
        except Exception as e:
            print(f"Error initializing notes: {e}")
            self.notes_content = f"Error loading notes: {str(e)}"
    
    def format_notes_for_display(self, docs):
        """Format notes for display in the frontend"""
        formatted = []
        for doc in docs:
            source = doc.metadata.get("source", "unknown")
            filename = Path(source).name
            formatted.append(f"📄 {filename}\n{doc.page_content[:200]}...")
        return "\n\n".join(formatted)
    
    def format_docs(self, docs):
        """Format documents for RAG context"""
        formatted = []
        for d in docs: 
            source = d.metadata.get("source", "unknown.md")
            formatted.append(f"[SOURCE: {Path(source).name}]\n{d.page_content}")
        return "\n\n---\n\n".join(formatted)
    
    def setup_rag_chain(self):
        """Setup the RAG chain for question answering"""
        if not self.retriever:
            return
            
        RAG_PROMPT = PromptTemplate.from_template(
            """You are a helpful notes assistant. Use only the provided context to answer the question.
Cite sources like [SOURCE: filename.md] when relevant.

Question:
{question}

Context:
{context}

Answer succinctly, with bullet points when helpful, and list sources at the end."""
        )
        
        self.rag_chain = (
            {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
            | RAG_PROMPT
            | llm
            | StrOutputParser()
        )
    
    def read_notes(self):
        """Return the formatted notes content for display"""
        return self.notes_content
    
    def summarize_notes(self, query):
        """Query notes using RAG and return response"""
        if not self.rag_chain:
            return "Notes system not properly initialized. Please check that you have documents in the ./notes folder."
        
        try:
            response = self.rag_chain.invoke(query)
            return response
        except Exception as e:
            return f"Error processing your question: {str(e)}"

# Initialize the note reader
note_reader = NoteReader()

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Process the message and get response
        response = note_reader.summarize_notes(message)
        
        return jsonify({
            'response': response,
            'timestamp': '2024-01-01T00:00:00Z'  # You can add proper timestamp logic
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes', methods=['GET'])
def get_notes():
    try:
        # Get notes content
        notes_content = note_reader.read_notes()
        
        return jsonify({
            'notes': notes_content,
            'timestamp': '2024-01-01T00:00:00Z'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def serve():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
