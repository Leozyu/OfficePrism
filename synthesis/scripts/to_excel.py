import pandas as pd
import glob
import json
import os
def main():
    files = glob.glob('data/tasks_clean/tasks_*.json')
    all_tasks = []
    for f in files:
        domain_name = os.path.basename(f).replace('tasks_', '').replace('.json', '')
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for task in data:
                # Add or overwrite the domain column
                task['domain'] = domain_name
                # Convert nested dicts/lists to strings for Excel compatibility
                for k, v in task.items():
                    if isinstance(v, (dict, list)):
                        task[k] = json.dumps(v, ensure_ascii=False)
                all_tasks.append(task)
    if not all_tasks:
        print("No tasks found.")
        return
    df = pd.DataFrame(all_tasks)
    output_path = 'data/tasks_clean/tasks_all.xlsx'
    df.to_excel(output_path, index=False)
    print(f"Saved {len(all_tasks)} tasks to {output_path}")
if __name__ == "__main__":
    main()
