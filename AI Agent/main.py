from google import genai
import os
import json
import shutil

client = genai.Client()

folder_path = input("Enter the path of the folder to sort: ")
files = [f for f in os.listdir(folder_path) if f.lower() != "desktop.ini"]

response = client.models.generate_content(
	model="gemini-2.5-flash-lite",
	contents=f"Organize these files into logical category folders based on their names and extensions:\n{files}",
	config={
		"response_mime_type": "application/json",
		"response_schema": {
		    "type": "ARRAY",
		    "description": "A list of folder allocations.",
		    "items": {
		        "type": "OBJECT",
		        "properties": {
		            "folder_name": {
		                "type": "STRING",
		                "description": "The category or folder name (e.g., 'Images', 'Documents')."
		            },
		            "files": {
		                "type": "ARRAY",
		                "items": {"type": "STRING"},
		                "description": "The list of filenames that belong inside this folder."
		            }
		        },
		        "required": ["folder_name", "files"]
		    }
		}
	}
)

sorted_folders = json.loads(response.text)

print(json.dumps(sorted_folders, indent=4))

sorted_folders = {item["folder_name"]: item["files"] for item in sorted_folders}

authorization = input("Authorize the sorting by entering 'authorized' in reply to this prompt. ").lower()
if authorization == "authorized":

	for folder_name, file_list in sorted_folders.items():
	    destination_folder = os.path.join(folder_path, folder_name)
	    
	    if not os.path.exists(destination_folder):
	        os.makedirs(destination_folder)
	        print(f"Created folder: {folder_name}/")
	
	    for filename in file_list:
	        source_file_path = os.path.join(folder_path, filename)
	        destination_file_path = os.path.join(destination_folder, filename)
	
	        if os.path.exists(source_file_path):
	            try:
	                shutil.move(source_file_path, destination_file_path)
	                print(f"  -> Moved: {filename} to {folder_name}/")
	            except Exception as e:
	                print(f"  [Error] Could not move {filename}: {e}")
	        else:
	            print(f"  [Warning] File not found (skipping): {filename}")