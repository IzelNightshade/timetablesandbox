import pandas as pd
import json

def convert_csv_to_json(classes_file, subjects_file, teachers_file, output_file):
    # Load CSV files
    classes_df = pd.read_csv(classes_file)
    subjects_df = pd.read_csv(subjects_file)
    teachers_df = pd.read_csv(teachers_file)
    
    # Convert classes data
    classes_data = []
    for _, row in classes_df.iterrows():
        class_entry = {
            "class": row["Class"],
            "subjects": row["Subjects"].split("; ")  # Split semicolon-separated subjects
        }
        classes_data.append(class_entry)
    
    # Convert subjects data
    subjects_data = subjects_df.to_dict(orient="records")
    
    # Convert teachers data
    teachers_data = teachers_df.to_dict(orient="records")
    
    # Structure everything into a JSON format
    timetable_data = {
        "classes": classes_data,
        "subjects": subjects_data,
        "teachers": teachers_data
    }
    
    # Save to JSON file
    with open(output_file, "w") as json_file:
        json.dump(timetable_data, json_file, indent=4)
    
    print(f"JSON file saved as {output_file}")

# Example usage
convert_csv_to_json("classes.csv", "subjects.csv", "teachers.csv", "data.json")
