# Animation GenAI 🎬✨

A powerful AI-driven tool that generates educational animations using Google's Gemini AI and the Manim library. Create beautiful mathematical and educational animations in the style of 3Blue1Brown by simply describing what you want to animate!
Live link :- https://animation-genai.streamlit.app/

## 🚀 Features

- **🤖 Advanced AI Generation**: Uses Google Gemini 2.5 Pro with enhanced system prompts for highly accurate animation code
- **🔄 Intelligent Self-Correction**: Automatically detects and fixes Manim syntax errors with up to 5 correction attempts
- **🎨 Streamlit Web Interface**: Modern, responsive web interface with beautiful cyan-themed UI
- **📚 3Blue1Brown Style**: Generates animations following the pedagogical approach of 3Blue1Brown
- **🔧 Auto-Fix System**: Automatically fixes common Manim syntax errors (deprecated methods, axes configuration, etc.)
- **🔒 Secure API Management**: Uses environment variables for API key security
- **📝 Script Editor**: View and edit generated scripts with syntax highlighting before re-rendering
- **📥 Download Support**: Download generated animations as MP4 files
- **⚙️ Configurable Settings**: Adjustable auto-fix options and correction attempt limits
- **🎯 Real-time Error Analysis**: Detailed error analysis with specific suggestions for manual fixes

## 📋 Prerequisites

- **Python 3.10 or higher**
- **Google AI Studio API key** ([Get one here](https://makersuite.google.com/app/apikey))
- **FFmpeg** (for video rendering)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Aafimalek/animation_genai
   cd animation_genai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_actual_gemini_api_key_here
   ```

4. **Install FFmpeg** (if not already installed)
   - **Windows**: Download from [FFmpeg.org](https://ffmpeg.org/download.html) or use `choco install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt update && sudo apt install ffmpeg`

## 🚀 Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:8501`

3. **Configure settings** (optional)
   - **Auto-fix syntax errors**: Enabled by default
   - **Max correction attempts**: Set between 1-5 (default: 3)

4. **Generate animations**
   - Enter a description of the animation you want to create
   - Click "🎬 Generate Animation"
   - Watch AI create your animation with automatic error correction!
   - Download the result as an MP4 file

## 📁 Project Structure

```
animation_genai/
├── app.py                    # Main Streamlit application with self-correction
├── check.py                 # Script to check available Gemini models
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create this)
├── .gitignore              # Git ignore file
├── .streamlit/
│   └── config.toml         # Streamlit UI theme configuration
├── style.css               # Custom CSS styling (optional)
├── README.md              
└── manim_work_*/          # Generated animation workspaces (auto-created)
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Your Google AI API key from AI Studio | Yes |

### Streamlit Theme

The app uses a beautiful dark theme with cyan accents configured in `.streamlit/config.toml`:
- **Primary Color**: `#00D4FF` (Bright cyan for tech/animation feel)
- **Background**: `#0C0E16` (Deep dark blue-black)
- **Secondary Background**: `#1A1D29` (Dark blue-grey for containers)
- **Text**: `#E8E9F3` (Soft white with blue tint)

### Model Configuration

The application uses `gemini-2.5-pro-preview-06-05` for optimal animation generation. You can check available models by running:

```bash
python check.py
```

## 📝 Example Prompts

Try these example prompts to get started:

### 🔢 Mathematics
- "Create an animation showing the Pythagorean theorem with a visual proof"
- "Animate a sine wave transforming into a cosine wave with equation display"
- "Show how the derivative of x squared equals 2x with step-by-step visual explanation"
- "Demonstrate the concept of limits approaching infinity with graphical representation"


## 🎨 Animation Features

The generated animations include:

- **📐 Mathematical Expressions**: LaTeX-rendered formulas using MathTex
- **🎬 Smooth Transitions**: Professional animations with proper timing and easing
- **🎨 Color Schemes**: Beautiful color palettes following 3Blue1Brown aesthetic
- **📚 Educational Structure**: Clear, pedagogical presentation of concepts
- **🔄 Interactive Elements**: Dynamic visualizations that build understanding step-by-step
- **⚡ Modern Syntax**: Uses latest Manim Community Edition v0.19.0+ features

### Self-Correction System
The app includes an intelligent self-correction system:

1. **First Attempt**: Generates script with enhanced prompts
2. **Auto-Fix**: Applies common syntax corrections automatically
3. **Error Analysis**: If rendering fails, analyzes the specific error type
4. **AI Correction**: Uses AI to fix the identified issues
5. **Multiple Attempts**: Retries up to 5 times with progressive improvements

### Settings Configuration
- **🔧 Auto-fix syntax errors**: Toggle automatic fixing of common issues
- **🔄 Max correction attempts**: Set between 1-5 attempts for error correction
- **📊 Real-time feedback**: View applied fixes and error analysis in real-time

1. **Rendering Failures with Auto-Correction**
   ```
   All 3 attempts failed
   ```
   **Solution**:
   - Check detailed error in expandable section
   - Try simpler prompts first
   - Increase max attempts to 5
   - Manually edit script using provided suggestions

### Getting Help

If you encounter persistent issues:

1. **Check Error Details**: Use the expandable "View Full Error Details" section
2. **Review Documentation**: 
   - [Manim Documentation](https://docs.manim.community/)
   - [Google AI Documentation](https://ai.google.dev/)
3. **Create an Issue**: Include:
   - Operating system and Python version
   - Full error message from expandable section
   - The prompt you were trying to use
   - Auto-fix settings and attempt count

## 🙏 Acknowledgments

- **[Manim Community](https://www.manim.community/)** - Incredible animation library and documentation
- **[3Blue1Brown](https://www.3blue1brown.com/)** - Inspiration for educational animation excellence
- **[Google AI](https://ai.google.dev/)** - Powerful Gemini AI models and API
- **[Streamlit](https://streamlit.io/)** - Excellent framework for rapid prototyping and beautiful UIs
---

**🎬✨ Happy Animating!**

*Transform complex concepts into beautiful, understandable visual stories with the power of AI and mathematics.*

[![Made with Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-FF6B6B.svg)](https://streamlit.io/)
[![Powered by Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-00D4FF.svg)](https://ai.google.dev/)
[![Built with Manim](https://img.shields.io/badge/Built%20with-Manim-1A1D29.svg)](https://www.manim.community/)
