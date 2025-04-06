import csv
import os

def save_post_to_csv(post_data, filename):
    print("Записываю данные о постах в CSV файл")
    file_exists = os.path.isfile(filename)
    existing_entries = set()

    if file_exists:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                unique_key = (row["description"], row["publication_date"])
                existing_entries.add(unique_key)
    
    try:
        new_key = (post_data["description"], post_data["publication_date"])
        if new_key in existing_entries:
            print("Такой пост уже есть, пропускаю")
            return
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["URl", "description", "likes", "comments", "publication_date"])

            if not file_exists:
                writer.writeheader()

            writer.writerow(post_data)
    except: 
        print("Не получилось записать инфу про пост в CSV")