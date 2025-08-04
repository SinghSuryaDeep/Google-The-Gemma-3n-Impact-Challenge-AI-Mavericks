#!/bin/bash

# EmpowerEd Setup Script
# Installs all dependencies and Gemma 3n models via Ollama

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🌟 EmpowerEd - Special Needs Learning Assistant${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print status
print_status() {
    echo -e "${YELLOW}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check Python version
print_status "Checking Python version..."
if command_exists python3; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_success "Python $PYTHON_VERSION found"
else
    print_error "Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment
print_status "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate
print_success "Virtual environment created"

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip
print_success "Pip upgraded"

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt
print_success "Python dependencies installed"

# Install Ollama if not present
if ! command_exists ollama; then
    print_status "Installing Ollama..."
    
    # Detect OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -fsSL https://ollama.com/install.sh | sh
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command_exists brew; then
            brew install ollama
        else
            curl -fsSL https://ollama.com/install.sh | sh
        fi
    else
        print_error "Unsupported OS. Please install Ollama manually from https://ollama.com"
        exit 1
    fi
    print_success "Ollama installed"
else
    print_success "Ollama already installed"
fi

# Start Ollama service
print_status "Starting Ollama service..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS - start in background
    ollama serve > /dev/null 2>&1 &
    OLLAMA_PID=$!
else
    # Linux - use systemctl if available
    if command_exists systemctl; then
        sudo systemctl start ollama 2>/dev/null || ollama serve > /dev/null 2>&1 &
    else
        ollama serve > /dev/null 2>&1 &
        OLLAMA_PID=$!
    fi
fi
sleep 5  # Give Ollama time to start
print_success "Ollama service started"

# Download Gemma 3n models
echo ""
echo -e "${BLUE}📥 Downloading Gemma 3n Models${NC}"
echo -e "${BLUE}==============================${NC}"
echo ""

# Model 1: Fast model (2B) for instant responses
print_status "Downloading Gemma 3n 2B (Fast Model)..."
echo "   Used for: Reading assistance, quick text processing"
ollama pull gemma3n:e2b
print_success "Fast model downloaded"

# Model 2: Accurate model (4B) for complex tasks
print_status "Downloading Gemma 3n 4B (Accurate Model)..."
echo "   Used for: Complex analysis, lesson generation"
ollama pull hf.co/unsloth/gemma-3n-E4B-it-GGUF:UD-Q4_K_XL
print_success "Accurate model downloaded"

# Model 3: Vision model for image processing
print_status "Downloading Gemma 3n Vision Model..."
echo "   Used for: Image analysis, visual learning"
ollama pull gemma3n:e4b
print_success "Vision model downloaded"

# Verify models
echo ""
print_status "Verifying installed models..."
INSTALLED_MODELS=$(ollama list)
echo "$INSTALLED_MODELS"
print_success "All models verified"

# Create necessary directories
print_status "Creating project directories..."
mkdir -p data/{profiles,progress,lessons,resources}
mkdir -p data/resources/{fonts,images,audio}
mkdir -p logs
mkdir -p cache
mkdir -p demo/screenshots
print_success "Directories created"

# Download accessibility resources
print_status "Downloading accessibility resources..."

# OpenDyslexic font for dyslexia support
if [ ! -f "data/resources/fonts/OpenDyslexic.ttf" ]; then
    curl -L https://github.com/antijingoist/opendyslexic/raw/master/otf/OpenDyslexic-Regular.otf \
         -o data/resources/fonts/OpenDyslexic.ttf 2>/dev/null
    print_success "OpenDyslexic font downloaded"
fi

# Create sample data
print_status "Creating sample data..."
cat > data/profiles/sample_profile.json << EOF
{
    "name": "Sample Student",
    "disabilities": ["Dyslexia", "ADHD"],
    "reading_speed": "slow",
    "visual_preference": "dyslexia_friendly",
    "audio_preference": true,
    "attention_span": 10,
    "learning_style": "visual"
}
EOF
print_success "Sample data created"

# Create .env file if not exists
if [ ! -f ".env" ]; then
    print_status "Creating environment configuration..."
    cat > .env << EOF
# EmpowerEd Configuration
DEBUG=False
OLLAMA_HOST=http://localhost:11434

# Gemma 3n Models
FAST_MODEL=gemma3n:e2b
ACCURATE_MODEL=hf.co/unsloth/gemma-3n-E4B-it-GGUF:UD-Q4_K_XL
VISION_MODEL=gemma3n:e4b

# Accessibility Settings
DEFAULT_FONT_SIZE=16
HIGH_CONTRAST_MODE=False
AUDIO_ENABLED=True
EOF
    print_success "Environment configuration created"
fi

# Test the setup
echo ""
echo -e "${BLUE}🧪 Testing Setup${NC}"
echo -e "${BLUE}===============${NC}"
echo ""

print_status "Running setup tests..."
python3 scripts/test_setup.py

# Create launch script
print_status "Creating launch script..."
cat > run_empowered.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
streamlit run app/main.py
EOF
chmod +x run_empowered.sh
print_success "Launch script created"

# Final summary
echo ""
echo -e "${GREEN}✨ Setup Complete! ✨${NC}"
echo -e "${GREEN}====================${NC}"
echo ""
echo "📋 Installed Components:"
echo "   • Python dependencies ✅"
echo "   • Ollama service ✅"
echo "   • Gemma 3n 2B (Fast) ✅"
echo "   • Gemma 3n 4B (Accurate) ✅"
echo "   • Gemma 3n Vision ✅"
echo "   • Accessibility fonts ✅"
echo ""
echo "🚀 To start EmpowerEd:"
echo "   ./run_empowered.sh"
echo ""
echo "📖 Or manually:"
echo "   source venv/bin/activate"
echo "   streamlit run app/main.py"
echo ""
echo "🌐 The app will open at: http://localhost:8501"
echo ""
echo -e "${BLUE}Thank you for helping make education accessible! 🌟${NC}"