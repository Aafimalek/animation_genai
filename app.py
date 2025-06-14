import streamlit as st
import google.generativeai as genai
import subprocess
import os
import tempfile
import shutil
from pathlib import Path
import time
import uuid
from dotenv import load_dotenv

# Configure the page
st.set_page_config(
    page_title="Manim Animation Generator",
    page_icon="🎬",
    layout="wide"
)

# Title and description
st.title("🎬 Manim Animation Generator")
st.markdown("Generate 2D educational animations in the style of 3Blue1Brown using AI")

# Load API key from .env file instead of sidebar
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Use the more capable Gemini 1.5 Pro model for better animation generation
model = genai.GenerativeModel('models/gemini-2.5-pro-preview-06-05')

def generate_manim_script(prompt):
    """Generate a Manim script using Gemini API"""
    system_prompt = """You are an expert in creating educational animations using the Manim library (Community Edition v0.19.0), exactly like 3Blue1Brown's style.

Generate a complete Python script that:
1. Uses Manim to create a 2D educational animation
2. Explains the concept clearly with visual elements
3. Includes proper animations, text, and mathematical expressions
4. Follows 3Blue1Brown's pedagogical approach
5. Has a clean, professional look with good color schemes

CRITICAL SYNTAX REQUIREMENTS for Manim Community v0.19.0:
- Use .move_to(ORIGIN) or .center() instead of .to_center()
- Use .shift() for positioning adjustments
- Use MathTex() for mathematical expressions (not TexMobject)
- Use Text() for regular text (not TextMobject)
- For axes: Use Axes(x_range=[min, max], y_range=[min, max]) - DO NOT put x_range/y_range in axis config
- Use self.play() for animations, self.add() for static objects
- Use self.wait() for pauses between animations
- For plotting graphs: Use axes.plot(function, x_range=[min, max]) NOT axes.get_graph()
- For graph labels: Use axes.get_graph_label() or create Text/MathTex separately
- For axis labels: Use axes.get_axis_labels() or create labels manually
- Always define functions with lambda or def before plotting

IMPORTANT AXES CONFIGURATION:
- NEVER put x_range or y_range inside x_axis_config or y_axis_config
- Correct: Axes(x_range=[-3, 3], y_range=[-2, 2])
- Wrong: Axes(x_axis_config={"x_range": [-3, 3]}, y_axis_config={"y_range": [-2, 2]})
- Axis configs should only contain visual properties like font_size, color, etc.

The script MUST follow this structure:
- Start with: from manim import *
- Create a Scene class named 'MainScene' that inherits from Scene
- Implement the construct(self) method with the animation logic
- Use animations like Write, Create, Transform, FadeIn, FadeOut
- Include mathematical expressions with MathTex when relevant
- Use colors from Manim's color palette (BLUE, RED, GREEN, YELLOW, etc.)
- Have smooth transitions and proper timing
- Be educational and engaging

IMPORTANT: 
- The scene class MUST be named 'MainScene' and inherit from Scene
- Return ONLY pure Python code
- Do NOT use markdown formatting
- Do NOT wrap the code in ```python``` or ``` blocks
- Start directly with 'from manim import *'
- Use ONLY modern Manim Community syntax

Example structure:
from manim import *

class MainScene(Scene):
    def construct(self):
        # Your animation code here
        title = Text("Your Title")
        title.move_to(ORIGIN)
        self.play(Write(title))
        self.wait()
        
        # For axes (correct syntax):
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=6,
            y_length=4
        )
        
        # For plotting graphs (correct syntax):
        func = lambda x: x**2
        graph = axes.plot(func, x_range=[-2, 2], color=BLUE)
        self.play(Create(axes), Create(graph))"""

    try:
        full_prompt = f"{system_prompt}\n\nCreate an educational animation about: {prompt}"
        
        response = model.generate_content(full_prompt)
        script = response.text.strip()
        
        # Clean the response - remove markdown code blocks if present
        if script.startswith('```python'):
            script = script[9:]  # Remove ```python
        if script.startswith('```'):
            script = script[3:]   # Remove ```
        if script.endswith('```'):
            script = script[:-3]  # Remove trailing ```
        
        return script.strip()
    except Exception as e:
        st.error(f"Error generating script: {str(e)}")
        return None

def auto_fix_manim_syntax(script_content):
    """Automatically fix common Manim syntax issues"""
    fixes_applied = []
    
    # Fix .to_center() -> .move_to(ORIGIN)
    if '.to_center()' in script_content:
        script_content = script_content.replace('.to_center()', '.move_to(ORIGIN)')
        fixes_applied.append("Replaced .to_center() with .move_to(ORIGIN)")
    
    # Fix TexMobject -> MathTex
    if 'TexMobject' in script_content:
        script_content = script_content.replace('TexMobject', 'MathTex')
        fixes_applied.append("Replaced TexMobject with MathTex")
    
    # Fix TextMobject -> Text
    if 'TextMobject' in script_content:
        script_content = script_content.replace('TextMobject', 'Text')
        fixes_applied.append("Replaced TextMobject with Text")
    
    # Fix incorrect axes configuration (x_range/y_range in axis config)
    import re
    
    # Pattern to find Axes with x_axis_config or y_axis_config containing x_range/y_range
    axes_pattern = r'Axes\((.*?)\)'
    axes_matches = re.findall(axes_pattern, script_content, re.DOTALL)
    
    for match in axes_matches:
        original_axes = f'Axes({match})'
        fixed_axes = fix_axes_config(original_axes)
        if fixed_axes != original_axes:
            script_content = script_content.replace(original_axes, fixed_axes)
            fixes_applied.append("Fixed Axes configuration - moved x_range/y_range out of axis configs")
    
    # Fix get_graph syntax (basic pattern)
    pattern = r'\.get_graph\((.*?),\s*x_range=\[(.*?)\](.*?)\)'
    matches = re.findall(pattern, script_content)
    if matches:
        for match in matches:
            old_syntax = f'.get_graph({match[0]}, x_range=[{match[1]}]{match[2]})'
            new_syntax = f'.plot({match[0]}, x_range=[{match[1]}]{match[2]})'
            script_content = script_content.replace(old_syntax, new_syntax)
        fixes_applied.append("Replaced .get_graph() with .plot() for graph plotting")
    
    return script_content, fixes_applied

def fix_axes_config(axes_string):
    """Fix Axes configuration by moving x_range/y_range out of axis configs"""
    import re
    
    # Extract x_range and y_range from axis configs
    x_range_pattern = r'x_axis_config\s*=\s*\{[^}]*"x_range"\s*:\s*(\[[^\]]+\])[^}]*\}'
    y_range_pattern = r'y_axis_config\s*=\s*\{[^}]*"y_range"\s*:\s*(\[[^\]]+\])[^}]*\}'
    
    x_range_match = re.search(x_range_pattern, axes_string)
    y_range_match = re.search(y_range_pattern, axes_string)
    
    if not (x_range_match or y_range_match):
        return axes_string  # No fixes needed
    
    # Extract the existing parameters
    axes_content = axes_string[5:-1]  # Remove 'Axes(' and ')'
    
    new_params = []
    
    # Add x_range if found in x_axis_config
    if x_range_match:
        x_range = x_range_match.group(1)
        new_params.append(f'x_range={x_range}')
        # Remove x_range from x_axis_config
        axes_content = re.sub(r'"x_range"\s*:\s*\[[^\]]+\],?\s*', '', axes_content)
    
    # Add y_range if found in y_axis_config
    if y_range_match:
        y_range = y_range_match.group(1)
        new_params.append(f'y_range={y_range}')
        # Remove y_range from y_axis_config
        axes_content = re.sub(r'"y_range"\s*:\s*\[[^\]]+\],?\s*', '', axes_content)
    
    # Clean up empty configs
    axes_content = re.sub(r'x_axis_config\s*=\s*\{\s*\},?\s*', '', axes_content)
    axes_content = re.sub(r'y_axis_config\s*=\s*\{\s*\},?\s*', '', axes_content)
    
    # Combine new parameters with existing ones
    if axes_content.strip():
        all_params = ', '.join(new_params) + ', ' + axes_content
    else:
        all_params = ', '.join(new_params)
    
    return f'Axes({all_params})'

def save_and_render_script(script_content, session_id, auto_fix=True):
    """Save the script and render it with Manim"""
    try:
        # Apply automatic fixes if enabled
        if auto_fix:
            script_content, fixes_applied = auto_fix_manim_syntax(script_content)
            if fixes_applied:
                st.info(f"🔧 **Auto-fixes Applied**: {', '.join(fixes_applied)}")
        
        # Create a unique directory for this session
        work_dir = Path(f"manim_work_{session_id}")
        work_dir.mkdir(exist_ok=True)
        
        # Save the script with UTF-8 encoding
        script_path = work_dir / "animation.py"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Verify the file was created
        if not script_path.exists():
            st.error(f"Failed to create script file at {script_path}")
            return None
        
        # Run Manim to render the animation - use absolute path and specify scene
        script_abs_path = script_path.resolve()
        cmd = [
            "manim", 
            str(script_abs_path),
            "MainScene",  # Specify the scene class name
            "-ql",  # Low quality for faster rendering
            "--disable_caching",  # Prevent caching issues
            f"--media_dir={work_dir.resolve()}/media"
        ]
        
        # Execute Manim with proper encoding handling for Windows
        import sys
        
        # Set environment variables for better Unicode support
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONLEGACYWINDOWSFSENCODING'] = '0'
        
        try:
            # Try UTF-8 first
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                encoding='utf-8',
                errors='ignore',  # Ignore problematic characters
                env=env
            )
        except UnicodeDecodeError:
            # Fallback to system default encoding with error handling
            try:
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=False,  # Get bytes instead
                    env=env
                )
                # Manually decode with error handling
                stdout = result.stdout.decode('utf-8', errors='replace') if result.stdout else ""
                stderr = result.stderr.decode('utf-8', errors='replace') if result.stderr else ""
                
                # Create a result-like object
                class ProcessResult:
                    def __init__(self, returncode, stdout, stderr):
                        self.returncode = returncode
                        self.stdout = stdout
                        self.stderr = stderr
                
                result = ProcessResult(result.returncode, stdout, stderr)
                
            except Exception as e:
                st.error(f"Encoding error during subprocess execution: {str(e)}")
                return None
        
        if result.returncode == 0:
            # Find the generated video file
            media_dir = work_dir / "media" / "videos" / "animation" / "480p15"
            
            # Also check for common alternative paths
            possible_paths = [
                media_dir,
                work_dir / "media" / "videos" / "480p15",
                work_dir / "media" / "videos",
                work_dir / "media"
            ]
            
            video_path = None
            for path in possible_paths:
                if path.exists():
                    video_files = list(path.glob("*.mp4"))
                    if video_files:
                        video_path = str(video_files[0])
                        break
            
            if video_path:
                return video_path
            else:
                st.error("Video file not found after rendering")
                st.error(f"Checked paths: {[str(p) for p in possible_paths]}")
                return None
        else:
            st.error(f"Manim rendering failed:")
            # Show detailed error information
            st.error(f"Return code: {result.returncode}")
            
            # Parse common errors and provide helpful suggestions
            if "multiple values for argument 'x_range'" in result.stderr:
                st.error("⚠️ **Axes Configuration Error**: x_range/y_range conflict detected.")
                st.error("💡 **Suggestion**: Use `Axes(x_range=[...], y_range=[...])` instead of putting ranges in axis configs")
                
            if "AttributeError" in result.stderr:
                st.error("⚠️ **Syntax Error Detected**: The generated script contains outdated Manim syntax.")
                if "to_center" in result.stderr:
                    st.error("💡 **Suggestion**: Replace `.to_center()` with `.move_to(ORIGIN)` or `.center()`")
                if "TexMobject" in result.stderr:
                    st.error("💡 **Suggestion**: Replace `TexMobject` with `MathTex`")
                if "TextMobject" in result.stderr:
                    st.error("💡 **Suggestion**: Replace `TextMobject` with `Text`")
            
            if "TypeError" in result.stderr and "get_graph" in result.stderr:
                st.error("⚠️ **Graph Plotting Error**: Outdated graph plotting syntax detected.")
                st.error("💡 **Suggestion**: Replace `axes.get_graph(func, x_range=[...])` with `axes.plot(func, x_range=[...])`")
                st.error("💡 **Note**: Make sure to define your function first: `func = lambda x: your_function`")
            
            with st.expander("View Full Error Details"):
                st.code(f"STDOUT:\n{result.stdout}", language="text")
                st.code(f"STDERR:\n{result.stderr}", language="text")
            
            return None
            
    except Exception as e:
        st.error(f"Error in rendering: {str(e)}")
        return None

def main():
    # Initialize session state
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if 'generated_script' not in st.session_state:
        st.session_state.generated_script = None
    
    if 'video_path' not in st.session_state:
        st.session_state.video_path = None
    
    # Main interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Input")
        prompt = st.text_area(
            "Describe the educational concept you want to animate:",
            placeholder="e.g., Explain the Pythagorean theorem with a visual proof",
            height=100
        )
        
        generate_button = st.button("🎬 Generate Animation", type="primary")
        
        # Auto-fix toggle
        auto_fix_enabled = st.checkbox("🔧 Auto-fix common syntax errors", value=True, 
                                     help="Automatically fix common outdated Manim syntax")
        
        if generate_button and prompt and api_key:
            with st.spinner("Generating Manim script..."):
                script = generate_manim_script(prompt)
                
            if script:
                st.session_state.generated_script = script
                st.session_state.session_id = str(uuid.uuid4())  # New session for new generation
                
                with st.spinner("Rendering animation... This may take a moment..."):
                    video_path = save_and_render_script(script, st.session_state.session_id, auto_fix_enabled)
                    st.session_state.video_path = video_path
                
                if video_path:
                    st.success("Animation generated successfully!")
                else:
                    st.error("Failed to render animation. Please check your script.")
        
        elif generate_button and not api_key:
            st.error("Please enter your Gemini API key in the sidebar")
        elif generate_button and not prompt:
            st.error("Please enter a prompt")
    
    with col2:
        st.header("🎥 Output")
        
        if st.session_state.video_path and os.path.exists(st.session_state.video_path):
            # Display the video
            with open(st.session_state.video_path, 'rb') as video_file:
                video_bytes = video_file.read()
                st.video(video_bytes)
            
            # Download button
            st.download_button(
                label="📥 Download Animation",
                data=video_bytes,
                file_name=f"manim_animation_{int(time.time())}.mp4",
                mime="video/mp4"
            )
        else:
            st.info("Generated animation will appear here")
    
    # Show generated script
    if st.session_state.generated_script:
        st.header("🐍 Generated Manim Script")
        with st.expander("View/Edit Script", expanded=False):
            edited_script = st.text_area(
                "Manim Python Script:",
                value=st.session_state.generated_script,
                height=300
            )
            
            if st.button("🔄 Re-render with Edited Script"):
                auto_fix_rerender = st.checkbox("🔧 Apply auto-fixes to edited script", value=True)
                with st.spinner("Rendering edited script..."):
                    st.session_state.session_id = str(uuid.uuid4())  # New session
                    video_path = save_and_render_script(edited_script, st.session_state.session_id, auto_fix_rerender)
                    st.session_state.video_path = video_path
                    st.session_state.generated_script = edited_script
                
                if video_path:
                    st.success("Animation re-rendered successfully!")
                    st.rerun()

if __name__ == "__main__":
    main()