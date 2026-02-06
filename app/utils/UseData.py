from app.utils.DateHelper import get_today_date


def write_to_file(string: str):
    with open('output/use_data.txt', 'a', encoding='utf-8') as file:
        file.write(get_today_date() + " " + string + "\n")
