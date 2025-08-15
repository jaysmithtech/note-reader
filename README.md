# 🤖 Note Reader Chat App

> **AI-powered note analysis and chat application built with Flask, React, and LangChain**

Transform your notes into an intelligent, searchable knowledge base. Ask questions about your documents and get AI-powered responses with source citations.

![Note Reader Chat](https://img.shields.io/badge/React-18.2.0-blue?style=for-the-badge&logo=react)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green?style=for-the-badge&logo=flask)
![LangChain](https://img.shields.io/badge/LangChain-0.1.0-orange?style=for-the-badge)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-purple?style=for-the-badge&logo=openai)

## ✨ Features

- 🧠 **AI-Powered Analysis** - RAG (Retrieval-Augmented Generation) for intelligent note querying
- 💬 **Modern Chat Interface** - Beautiful React-based UI with real-time chat
- 📚 **Multi-format Support** - Handles Markdown, TXT, PDF, and DOCX files
- 🔍 **Vector Search** - FAISS-based similarity search for relevant document chunks
- 📱 **Responsive Design** - Mobile-first interface with Tailwind CSS
- ⚡ **Real-time Chat** - Instant AI responses with typing indicators
- 🎯 **Source Citations** - Every response includes document references

## 🏗️ Architecture

This application combines the power of modern web technologies:

- **Backend**: Flask + LangChain + OpenAI + FAISS
- **Frontend**: React 18 + Tailwind CSS + Lucide Icons
- **AI**: GPT-4o with RAG (Retrieval-Augmented Generation)
- **Vector Database**: FAISS for similarity search

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- OpenAI API key

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/note-reader-chat.git
cd note-reader-chat
```

### 2. Automated Setup (Recommended)

```bash
chmod +x setup.sh
./setup.sh
```

### 3. Manual Setup

#### Backend Setup
```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Create environment file
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run build
cd ..
```

### 4. Add Your Notes

Place documents in the `notes/` folder:
- **Markdown** (`.md`)
- **Text** (`.txt`) 
- **PDF** (`.pdf`)
- **Word** (`.docx`)

### 5. Run the Application

```bash
python3 app.py
```

### 6. Open Your Browser

Navigate to: `http://localhost:5001`

## 🎯 How It Works

### 1. Document Processing
- Documents are automatically loaded from the `notes/` folder
- Text is split into optimal chunks for AI processing
- FAISS creates searchable vector embeddings

### 2. AI-Powered Querying
- When you ask a question, the system:
  - Searches for relevant document chunks
  - Provides context to the AI model
  - Generates accurate, source-cited responses

### 3. Modern Web Interface
- React frontend provides a smooth chat experience
- Real-time updates with typing indicators
- Responsive design works on all devices

## 🎨 Frontend Features

- **Modern UI**: Built with React 18 and Tailwind CSS
- **Responsive Design**: Mobile-first approach
- **Smooth Animations**: Fade-in effects and transitions
- **Real-time Chat**: Live updates with typing indicators
- **Clean Layout**: Two-column design with chat and notes preview
- **Accessibility**: Proper ARIA labels and keyboard navigation

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main React application |
| `/api/chat` | POST | Send chat messages and get AI responses |
| `/api/notes` | GET | Retrieve formatted notes content |

## 🛠️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
OPENAI_MODEL=gpt-4o
OPENAI_TEMPERATURE=0.2
```

### Model Settings

- **Default Model**: GPT-4o (can be changed to GPT-5 if available)
- **Temperature**: 0.2 (balanced creativity and accuracy)
- **Chunk Size**: 1200 characters (optimized for context)
- **Search Results**: Top 4 most relevant chunks

## 📁 Project Structure

```
note-reader/
├── app.py                    # Flask backend with LangChain integration
├── requirements.txt          # Python dependencies
├── .env                     # Environment variables (create this)
├── .gitignore               # Git ignore rules
├── setup.sh                 # Automated setup script
├── frontend/                # React frontend application
│   ├── src/                 # React source code
│   ├── public/              # Static assets
│   ├── package.json         # Node.js dependencies
│   └── tailwind.config.js   # Tailwind CSS configuration
├── notes/                   # Your documents (add files here)
│   └── .gitkeep            # Preserves folder structure
└── README.md                # This file
```

## 🚨 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| "OPENAI_API_KEY is not set" | Create `.env` file with your API key |
| "No documents found" | Add files to `notes/` folder and restart |
| Import errors | Run `pip3 install -r requirements.txt` |
| Port 5001 busy | Change port in `app.py` |
| Frontend not loading | Ensure you ran `npm run build` |

### Getting Help

1. Check the [Issues](../../issues) page
2. Verify your OpenAI API key is valid
3. Ensure all dependencies are installed
4. Check the console for error messages

## 🛠️ Development

### Frontend Development
```bash
cd frontend
npm start  # Runs on http://localhost:3000 with hot reload
```

### Backend Development
```bash
python3 app.py  # Runs on http://localhost:5001
```

### Production Build
```bash
cd frontend
npm run build
cd ..
python3 app.py
```

## 📦 Dependencies

### Backend
- **Flask**: Web framework
- **LangChain**: AI/LLM orchestration
- **OpenAI**: Language model API
- **FAISS**: Vector similarity search
- **Document Loaders**: Multi-format support

### Frontend
- **React 18**: Modern UI framework
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Beautiful icon library
- **Modern JavaScript**: ES6+ features and hooks

## 🌟 Use Cases

- **Research Papers**: Ask questions about academic documents
- **Meeting Notes**: Get summaries and find specific information
- **Project Documentation**: Search through technical docs
- **Personal Journals**: Analyze and query personal notes
- **Study Materials**: Interactive learning with your notes

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for the GPT models
- **LangChain** for AI orchestration
- **FAISS** for vector similarity search
- **React** and **Tailwind CSS** for the beautiful UI

---

**Made with ❤️ by Jaylon**
