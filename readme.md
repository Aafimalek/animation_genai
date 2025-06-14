# Animation GenAI 🎬✨

A powerful AI-driven tool that generates educational animations using Google's Gemini AI and the Manim library. Create beautiful mathematical and educational animations in the style of 3Blue1Brown by simply describing what you want to animate!

## 🚀 Features

- **AI-Powered Animation Generation**: Uses Google Gemini 2.5 Pro for highly accurate animation code generation
- **Streamlit Web Interface**: User-friendly web interface with real-time preview
- **3Blue1Brown Style**: Generates animations following the pedagogical approach of 3Blue1Brown
- **Auto-Fix System**: Automatically fixes common Manim syntax errors for better compatibility
- **Secure API Management**: Uses environment variables for API key security
- **Script Editor**: View and edit generated scripts before re-rendering
- **Download Support**: Download generated animations as MP4 files

## 📋 Prerequisites

- **Python 3.8 or higher**
- **Google AI Studio API key** ([Get one here](https://makersuite.google.com/app/apikey))
- **FFmpeg** (for video rendering)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
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

3. **Generate animations**
   - Enter a description of the animation you want to create
   - Click "🎬 Generate Animation"
   - Watch AI create your animation in real-time!
   - Download the result as an MP4 file

## 📁 Project Structure

```
animation_genai/
├── app.py              # Main Streamlit application
├── check.py           # Script to check available Gemini models
├── requirements.txt   # Python dependencies
├── .env              # Environment variables (create this)
├── .gitignore        # Git ignore file
├── README.md         # This file
└── manim_work_*/     # Generated animation workspaces (auto-created)
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Your Google AI API key from AI Studio | Yes |

### Model Configuration

The application uses `gemini-2.5-pro-preview-06-05` for optimal animation generation. You can check available models by running:

```bash
python check.py
```

## 📝 Example Prompts

Try these example prompts to get started:

### Mathematics
- "Create an animation showing the Pythagorean theorem with a visual proof"
- "Animate a sine wave transforming into a cosine wave"
- "Show how the derivative of x squared equals 2x with visual explanation"
- "Demonstrate the concept of limits approaching infinity"

### Linear Algebra
- "Visualize matrix multiplication with animated vectors"
- "Show how eigenvectors behave under matrix transformation"
- "Animate the process of solving a system of linear equations"

### Calculus
- "Create a visualization of integration as area under a curve"
- "Show the relationship between a function and its derivative"
- "Animate the concept of Taylor series expansion"

### Physics
- "Visualize wave interference patterns"
- "Show projectile motion with velocity vectors"
- "Animate simple harmonic motion"

## 🎨 Animation Features

The generated animations include:
- **Mathematical Expressions**: LaTeX-rendered formulas using MathTex
- **Smooth Transitions**: Professional animations with proper timing
- **Color Schemes**: Beautiful color palettes following 3Blue1Brown style
- **Educational Structure**: Clear, pedagogical presentation of concepts
- **Interactive Elements**: Dynamic visualizations that build understanding

## 🛠️ Advanced Usage

### Custom Script Editing
1. Generate an animation using AI
2. View the generated script in the expandable section
3. Edit the script as needed
4. Click "🔄 Re-render with Edited Script"

### Troubleshooting Common Issues
The app provides detailed error messages and suggestions for common issues:
- **Axes Configuration Errors**: Clear guidance on proper syntax
- **Syntax Errors**: Automatic detection and fixing suggestions
- **Graph Plotting Issues**: Modern syntax recommendations


## 🆘 Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   Error: Please enter your Gemini API key
   ```
   - Ensure your `.env` file exists in the project root
   - Check that `GOOGLE_API_KEY` is correctly set
   - Verify your API key has the necessary permissions

2. **Manim Installation Issues**
   ```
   Error: manim command not found
   ```
   - Install Manim: `pip install manim`
   - Install FFmpeg (see installation section)
   - Restart your terminal/command prompt

3. **Import/Encoding Errors**
   ```
   UnicodeDecodeError or similar
   ```
   - The app includes automatic encoding handling
   - Try running with administrator privileges on Windows
   - Ensure your system supports UTF-8 encoding

4. **Rendering Failures**
   ```
   Manim rendering failed
   ```
   - Check the detailed error in the expandable section
   - Enable auto-fix for common syntax issues
   - Try simpler prompts first to test your setup

### Getting Help

If you encounter issues:
1. Check the error details in the expandable "View Full Error Details" section
2. Review the [Manim Documentation](https://docs.manim.community/)
3. Check [Google AI Documentation](https://ai.google.dev/)
4. Create an issue in this repository with:
   - Your operating system
   - Python version
   - Full error message
   - The prompt you were trying to use

## 🔄 Updates & Changelog

### Version Features
- **v1.0**: Initial release with Gemini 2.5 Pro integration
- **Auto-fix System**: Intelligent syntax error correction
- **Enhanced Error Handling**: Detailed error messages and suggestions
- **Script Editor**: In-app script editing and re-rendering

## 🙏 Acknowledgments

- **[Manim Community](https://www.manim.community/)** - Amazing animation library
- **[3Blue1Brown](https://www.3blue1brown.com/)** - Inspiration for educational animation style
- **[Google AI](https://ai.google.dev/)** - Powerful Gemini AI models
- **[Streamlit](https://streamlit.io/)** - Excellent web framework for rapid prototyping

**Happy Animating!** 🎬✨

*Create educational content that makes complex concepts simple and beautiful.*