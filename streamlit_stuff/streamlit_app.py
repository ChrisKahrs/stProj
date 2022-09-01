from imp import reload
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import time


def read_index_html(copy_text: int):
    with open("index.html") as f:
        return f.read().replace("python_string", f'"Counter value is {copy_text}"')


if "counter" not in st.session_state:
    st.session_state.counter = 0


def left_callback():
    st.session_state.counter -= 1


def right_callback():
    st.session_state.counter += 1
    
def none_callback():
    if 'noneCounter' not in st.session_state:
        st.session_state.noneCounter = 0
    st.session_state.noneCounter +=1

list1 = [0,1,2,3,4]
list2 = [1,2,4,7,st.session_state.counter+1*2]
list3 = [st.session_state.counter+3*39,4,5,8,9]
df = pd.DataFrame({"A": list1, "B": list2, "C": list3})
print(df)
df = df.append({"A": st.session_state.counter, "B": st.session_state.counter+3*4, "C": st.session_state.counter+19}, ignore_index=True)
print(df)

# list1 = [st.session_state.counter]
# list2 = [st.session_state.counter*2]
# df = pd.DataFrame({"A": list1, "B": list2})
st.title("Hacking Streamlit Frontend")
st.caption(
    "Press left / right arrow keys to simulate decrement / increment button click"
)
st.caption("Press Enter key to simulate Copy to clipboard button click")
left_col, right_col, _ = st.columns([1, 1, 3])

# try:
#     st.write(st.experimental_get_query_params['direction'][0])
# except:
#     print("No direction")

left_col.button("Decrement", on_click=left_callback)
right_col.button("Increment", on_click=right_callback)
right_col.button("none", on_click=none_callback)

st.metric("Counter", st.session_state.counter)
df = df.append({"A": st.session_state.counter+1, "B": st.session_state.counter+3*4, "C": st.session_state.counter+19}, ignore_index=True)

df = df.append({"A": st.session_state.counter+1, "B": st.session_state.counter+3*4, "C": st.session_state.counter+19}, ignore_index=True)
st.line_chart(df, x="A", y=["B", "C"])
# placeholder = st.empty()

# def basic_func(sec):
#     st.write(sec)

# with placeholder:
#     for second in range(50):
#         time.sleep(1)
#         basic_func(second)
        
components.html(
    read_index_html((st.session_state.counter)),
    height=0,
    width=0,
)

# chart = st.line_chart(np.random.randn(10, 2))
full_replacement_chart = st.empty()

# while True:
new_rows = np.random.randn(10, 2) 
if 'new_rows' not in st.session_state:
    st.session_state['new_rows'] = new_rows
else:
    st.session_state['new_rows'] += new_rows
# Append data to the chart.
# chart.add_rows(new_rows)

# Just replace the chart
full_replacement_chart.line_chart(st.session_state['new_rows'])

    # Wait
    # time.sleep(.1)