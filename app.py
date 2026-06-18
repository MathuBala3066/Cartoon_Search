from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

df = pd.read_csv("Cartoon_datasets.csv")

st.title("Cartoon Data QueryInterface")

question = st.text_input("Enter your query about the cartoon data:")

if question:
    try:
        load_dotenv()
        api_key = os.getenv("API_KEY")
        if not api_key:
            st.error("API_KEY not found in environment variables.")
            exit(1)
        
        prompt = f"""You are a PostgreSQL Query Generator.

           Rules:
                1. Generate ONLY PostgreSQL SQL queries.
                2. Do NOT explain the query.
                3. Do NOT add comments.
                4. Do NOT add markdown or code fences.
                5. Return only executable PostgreSQL syntax.
                6. If multiple queries are needed, separate them with semicolons.
                7. Assume table and column names from the question unless specified.
                8. Use PostgreSQL syntax only.
                example QUERY : SELECT "student_name", "department"
                                FROM "students"
                                WHERE "department" = 'CSE'
                                LIMIT 10;
                9. Always use double quotes for table and column names.
                10.Don't Generate User Safety : safe or unsafe queries. Just Generate the query.

              User Question:
              {question}

              Table:
              "Cartoon_Details" 

              columns:
                 "Name"
                 "Span"
                 "Description"
                 "Rating"
               """


                   


        client = OpenAI(api_key = api_key , base_url="https://openrouter.ai/api/v1")


        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    except Exception as e:
        st.error(f"Error loading environment variables: {e}")
        exit(1)


    st.write("Answer:")
    sql = (response.choices[0].message.content)
    sql = sql.replace("``` sql","").replace("```", "").strip()

    st.code(sql, language="sql")

    result = pd.read_sql(sql, engine)

    st.dataframe(result)