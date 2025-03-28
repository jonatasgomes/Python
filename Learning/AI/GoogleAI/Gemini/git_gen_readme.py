import os, env
import google.generativeai as genai

genai.configure(api_key=env.GEMINI_API_KEY)  # Replace with your actual API key
# models = genai.list_models()
# for model in models:
#     print(model.name)
# exit()

def scan_folders(repo_path):
    folder_set = set()
    for root, dirs, files in os.walk(repo_path):
        if any(f.endswith(".py") for f in files):  # Only consider folders containing .py files
            folder_set.add(root.replace(repo_path, "").strip(os.sep))
    return sorted(folder_set)

def generate_readme(folders):
    prompt = (
        "I have a Python GitHub repository with the following folder structure: \n"
        + "\n".join(folders)
        + "\n\nPlease generate a README.md file that briefly describes the repository and summarizes the purpose of each folder."
    )
    
    response = genai.GenerativeModel("gemini-2.0-flash").generate_content(prompt)
    return response.text

def main():
    repo_path = "/Users/jonatas/Apps/Python/"  # Replace with your local repo path
    folders = scan_folders(repo_path)
    readme_content = generate_readme(folders)
    
    with open(os.path.join(os.path.dirname(__file__), "README.md"), "w") as f:
        f.write(readme_content)
    
    print("README.md generated successfully!")

if __name__ == "__main__":
    main()
