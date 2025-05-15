import streamlit as st
from openai import OpenAI
import language_tool_python

client = OpenAI(api_key=st.secrets["openai_api_key"])
tool = language_tool_python.LanguageTool('uk-UA')

st.title("Генератор тексту у вибраному стилі")

style = st.selectbox(
    "Оберіть стиль тексту:",
    ["Офіційний", "Креативний", "Науковий", "Простий", "Мотиваційний"]
)

prompt_styles = {
    "Офіційний": "Напиши цей текст у формальному, офіційному стилі:",
    "Креативний": "Перетвори цей текст у креативну та натхненну історію:",
    "Науковий": "Сформулюй цей текст як наукову доповідь:",
    "Простий": "Поясни цей текст простою мовою:",
    "Мотиваційний": "Напиши цей текст як мотиваційне звернення:"
}

user_input = st.text_area("Введіть свій текст:")

if st.button("Згенерувати текст"):
    if user_input:
        full_prompt = f"{prompt_styles[style]} {user_input}"
        with st.spinner("Генерується..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ти асистент, що генерує граматично правильні тексти українською мовою у заданому стилі."},
                    {"role": "user", "content": full_prompt}
                ]
            )
            generated_text = response.choices[0].message.content

            st.subheader("Згенерований текст:")
            st.write(generated_text)

            # Перевірка та виправлення
            matches = tool.check(generated_text)
            corrected = language_tool_python.utils.correct(generated_text, matches)

            if generated_text != corrected:
                st.subheader("Текст після граматичної перевірки:")
                st.success(corrected)
            else:
                st.info("Граматичних помилок не виявлено.")
    else:
        st.warning("Будь ласка, введіть текст.")
