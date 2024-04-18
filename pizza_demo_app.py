import streamlit as st
from streamlit_gsheets import GSheetsConnection

def reload():
    st.cache_data.clear()
    st.experimental_rerun()


def load_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(worksheet="Orders")
    data = data.dropna(axis=0, how="all").dropna(axis=1, how="all")

    if not data.empty:
        buttons = []
        for idx, row in data.iterrows():
            st.table(row)
            button = st.button(f"Delete Order {idx+1}")
            buttons.append(button)

        if any(buttons):
            for idx, button in enumerate(buttons):
                if button:
                    updated_data = data.drop(index=idx)
                    conn.clear(worksheet="Orders")
                    conn.update(worksheet="Orders", data=updated_data)
                    st.success(f"Order {idx+1} deleted successfully.")
                    reload()

load_data()
