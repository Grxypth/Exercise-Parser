import json
import os

def categorize_difficulty(difficulty):
    if difficulty <= 3:
        return "Easy"
    elif difficulty <= 6:
        return "Medium"
    elif difficulty == 7:
        return "Hard"

def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def categorize_exercises(data):
    categorized_exercises = {}

    concept_exercises = data.get("exercises", {}).get("concept", [])
    practice_exercises = data.get("exercises", {}).get("practice", [])

    practice_map = {}
    for practice in practice_exercises:
        practice_name = practice['name']
        practice_difficulty = categorize_difficulty(practice.get('difficulty', 1))  
        for category in practice.get('practices', []):
            if category not in practice_map:
                practice_map[category] = []
            practice_map[category].append(f"{practice_name} ({practice_difficulty})")

    for exercise in concept_exercises:
        exercise_difficulty = categorize_difficulty(exercise.get('difficulty', 1)) 
        for category in exercise.get('concepts', []): 
            if category not in categorized_exercises:
                categorized_exercises[category] = []
            categorized_exercises[category].append(f"{exercise['name']} ({exercise_difficulty})")
    
    for category, exercises in practice_map.items():
        if category not in categorized_exercises:
            categorized_exercises[category] = []
        categorized_exercises[category].extend(exercises)
    
    return categorized_exercises

def write_report_to_file(categorized_exercises, output_file):
    with open(output_file, "w") as file:
        total_exercises = sum(len(exercises) for exercises in categorized_exercises.values())
        file.write(f"Total exercises: {total_exercises}\n\n")
        
        for category, exercises in categorized_exercises.items():
            file.write(f"Category: {category}\n")
            for exercise in exercises:
                file.write(f"- {exercise}\n")
            file.write("\n")

def main(input_json_file):
    language = input("For which language are you parsing the exercises for? ").strip()
    language_folder = os.path.join(os.getcwd(), language)
    os.makedirs(language_folder, exist_ok=True)
    output_txt_file = os.path.join(language_folder, f"{language}_exercises_report.txt")
    
    data = read_json_from_file(input_json_file)
    categorized_exercises = categorize_exercises(data)
    write_report_to_file(categorized_exercises, output_txt_file)

    print(f"Report saved to {output_txt_file}.")

input_json_file = "exercises.json"
main(input_json_file)
