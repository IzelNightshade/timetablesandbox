import json
import random
import os

# Directory where test JSON files will be saved
output_dir = "test_jsons"
os.makedirs(output_dir, exist_ok=True)

# Pre-defined subjects and their required periods
subjects_list = [
    {"Subject": "Math", "Periods": 5},
    {"Subject": "English", "Periods": 4},
    {"Subject": "Science", "Periods": 4},
    {"Subject": "History", "Periods": 3},
    {"Subject": "Art", "Periods": 2}
]

# Pre-defined teachers for the subjects (allowing multiple teachers per subject)
teachers_list = [
    {"Teacher": "Mr. Smith", "Subject": "Math"},
    {"Teacher": "Ms. Johnson", "Subject": "English"},
    {"Teacher": "Dr. Brown", "Subject": "Science"},
    {"Teacher": "Prof. Lee", "Subject": "History"},
    {"Teacher": "Mrs. Davis", "Subject": "Art"},
    {"Teacher": "Ms. Clark", "Subject": "Math"}
]

def generate_class_name(index):
    # Generate a class name like "Grade 10A", "Grade 10B", etc.
    letter = chr(65 + (index % 26))  # 65 = ASCII A
    return f"Grade 10{letter}"

def generate_classes(num_classes):
    classes = []
    # For each class, assign a random subset of subjects (at least 2 subjects)
    for i in range(num_classes):
        class_name = generate_class_name(i)
        # Choose a random number of subjects for this class (minimum 2, maximum all subjects)
        num_subjects = random.randint(2, len(subjects_list))
        # Randomly select subjects without duplicates
        selected_subjects = random.sample([s["Subject"] for s in subjects_list], num_subjects)
        classes.append({
            "class": class_name,
            "subjects": selected_subjects
        })
    return classes

def build_base_data(num_classes, periods_per_day=8):
    # Build the base valid JSON data dynamically based on number of classes
    base_data = {
        "classes": generate_classes(num_classes),
        "subjects": subjects_list,
        "teachers": teachers_list
    }
    return base_data

def inject_errors(data):
    """Randomly inject errors into the data dictionary."""
    # Copy data to avoid modifying the original
    data_with_error = json.loads(json.dumps(data))
    
    error_types = [
        "remove_key",             # remove a required key entirely
        "remove_field",           # remove a required field from an object
        "wrong_type",             # set a wrong type (e.g., string instead of list)
        "extra_subject",          # add a subject to a class that is not defined in subjects
        "exceed_periods"          # set a subject's periods to a value that exceeds available slots
    ]
    
    # Randomly decide how many errors to inject (0, 1, or 2)
    num_errors = random.choice([0, 1, 2])
    for _ in range(num_errors):
        error = random.choice(error_types)
        
        if error == "remove_key":
            # Remove a top-level key
            key_to_remove = random.choice(["classes", "subjects", "teachers"])
            if key_to_remove in data_with_error:
                print(f"Injecting error: Removing key '{key_to_remove}'")
                del data_with_error[key_to_remove]
        
        elif error == "remove_field":
            # Remove a required field from a random object in one of the lists
            list_key = random.choice(["classes", "subjects", "teachers"])
            if list_key in data_with_error and data_with_error[list_key]:
                obj = random.choice(data_with_error[list_key])
                if list_key == "classes":
                    field_to_remove = random.choice(["class", "subjects"])
                elif list_key == "subjects":
                    field_to_remove = random.choice(["Subject", "Periods"])
                else:  # teachers
                    field_to_remove = random.choice(["Teacher", "Subject"])
                if field_to_remove in obj:
                    print(f"Injecting error: Removing field '{field_to_remove}' from an item in '{list_key}'")
                    del obj[field_to_remove]
        
        elif error == "wrong_type":
            # Change a field to the wrong type.
            list_key = random.choice(["classes", "subjects", "teachers"])
            if list_key in data_with_error and data_with_error[list_key]:
                obj = random.choice(data_with_error[list_key])
                if list_key == "classes" and "subjects" in obj:
                    print("Injecting error: Setting 'subjects' field of a class to a string")
                    obj["subjects"] = "Math, English, Science"
                elif list_key == "subjects" and "Periods" in obj:
                    print("Injecting error: Setting 'Periods' field of a subject to a string")
                    obj["Periods"] = "five"
        
        elif error == "extra_subject":
            # Add an undefined subject to a random class
            if "classes" in data_with_error and data_with_error["classes"]:
                cls = random.choice(data_with_error["classes"])
                undefined_subject = "UndefinedSubject"
                if "subjects" in cls and undefined_subject not in cls["subjects"]:
                    print("Injecting error: Adding an undefined subject to a class")
                    cls["subjects"].append(undefined_subject)
        
        elif error == "exceed_periods":
            # Set a subject's required periods to a value that exceeds available slots
            if "subjects" in data_with_error and data_with_error["subjects"]:
                subj = random.choice(data_with_error["subjects"])
                # Assuming available slots is 5 days * periods_per_day = 40 (default periods_per_day=8)
                print(f"Injecting error: Setting subject '{subj.get('Subject', '<unknown>')}' periods to 50 (exceeds available slots)")
                subj["Periods"] = 50

    return data_with_error

def generate_test_jsons(num_files=5, num_classes=2, periods_per_day=8):
    base_data = build_base_data(num_classes, periods_per_day)
    for i in range(num_files):
        # Randomly decide whether to inject errors
        inject_error = random.choice([True, False])
        if inject_error:
            test_data = inject_errors(base_data)
        else:
            test_data = base_data
        
        file_name = f"test_{i+1}.json"
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, "w") as f:
            json.dump(test_data, f, indent=2)
        print(f"Generated {file_path}")

if __name__ == "__main__":
    try:
        num_classes = int(input("Enter the number of classes required: "))
    except ValueError:
        print("Invalid input. Using default of 2 classes.")
        num_classes = 2

    generate_test_jsons(num_files=10, num_classes=num_classes, periods_per_day=8)
