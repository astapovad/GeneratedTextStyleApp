import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["openai_api_key"])

st.title("Генератор тексту у вибраному стилі")

style = st.selectbox(
    "Оберіть стиль тексту:",
    ["Офіційний", "Креативний", "Науковий", "Формальний", "Мотиваційний"]
)

prompt_styles = {
    "Офіційний": "Напиши цей текст у формальному, офіційному стилі:",
    "Креативний": "Перетвори цей текст у креативну та натхненну історію:",
    "Науковий": "Сформулюй цей текст як наукову доповідь:",
    "Формальний": "Поясни цей текст простою, формальною мовою:",
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
                    {"role": "system", "content": "Ти професійний мовний редактор, який перетворює вхідний текст на граматично, лексично та стилістично бездоганний український текст у заданому стилі. Уникай русизмів, кальок і нетипових конструкцій."},
                    {"role": "system", "content": "Усі речення мають бути логічно зв’язані, лексика – відповідна до стилю, а пунктуація – коректною."},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens = 1000 ,
                temperature = 0.8
            )
            st.subheader("Згенерований текст:")
            st.write(response.choices[0].message.content)
    else:
        st.warning("Будь ласка, введіть текст.")
