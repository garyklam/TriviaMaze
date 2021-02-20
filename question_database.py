import requests
import sqlite3
from sqlite3 import Error


class SQLDatabase:

    def __init__(self, category=None, difficulty="easy", target=None):
        self.category = category
        self.difficulty = difficulty
        self.target = target
        trivia_token = requests.get("https://opentdb.com/api_token.php?command=request").json()
        self.trivia_token_url = "&token=" + trivia_token["token"]
        self.category_list = self.get_category_list()
        self.question_count = self.get_question_count()

    def set_category(self, category):
        self.category = category
        self.question_count = self.get_question_count()

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.question_count = self.get_question_count()

    @staticmethod
    def get_category_list():
        c_response = requests.get("https://opentdb.com/api_category.php")
        categories = c_response.json()
        category_list = {}
        for item in categories["trivia_categories"]:
            category_list[item["name"]] = str(item["id"])
        return category_list

    def get_question_count(self):
        if self.category:
            category_id = self.category_list[self.category]
            category_lookup = "https://opentdb.com/api_count.php?category=" + category_id
            q_count_response = requests.get(category_lookup)
            q_count = q_count_response.json()
            difficulty = "total_" + self.difficulty + "_question_count"
            total_question_count = q_count["category_question_count"][difficulty]
        else:
            total_question_count = 500
        return total_question_count

    def get_questions(self, amount):
        amount_url = "&amount=" + str(amount)
        category_url = ""
        if self.category:
            category_url = ""
        difficulty_url = "&difficulty=" + self.difficulty
        trivia_url = "https://opentdb.com/api.php?" + amount_url + category_url + difficulty_url + self.trivia_token_url
        q_response = requests.get(trivia_url).json()
        questions = q_response["results"]
        sql_str = {"boolean": [], "multiple": []}
        for question in questions:
            if question["type"] == "boolean":
                content = (question["question"], question["correct_answer"], question["incorrect_answers"][0])
            else:
                content = (question["question"], question["correct_answer"], question["incorrect_answers"][0],
                           question["incorrect_answers"][1], question["incorrect_answers"][2])
            sql_str[question["type"]].append(content)
        return sql_str

    def build_database(self):
        try:
            conn = sqlite3.connect(r"trivia_maze_questions.db")
        except Error as e:
            print(e)
        if conn:
            try:
                c = conn.cursor()
                c.execute("DROP TABLE IF EXISTS true_false;")
                c.execute("DROP TABLE IF EXISTS multiple;")
            except Error as e:
                print(e)
        if conn:
            try:
                c = conn.cursor()
                c.execute("""CREATE TABLE IF NOT EXISTS true_false (
                          question text,
                          correct_answer text,
                          incorrect_answer text
                          );""")
                c.execute("""CREATE TABLE IF NOT EXISTS multiple (
                            question text,
                            correct_answer text,
                            incorrect1 text,
                            incorrect2 text,
                            incorrect3 text
                            );""")
            except Error as e:
                print(e)
        self.add_questions(c)
        conn.commit()

    def add_questions(self, c):
        questions = self.get_questions(10)
        c.executemany("INSERT INTO true_false Values (?,?,?)", questions["boolean"])
        c.executemany("INSERT INTO multiple Values (?,?,?,?,?)", questions["multiple"])



if __name__ == '__main__':
    db = SQLDatabase()
    db.set_category("Entertainment: Music")
    db.set_difficulty("easy")
    db.build_database()
