input_file = "Full database for raj.txt"
output_file = "Full_database_for_raj_cleaned.txt"

cleaned_lines = []
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        # Remove bold markers
        line = line.replace("**", "")
        
        # Skip lines that are only separators
        if set(line.strip()) <= {"-", "="} and len(line.strip()) > 5:
            continue
        
        cleaned_lines.append(line)

with open(output_file, "w", encoding="utf-8") as f:
    f.writelines(cleaned_lines)

print("✅ Cleaned file saved as", output_file)
