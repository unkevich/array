import requests
from collections import defaultdict
import json

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.text.strip()
        try:
            json_data = json.loads(f"[{data.replace('}\n{', '},{')}]")
            return json_data
        except json.JSONDecodeError as e:
            print(f"ERROR | {e}")
            return []
    except requests.RequestException as e:
        print(f"ERROR | {e}")
        return []


def parse_file(file_path, tune_data):
    result = defaultdict(lambda: defaultdict(list))
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) < 5:
                    continue

                main_id = int(parts[1])
                tune_id = int(parts[0])

                found = False
                for tune in tune_data:
                    if str(tune["tuneId"]) == str(tune_id):
                        result[main_id][tune_id].append(tune["name"])
                        found = True

                if not found:
                    print(f"Не найдено соответствие для tune_id: {tune_id}")

        output = "new test_array[][] = {\n"
        main_ids = list(result.keys())
        for idx, main_id in enumerate(main_ids):
            output += f"  {{{main_id}, {{ "
            tune_entries = []
            for tune_id, names in result[main_id].items():
                for name in names:
                    tune_entries.append(f"{{ {tune_id}, \"{name}\" }}")
            if not tune_entries:
                tune_entries.append("{ -1, \"\" }")
            output += ', '.join(tune_entries)
            if idx == len(main_ids) - 1:
                output += "}}}\n"
            else:
                output += "}}},\n"
        output += "};"

        return output

    except Exception as e:
        print(f"ERROR | {e}")
        raise


def main():
    input_file = 'customtune.dat'
    output_file = 'output.txt'
    url = 'https://pastebin.com/raw/xm80XkAB'

    try:
        tune_data = fetch_data(url)
        if not tune_data:
            print("Не удалось загрузить данные с URL.")
            return

        output_data = parse_file(input_file, tune_data)

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(output_data)

        print(f"Результат в {output_file}")

    except Exception as e:
        print("Произошла ошибка:", e)


if __name__ == "__main__":
    main()
