import os
import sys
from git import Repo
import google.generativeai as genai
from dotenv import load_dotenv
import re
# Load environment variables
load_dotenv()

# Set up Gemini API key
GEMINI_API_KEY = "AIzaSyCWSnVxKsmtEBJqHq_0C_eqTG-xu8JN67Y"
if GEMINI_API_KEY == "GEMINI_API_KEY":
    print("Error: GEMINI_API_KEY environment variable is not set.")
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)

import shutil

def clone_repo(repo_url, clone_dir):
    """Clone the GitHub repository to the local directory, ensuring a clean clone."""
    if os.path.exists(clone_dir):
        print(f"Removing existing directory {clone_dir}...")
        shutil.rmtree(clone_dir)  # Remove old clone

    print(f"Cloning repository from {repo_url}...")
    Repo.clone_from(repo_url, clone_dir)
    return clone_dir

def list_files(directory):
    """List only source code files in the cloned repository."""
    files = []
    for root, _, filenames in os.walk(directory):
        # Skip the .git directory
        if ".git" in root:
            continue
        for filename in filenames:
            # Include only common code file types
            if filename.endswith((".py", ".c", ".cpp", ".java", ".js", ".ts", ".html", ".css")):
                files.append(os.path.relpath(os.path.join(root, filename), directory))
    return files

def read_file(file_path):
    """Read the contents of the specified file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# Configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def grade_code(file_content, file_name):
    """Send the code to Gemini 2.0 Flash for grading."""
    
    prompt = f"""

AI-Powered Python Code Grading Assistant

### Task Description:
You are an AI-powered code grading assistant specializing in evaluating Python submissions. Your task is to analyze a given Python code snippet and return a **formal, structured evaluation report in HTML format only**.

### **Critical Instructions (STRICTLY FOLLOW THESE)**:
- **Do NOT use emojis, symbols, or decorative characters.** The output must be formal and professional.
- **Return only valid, clean HTML5**—strictly no JSON, Markdown, or raw text.
- **No `<style>` tags that cause formatting issues.** Use clean inline CSS for structured styling.
- **Headings (`h1`, `h2`, etc.) should be centered and well-formatted.**
- **Ensure zero broken elements, extraneous spaces, or unnecessary new lines in the output.**
- **Completely remove any Markdown artifacts (` ```html ` or similar issues).**
- **Do NOT use colors except black text on a white background.**
- **Ensure proper indentation, spacing, and structure in the generated HTML.**

---

### **Evaluation Criteria & Scoring:**
Each category is **scored from 0 to 10** (increments of 0.5) based on the following parameters:

| **Criteria**      | **Score Range (0-10)** | **Evaluation Focus** |
|-------------------|-----------------|--------------------------------|
| **Correctness**   | 0-10            | Does the code function as expected? Any syntax/logical errors? |
| **Efficiency**    | 0-10            | Is the time/space complexity optimal? Are unnecessary loops avoided? |
| **Readability**   | 0-10            | Are variable names meaningful? Is the code easy to understand? |
| **Style**         | 0-10            | Does the code follow best practices (PEP8, Google style guide)? |
| **Security**      | 0-10            | Are there vulnerabilities (e.g., SQL injections, memory leaks)? |
| **Fragility**     | 0-10            | How prone is the code to breaking under minor changes or edge cases? |

---

### **Expected HTML Output Format (STRICT GUIDELINES)**:
- **Return valid, professional HTML5 only.**
- **The main document heading (`h1`) must be centered.**
- The document must be **structured** with the following sections:
  1. **Overall Results**: Display scores in a clean table.
  2. **Flagged Code Sections**: Show problematic code snippets with comments.
  3. **Recommendations for Improvement**: Provide structured, actionable insights.
  4. **Corrected Code Snippets**: Display the optimized code with a functional **copy-to-clipboard** button.

- **Layout must ensure:**
  - **A white background with black text**—no unnecessary colors.
  - **Headings (`h1, h2, h3`) should be centered and have bottom borders.**
  - **Tables** must have borders and clearly separate data.
  - **Code blocks** must use a **monospaced font, light gray background, and proper padding**.
  - **Copy-to-Clipboard buttons** should be functional and placed **directly below the respective code blocks**.

---

### **Strict HTML Output Example (Compliant with Above Guidelines):**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Code Evaluation Report</title>
    <style>
    <style>
        /* The body should have a white background with black text for a formal look */
        body :
            font-family: Arial, sans-serif;
            margin: 40px;
            background: white;
            color: black;
        

        /* The main heading should be centered */
        h1 :
            text-align: center;
        

        /* Headings should have a bottom border for emphasis */
        h2, h3 :
            text-align: center;
            border-bottom: 2px solid black;
            padding-bottom: 5px;
        

        /* Tables should have borders to clearly separate data */
        table :
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        
        th, td :
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        
        th :
            background: #f0f0f0;
        

        /* Code blocks should have a light gray background with padding and a monospaced font */
        .code-block :
            background: #eee;
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
            white-space: pre-wrap;
        

        /* The copy button should have a black background with white text and darken when hovered */
        .copy-btn :
            margin-top: 5px;
            padding: 5px 10px;
            background: black;
            color: white;
            border: none;
            cursor: pointer;
        
        .copy-btn:hover  : background: #444;
        
    </style>
</head>
<body>

    <h1>Python Code Evaluation Report</h1>

    <h2>1. Overall Results</h2>
    <table>
        <tr><th>Criteria</th><th>Score (0-10)</th></tr>
        <tr><td>Correctness</td><td>7.5</td></tr>
        <tr><td>Efficiency</td><td>6.5</td></tr>
        <tr><td>Readability</td><td>8.0</td></tr>
        <tr><td>Style</td><td>7.0</td></tr>
        <tr><td>Security</td><td>9.0</td></tr>
        <tr><td>Fragility</td><td>5.5</td></tr>
    </table>

    <h2>2. Flagged Code Sections</h2>
    <div class="code-block">
        <code>for i in range(len(my_list)): print(my_list[i])</code>
    </div>
    <p><strong>Comment:</strong> This loop unnecessarily iterates using an index. A direct iteration is preferred.</p>

    <h2>3. Recommendations for Improvement</h2>
    <p>Instead of iterating using an index, consider using a direct iteration method to enhance readability and performance.</p>

    <h2>4. Corrected Code Snippets</h2>
    <div class="code-block" id="corrected-code">
        <code>for item in my_list: print(item)</code>
    </div>
    <button class="copy-btn" onclick="copyToClipboard()">Copy to Clipboard</button>

    <script>
        function copyToClipboard() 
    </script>

</body>
</html>

---

### **Final Notes:**
- DONT USE <pre>```html
- **No emojis** or unnecessary symbols are included.
- **Main heading (h1) is centered** as requested.
- **Consistent and professional HTML structure**.
- **Ensures clarity and readability in code evaluation**.

Outcome should be
No more emojis or extraneous symbols.
No broken/unwanted HTML rendering.
Fully formatted, clean HTML5 structure.
Ensures the report is easy to read, interpret, and act upon.
No unnecessary Markdown artifacts (```html blocks).

    File: {file_name}
    
    Code:
    ```
    {file_content}
    ```
    """

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content([{"text": prompt}])

        grading_result = response.text if response else "No response received."

        # Save results to an HTML file
        save_report_as_html(file_name, file_content, grading_result)

        return grading_result

    except Exception as e:
        return f"Error in API call: {e}"
    
def save_report_as_html(file_name, original_code, grading_result):
    """Generate an HTML report from the grading results."""

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Code Grading Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; padding: 20px; background-color: #f8f9fa; }}
            h1, h2 {{ color: #333; }}
            pre {{ background: #eee; padding: 10px; border-radius: 5px; white-space: pre-wrap; }}
            .container {{ max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); }}
            .feedback {{ color: #d9534f; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Code Grading Report</h1>
            <h2> File Graded: {file_name}</h2>
            
            <h2> Original Code:</h2>
            <pre>{original_code}</pre>

            <h2> Grading Results:</h2>
            <pre>{grading_result}</pre>

            <h2> Suggestions & Improvements:</h2>
            <p class="feedback">{grading_result}</p>
        </div>
    </body>
    </html>
    """


    """     # Save the report to `index.html`
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(html_content)
        # Read the HTML file
        content = file.read()

        # Remove all occurrences of Markdown-style ```html and ```
        cleaned_content = re.sub(r"```html", "", content)
        cleaned_content = re.sub(r"```", "", cleaned_content)

        # Write the cleaned content back to the file
        with open("index_cleaned.html", "w", encoding="utf-8") as file:
            file.write(cleaned_content)

        print("Cleanup completed. The cleaned file is saved as 'index_cleaned.html'.")

    print("\n Report saved to `index.html`. Open it in your browser to view results.")
    

    """



    # Step 2: Open `index.html` for reading and process it to remove ```html artifacts
    with open("index.html", "r", encoding="utf-8") as file:
        content = file.read()

    # Step 3: Remove all occurrences of Markdown-style ```html and ```
    cleaned_content = re.sub(r"```", "", content)
    cleaned_content = re.sub(r"```html", "", cleaned_content)

    # Step 4: Write the cleaned content back to `index.html`
    with open("indexfixed.html", "w", encoding="utf-8") as file:
        file.write(cleaned_content)

    print("Cleanup completed. The cleaned file is saved as 'index.html'. Open it in your browser to view results.")














if __name__ == "__main__":
    repo_url = input("Enter the GitHub repository URL: ")
    clone_dir = "cloned_repo"
    
    clone_repo(repo_url, clone_dir)
    
    files = list_files(clone_dir)
    if not files:
        print("No files found in the repository.")
        sys.exit(1)
    
    print("Files in repository:")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")
    
    file_index = int(input("Enter the number of the file to grade: ")) - 1
    if file_index < 0 or file_index >= len(files):
        print("Invalid file selection.")
        sys.exit(1)
    
    file_path = os.path.join(clone_dir, files[file_index])
    file_name = files[file_index]
    print(f"Checking file: {file_name}")  # Print the file being checked
    
    file_content = read_file(file_path)
    
    print("\nGrading the code...\n")
    grading_result = grade_code(file_content, file_name)
    
    print("\n--- Grading Result ---\n")
    print(grading_result)
