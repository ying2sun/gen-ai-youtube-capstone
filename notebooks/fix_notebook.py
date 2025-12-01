import json

# Replace with your actual filename
filename = "/workspaces/Capstone/notebooks/appendix_model_benchmarking.ipynb" 

with open(filename, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Safely remove the widgets block
if 'widgets' in data.get('metadata', {}):
    del data['metadata']['widgets']
    print("Success! Widgets removed.")
    
    # Save the fixed file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=1)
else:
    print("No widgets found to remove.")
