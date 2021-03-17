import requests
import sqlite3
from sqlite3 import Error
import html


class SQLDatabase:

    def __init__(self, category=None, difficulty="easy", target=180):
        self.category = category
        self.difficulty = difficulty
        self.target = (target//10 + 1) * 20
        self.online = True
        self.category_list = self.request_category_list()
        if self.online and category:
            self.category_id = self.category_list[self.category]
        self.total_question_count = self.request_total_question_count()

    def set_category(self, category):
        """Sets the category to the passed in value, finds the corresponding category id sets category id to that value,
        finds the question total for the current difficulty and category."""
        self.category = category
        self.category_id = self.category_list[self.category]
        self.total_question_count = self.request_total_question_count()

    def set_difficulty(self, difficulty):
        """Sets the difficulty to the passed in value, finds the question total for current difficulty and category."""
        self.difficulty = difficulty
        self.total_question_count = self.request_total_question_count()

    def request_category_list(self):
        """Queries the api for the categories and corresponding category id's. Converts that to a dictionary and returns
        it."""
        try:
            c_response = requests.get("https://opentdb.com/api_category.php")
            categories = c_response.json()
            category_list = {}
            for item in categories["trivia_categories"]:
                category_list[item["name"]] = str(item["id"])
            return category_list
        except requests.exceptions.ConnectionError:
            self.online = False
            return None

    def request_total_question_count(self):
        """Determines the total number of questions for a given category. If no category is specified, returns 200 for
        each difficulty. With a specified category, gets total number of questions of equal or lesser difficulty and
        returns it as a dictionary."""
        if self.category:
            difficulty = self.difficulty
            total_question_count = {}
            if difficulty == "hard":
                count = self.request_question_count("hard")
                total_question_count["hard"] = count
                difficulty = "medium"
            if difficulty == "medium":
                count = self.request_question_count("medium")
                total_question_count["medium"] = count
            count = self.request_question_count("easy")
            total_question_count["easy"] = count
        else:
            total_question_count = {"hard": 200, "medium": 200, "easy": 200}
        return total_question_count

    def request_question_count(self, difficulty):
        """Queries the api for the number of questions in the specified difficulty in the current category, rounds
        that number to lowest multiple of 10 and returns it."""
        category_lookup = "https://opentdb.com/api_count.php?category=" + self.category_id
        q_count_response = requests.get(category_lookup)
        q_count = q_count_response.json()
        difficulty = "total_" + difficulty + "_question_count"
        question_count = q_count["category_question_count"][difficulty]
        question_count = question_count//10 * 10
        return question_count

    def request_questions(self, amount, difficulty):
        """Queries the api for the the specified number of questions of the category(if one is specified) and
        difficulty. Formats the response into a list of tuples and returns it."""
        amount_url = "&amount=" + str(amount)
        category_url = ""
        if self.category:
            category_url = "&category=" + self.category_id
        difficulty_url = "&difficulty=" + difficulty
        trivia_url = "https://opentdb.com/api.php?" + amount_url + category_url + difficulty_url
        q_response = requests.get(trivia_url).json()
        questions = q_response["results"]
        sql_str = []
        for question in questions:
            if question["type"] == "boolean":
                content = (question["type"], question["question"], question["correct_answer"],
                           question["incorrect_answers"][0], "", "")
            else:
                content = (question["type"], question["question"], question["correct_answer"],
                           question["incorrect_answers"][0], question["incorrect_answers"][1],
                           question["incorrect_answers"][2])
            sql_str.append(content)
        return sql_str

    def build_database(self):
        """Creates the SQLite database and clears out any questions left over from a prior session and creates a new
        table. Determines the number of questions required (either the value that was passed in or the total number of
        questions available in the current category and difficulty) and starts pulling question and adding them to the
        database, starting from the highest possible difficulty and moving to easier ones."""
        if not self.online:
            return
        try:
            conn = sqlite3.connect(r"trivia_maze_questions.db")
        except Error as e:
            print(e)
        if conn:
            try:
                c = conn.cursor()
                c.execute("DROP TABLE IF EXISTS questions;")
            except Error as e:
                print(e)
        if conn:
            try:
                c.execute("""CREATE TABLE IF NOT EXISTS questions (
                            type text,
                            question text,
                            correct_answer text,
                            incorrect1 text,
                            incorrect2 text,
                            incorrect3 text
                            );""")
            except Error as e:
                print(e)
        database_question_count = 0
        difficulty = self.difficulty
        if sum(self.total_question_count.values()) < self.target:
            self.target = sum(self.total_question_count.values())
        if difficulty == "hard" and database_question_count < self.target:
            database_question_count = self.add_questions(difficulty, database_question_count, c)
            difficulty = "medium"
        if difficulty == "medium" and database_question_count < self.target:
            database_question_count = self.add_questions(difficulty, database_question_count, c)
            difficulty = "easy"
        if difficulty == "easy" and database_question_count < self.target:
            self.add_questions(difficulty, database_question_count, c)
        conn.commit()
        c.execute("VACUUM")
        conn.close()

    def add_questions(self, difficulty, db_question_count, c):
        """Determines the highest possible amount of questions that can be obtained from the desired difficulty that
        maximizes the total number of questions and requests them. Adds these into the database. Returns the total
        number of questions pulled."""
        amounts = [50, 40, 30, 20, 10]
        remaining = self.total_question_count[difficulty]
        for amount in amounts:
            while db_question_count + amount <= self.target and remaining - amount >= 0:
                questions = self.request_questions(amount, difficulty)
                c.executemany("INSERT INTO questions Values (?,?,?,?,?,?)", questions)
                remaining -= amount
                db_question_count += amount
        return db_question_count

    def get_random_question(self):
        """Connects to a database, depending on whether the user could connect to the api or not. Selects a random
        entry from the questions table, decodes special characters and returns an array containing the contents of the
        question entry."""
        if self.online:
            conn = sqlite3.connect(r"trivia_maze_questions.db")
        else:
            conn = sqlite3.connect(r"backup_questions.db")
        c = conn.cursor()
        c.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1;")
        question = []
        for item in c.fetchone():
            question.append(html.unescape(item))
        return question

# if __name__ == '__main__':
#     db = SQLDatabase()
#     # db.set_category("Entertainment: Music")
#     # db.set_difficulty("hard")
#     # db.build_database()
#     print(db.request_category_list())
