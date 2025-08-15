#!/bin/bash

echo "🚀 Setting up Note Reader Chat App..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Install Node.js dependencies and build React app
echo "⚛️  Setting up React frontend..."
cd frontend
npm install
npm run build
cd ..

echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Create a .env file with your OpenAI API key:"
echo "   echo 'OPENAI_API_KEY=your_key_here' > .env"
echo ""
echo "2. Add some notes to the ./notes folder"
echo ""
echo "3. Run the app: python3 app.py"
echo ""
echo "4. Open http://localhost:5001 in your browser"
