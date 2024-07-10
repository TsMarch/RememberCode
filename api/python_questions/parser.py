import pandas as pd
import sqlalchemy
import sqlalchemy.exc

from api.configs.environment import (DB_POSTGRES_HOST, DB_POSTGRES_NAME, DB_POSTGRES_PASS,
                                  DB_POSTGRES_PORT, DB_POSTGRES_USER)


def parse():
    with open("api/python_questions/questions.txt", "r") as file:
        df = pd.DataFrame()
        for count, line in enumerate(file):
            lst = line.split()
            try:
                answ = []
                match lst[0].endswith(")"):
                    case True:
                        quest = line
                    case False:
                        answ.append(line)
            except Exception as e:
                continue
            temp = pd.DataFrame({"question": quest, "answer": answ})
            df = pd.concat([df, temp])
            df.index = range(1, len(df) + 1)
    add_questions(df)


def add_questions(dataframe: pd.DataFrame):
    conn = sqlalchemy.create_engine(
        f"postgresql+psycopg://{DB_POSTGRES_USER}:{DB_POSTGRES_PASS}@{DB_POSTGRES_HOST}:{DB_POSTGRES_PORT}/{DB_POSTGRES_NAME}"
    )
    dataframe.to_sql(name="questions", con=conn, if_exists="replace")
