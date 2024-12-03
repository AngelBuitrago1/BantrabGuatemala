import streamlit as st
import random
import time
import requests
import json
import yaml

projects = []
project_ids = []


def load_config():
    with open('config.yaml', 'r') as file:
        config_content = yaml.safe_load(file)
    return config_content


config = load_config()
api_key = config['AAI-Brain']['API-KEY']
api_secret = config['AAI-Brain']['API-Secret']


def clear_session_state():
    st.session_state.messages = []
    print("cleared")


def create_chat(project_id):
    st.session_state.messages = []
    url_create = "https://api.getodin.ai/chat/create"
    payload = json.dumps({'project_id': project_id})
    headers = {
        "accept": "application/json",
        "X-API-KEY": api_key,
        "X-API-SECRET": api_secret,
        "content-type": "application/json"
    }
    response_create = requests.post(url_create, data=payload, headers=headers)
    conv_id = json.loads(response_create.content)["chat_id"]
    return conv_id


def get_projects():
    url_projects = "https://api.getodin.ai/projects"
    headers = {
        "accept": "application/json",
        "X-API-KEY": api_key,
        "X-API-SECRET": api_secret,
    }

    response_projects = requests.get(url_projects, headers=headers)
    projects_json = json.loads(response_projects.content)
    global projects
    projects = [project for project in projects_json['projects']]
    global project_ids
    project_ids = [project['name'] for project in projects_json['projects']]
    return projects, project_ids


# Call Projects function to fill the select-box element
get_projects()


@st.experimental_fragment
def sidebar_update():
    project_name = st.selectbox(
        "Selecciona el nombre del proyecto",
        project_ids,
        index=None,
        placeholder="Select Project name...",
    )

    for project in projects:
        if project['name'] == project_name:
            project_id_selected = project['id']
            st.session_state["project_id_selected"] = project_id_selected

# Create streaming Object from Response
def response_generator(response_str):
    full_response = ""
    for word in response_str:
        time.sleep(0.01)
        yield word

st.set_page_config(page_title='Banco Popular - Automation Anywhere - AAI Agent', page_icon = 'https://chat-beta.automationanywhere.com/assets/icon/favicon.ico', layout='wide')
st.header("Banco Popular - Automation Anywhere - AAI Agentic")
# st.image("https://chat-beta.automationanywhere.com/static/media/aa-gen-ai-logo.17572d7b831dd1a39cf8.png")
st.html("""
    <!doctype html>
    <html lang="en">
    <head>
    	<meta charset="utf-8"/>
    <title>AAI Enterprise Knowledge</title>
    </head>
    <body>
    <center> 
    <img src=https://chat-beta.automationanywhere.com/static/media/aa-gen-ai-logo.17572d7b831dd1a39cf8.png width=200>
    <br><br>
    <img src=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAhIAAABfCAMAAACKut4WAAAAilBMVEX///8Mhj0AgzYAgC8AhDkAfSYAgjMAfywAfikAhTpnqXwAgC6JupilyrEAfCP8/v3e7OOSv6DW59z1+vfr9O5hpnfJ39Cw0Lq/2cft9fDQ49aZw6a31MB8s41XoW8/l10bi0ZyroU4lFhOnWgukVGMvJsijUp4sYpZonEAeRlOnWk6lVmgx6wAdhD2Qtd3AAAVHElEQVR4nO1diZbqKBBtsxBiNMZ9b7VdenP+//dGSIoUUMS2Y8+z3+SeM+fMs5EQKKCWW+XTU4MGN2E4OfeX1qe9dec76HcnvT/wDg3uiOkm5H64tj4fvLNvwee8nf2B92hwJ5xZErRarWhm/WWatL4LL+38gVdpcA8MTlG+iOHI+tuafVskLiL2/AfepkF9dNOgWEJm//EQVC76FSS7//51GtRGP4UF9MbWH3tp1YpfR7r4A2/UoB7O5aL7Z+uvA15PJILNH3ilBrUwQccAt7d0168nEq3UVk8aPDR6XoxEYmj9fefVFAl/+gfeqkENrNEpEB/svx8KiQk8T3gbPCxBXwI7/vcv1aAGRlh7ZLajanj5e+BHITuMd+tOZ7173kZhcsvJQXTa4JFxxKpCYp/xizRK9/3JHH3Uy6Y7L/yyt4I17qrfhRa+B0LbAb0cz8hQxWAdJV+7Qnw7bNLggZGF2oa+6bvTE/+KUESTHxp7gx/BCgcwgo9bv936goWa2lZMgweGFsBg/Zu/30mvubvj0w8Mu8HP4YCPfiIMehWD7RU9k73ef9QNfg5DLYCRzq9/w8a42uNNWDENHhgTvJzx9nudHCsDY4QV0+CBscTqodf+Zi/dKpnw7zrgBj+NZ+yG9Lvf7aZCJryGQ/O7EOHV44Nv99N36hONo+p3QXdUhTUY1W2Xg4I3jqpfBY1pW4/r4qLjEeH2Bg8MjQtRLzyV0epEQITbGzwwTthRlaxq9bUkuf1NZPx3wXBU1STEnagYWE05a/AfY6IZHLeFQYneqKujIV7+LvRxeMJ7q2w7X6yms0GlrrixNcw4phqO5vPRqFE7HxF7vIZVDoSsc0p5lEQ8/Fy64yCT0BIJIi/kae6lYRqGaaN41kX3efP5udncM3lK8yW4HQiLTcpATwj88NW5v21DlMgLUXpoep+X+P9i9O4FAu/3S54aaLvaxXQZjg1KBEtcMfSuZXQQeSFP49zyDfZ3e5H/KYD+dEeOkpa042K6LJjNh3h33DFDy61NOUQLtmfD5a+Lgv703QA2Bd1RRTNdpu+UaZkS94HAs0HmpxyikCXwHb5OA4yX/PT27qhLbDVHFcl0OTtCnCmteJilKCiH6MxdtqDBLegVE/n9ALaFkR7zopguU1fQmzYujS7pk+BYXER13SD/e0D+do0AtomZ5qhKiBaOuIUUTZq529KvGcpRVVi+lHna4BaAKsjvVxKsg/VGUv9vVaRpRGSfb5oyEbeIJsVTKfO0wS0oVMHg835das5Giq+/rkrSiMjgheYPJZl7QNGgzNMGt6BQBe+YX9nTLMZg37ZQmbYTH+wvtNu6T5tSfEADbXgUNTEv9tYdA4tGdZnAs1AlEReZsL/gebpTi1J8wJgGd/ZXLsJe3dtymC0mi0oLpzefz28V0tFiMllU5jkMs8lkUh0Ykg8ffmN/ALn+jgz42tVlroNyWRdOb8GjGPSfW0mUtJ6X7rcaLN+2fhSx/VFcNNly2e8v8zBLNhC4zOVodWyP269nV+XVxfrEQ84v/23O5NTPp+0tD8OQx+NVtfBlm8PhdDq8XR563kchjyIexmuHxj9Zb8O8yeloiGN2lMVihSU/Oe69iHN/0zG6Ge3al9dqa6VD++2xgDx8gVzv6V8bzjrjw/a0f52O5L9WF+SJ3hcBvuDyadbdPb+8bD6scbfrVpe5CspRBQ5OtuzHoS/Ll8Senz6TQtE7b4s2rYCF2+lTlPgXyGKa6/fLKvP0tNikCbucT6Ly6o44CLrbEAdobJfp4i1MoIyKF1VrvR8siOM44Mu31IcDMWbpB/Hcc4ur516a7DRh9HxZKzacdzzO8o4Clh40Z88+kecuRy7E1Xt+Fr+LJS40eZ0BP/sII+ZdBhmwJN1PnrY8SZIoXRcTdpG9aLBPfSaCI5GlhNSpZvk1UC7rBVxXjGFzxksJ9bbra+UK4mibz55cNgYforuKWV7VyTbSrabkpC/f6CPVt0Z0qLgKoCnTv+OF5n2+io1KC8xDe1IZ95G2CEGK1fFC58L6GFy6J7R+2BswOYR4YEG498o28Cg1YZaBMKpZu/ALoBxVzuuKm36K0YsVMSlmWRgrmR2IF0h1Xt8utczogGGZOKfWWekxp9LheKh4rqZI995C67kxKva4ctUb9l965rOwPvaJPNjgFSxLNfTaVsp28W+xEKYXkXAaOYd1P4TEfnNfV4lusc5CZ0q6MFZcw0+RX35+oOQviMsz/I1KPwk8l7JXMWfvSPxHZOZ0XHrw3fWGmXIyTAkKQbGL5cGxKhyNKo83i529ioWwx24oIYaj6kdAOqpit/crxDvt/O5sJ0nfrlmNyxcdOWwmBrLXI0Xm0sCVoFZVOro0qrOIFmbvBVq8uAsw+HDMvebPCl7Kx2se7I4RBp3YByJAtrHW207DqxjWnUBF6OZV1xWK+y8r2knS96dr+By265w5mngwiwfXieUI6lXOmYokZ87SPKBx9CJHA/nsQtEuqjxghjtcupJxUHiAwBs4q5gw2cZiQVohibplkL8AylGlEYBjlkSRXw7VVyowCrd5FxPU19ZOxGy1WY2xOwTmsLdVH8bsYmJy2CV+q5j0PSsb+NpAHOwezbnnRRdLJ0UHQiHQw0BJhJeEacrL3QmuZ80jFPgXMwBVCCzWeEg4ojQPNr5ERJG5skPm+/pukOo4ViWkD8riYi1qlkH+AigfSr88qmO+7awms+WhHAkc+gP1gn6ym85m3WesWIh+0ayy8PD8ydWcguX7rJYi2vYnWTY5SsEKlALaUVKVxOvLQM6bsk+60AZ6aJCOZ0Nh9m/KXnItZuOVTVbZcL5Yl6dGodB18SQclrPBYIr00fwGWhCOqBM6OAZaXGDuw9e9cN+fTvufWL8VbdDY/WS/u8DasGf9GrV9l9cKk113XlJVBEqOjReD/K/UaMNCuwbTIk6PhQaenQKtXzWrcXgUyzcfqw9yDWYKu8JjoHD2nqOWvwUFXqUYBBFMzkxpYHQAp1xKdlJ2gEqQzrf3EkTE/4TFzLaG2Veq2F4LrrmBUrLymw/WBwWoIetGHhygfea0tRfoMWwXOuyiVU5YOMQTxpcOd5wesgw2drSiWibiExXi+EAyQZ6+atLZphyYYnYXGw3CbQGy5YcqKiv7BUJY7MHEf8ALSSbHEFbGOyDzYR2W9yfwhzzkqFCnE120S7HQGH61HXhIhNardKUIKVIjJSZ5t+pV8CSMQLRypnxBUPVQQTm4dOXBAZeI1D6VHPLS7hkqGZPquJqwltPE1pUNog7ha7Vzk5M0uSVSaylGhTLsPc2x+aq5XcBjEmsOgpnycQkHGCxoea7CyZgHTzogVSfHlugWsxhscQMwKRjJXYOlxFYASpmL0ZswzaKG+HCu58zpSYBzIddTgaCKJhEuXUlLwNon6B3qlDUmTHQIqXiR2+mia5cE1aX6t3oc2b+4GBqVBADGcRxrKwXLmcd5YVqNH/IAERV+F5gE5B/tgctfZCj14DRyJpvBHtLpflkxEJLOqNae65oGHI2sbGJwm6HbXCQUdUn3f4CkyAtIOaLQzntGHmx1iYhzFQocGz5UkGDRBto7mE8ChuOCoM2tqiylVkqGejTvXkg4fMA4Ns+YYsBSJMAWMncqXHVilVUUsFzQHkN9wOCdMwAdGPlMPVgWSiQmjk5h88TITNS3g3olKRJwZpgKC0PPVgRVJH0eerwWBi3+YDoairtHtoH2FfmY+hlA5f4Nnc7bCxKatoF7pYr2g3FsJQjgBVJuOWP0xRtK9bGIAmK6ukYfAAXOmeGgrirjXoHTh3o/OLhNWUfh/j39fiASuQAWp4rFtS8mTsrN0ebja8x2uGX4ExIPY5vC1R+hCaMpsxJ6Xha5mSoipcxRnAQfPVQSAGxCM9ewh3XpQl2z+GPFTErxhSggiotoyhdc+s7soeJQNWlfsA9I0nNxcFvxXTjQ20q0TYnSrwFHoydMuN4H1vhUIo84OHB6lOnHBOA2Y3vCDBhHAJlS4ebieltaZ9OSvagkANAZTG0WjHDpuQNChTljEBkU4lTsERzJ7iP6wBxfROT7p3YHAq4NJwHqn1kxI1J9wcVpvruKV4iDL3OwoTQGIsHHh5WXGx2nR4Ef07zsMBEvRpNHY6I7qugb5ujQJryt4zjW4heUo0pdtcbfQMWQrir6lldDFlornKFYg8XK18LRhwLoe+bagalGJRRkjktFXXSZeq652nBfyrsUdrupfoOK4T/RYVDswdYukdg2TvB4ZRiUmDADS91R5Uip2JNRoeTzil2HltcAzLhBwBsWkyT3X8+hG38g9QCUL6wqYDt2omn4BJR2qZ8SMHOkdglLaf6xMO+EDTaLyG5n2n0JCpdxNIOLXnZPEFS1RJ4Z1rfgZQ12Shup49SEGdAT9ZyVJT5sr3fg/n1gXWOlooknZBYhgLNH3htwpntmrDz/WGpucIYiLS7D9AHQKww1b6FkGRoYdyuEhkh7ShkWW+1j8IBE03Lm9ZefK4tYLgjEzoxd3Wbo2ZD+hFI0oG95r2jpUTBh+ruoqAd7cqsbCLrPwX3DLFO9ZcAPztQineJP9akMe13t64Lll38KjRJ8GGXKlhebiLg9YQ9Lq00FcLSD8iNlcDWXDbCLYQf+LVJ7VrFXzYKGIrDSEFLdYpkagj87j+qpeKO+PmdtEmCH8/KGBeeclBItPUq5LvERMFfcwTFq784eNdhBFb+hMtqVxMTAT1/cBHFDG6VurVKDwU4VlXZahIWVtxeNf6BYefLc5Oj/C2j7QDHG4lgt+ehwaRGd8mGNKAfiGOaWPCTKMGjslapXBzqS8fTyuS313EVcSETMclKs6sdH521f9SMnAU7x8qiEKF7uI9TSo+DsxROWqRCHpo67s0eNbF6K/aQwnLZbYcjDlG36VfRwo9wIdWshDUbJxFzV6Qdfh7rUuNIE+ihOOLiufKFTMPDyLT0/ctkgTvNLUu0J9lK81KqlouekBoJCiTErRj87wRv55nNZVwrAoK2YLWk+EhQGVS84UPHU5KjPQUGZXRygZ6ke6elRYzVhSsa6ZfRV7E1qwgwYP/1JaYIahtlgcOV3GYzMMD0MUACH2vh+lY2yVVvxRxXnqIzR+tvzYJRNOh7qW/DOlE2HrhadPqBmqRXzVruz3pQ/TpfTBMqhBCKafN7Firbr0b56jTQatXbHztgrv3OyJjbhn8+buKTHRsX6Y3ePHx9ni9l5oziTXuGMKcfvt16P60PJDZA/uqrCoEN9ZP6pm81Hi+UWKfpib1ITZkCrInCXhF2T1EPq+pqRGiRhiH5cMgjgWJmXFLvY52GosZilA6uKg5bHRXDVrNhjiFFSeNlmSHEWnJOSCxAzWvj1bSQ6LT8I4H5a4GkIMFfAB41Tm/uYRRxxdxQt9Fi+s3gS+oq03zWmNmaqXSYsDbmP2subtGhfUZZ2rqsSdyh8btF/qaw0myOMRh6Vl1KbudtJUbvGQXtyU+LYoWhwcjSIueN2JKt65ghK5WLvcPn6oFBXMQ0DD6RxZpt68ALiz8Ul7RUO4l3FhEmNEqVTOaBXEbhD4fNey5xgyvk1cwfSPIYWYl5B+BKiNiR8hBp94MnpevWVT2VBNwh8h0TM3fLMtuW54kiF4MrMr5qEUid9cjGYpK02NBxtdj2oEuImNdsT0NO7q7XLL+HF2htUtQo3J9zX02kqqKXi3LzGQZMgfyEEp870qTX2T665mDinne/xDU2NPU5LL1LfOQnRBmnkU4cESmfGwnS7T9x0dqFRUhNmQCt3SXPrb8LGek1SPSEqpRYzZprL7l98EZE/0D/D8gsafSCHzfFmkbZL1laDwBpIiSXpyRXMTyNMMrPya/wWIn58OG4WL9Wdj21aBLUwaOm5cVYLakU9krRnQv9+Xe2yZ0sEXU8EeEy+dijG0da+uGZcnzkG3xW8M6JIIpVFPfO1VTTTMoXg6WRDfqi4QUuzEBMA/LRtHSvZgWO6YRJpXkroxtd9vene3MFrTbTgVWQYtG2HZGd6KmE5YS+ovbuq5OCu2uXwQByFVD2R0T+Sset/TmOVQBv44Ym84OZjlYcbMM6OgzxBVnIniygg9vScwSrTRtaJOBMU+sDzub+2T83R5SH5pS0ylTeVFfYgHtYf7Tj3PZmXHLbMjPAcq4NIxBXvGoUvXc3wAw+BP+3wKDeEAhaFY2K+Bvs0EVnJgce4102i5IJQ6kpbJiugchxamLfVhMWMJ50szSdMtGnl7UM3o8pIy6ynXWZkShX5+z99mQgvkuMn61MoEO37TudJ1t/INuFhLdZqKdPo16LfXSpyxkOkjF2URVEtgL8b3rnebP2x9eLDuO94x1H3LRZVBE7tbnV9PRxW7E2Wu8t7HKfuqzmbdi7j3S1n5hmC/O691etLxDnbrFeOYNSo+/px2L6Mj8LbhKoCTPebzWa/b+tfGy03XE7YSU7YeawmbPpxab7ZmKckguGoqqVdTsm0sy+UT+qNRqOrD56Psq8OrkZRkuEXvquWsmZlRvAoVLCb6mCeZd8aoF6UjIiOZV/9nenemFaM71g+6UEAIZS6qviL5nd/FBjOEmJ0q3/evlQoZ+Y5LKq/r/Dt532W8geql94DhrOE0C47jLHrNbGyvV1EoXWf4/Xh0KMpNzfjB6qX3gOGx4jQLoXfgm+qixCO2naxDkB9T8ejwQihfBs/UL30HthcjWJLmQnSvfv4X4zdAvFwN+UdoJayZmXGtuF3fwzo5S5J7bLQGQPeIhkSWX8bVgjEw92UdwCEUOr+0FDLDtg9AAxGFaVdKoJNzMLW6wqJxXAw3cWh7w4K5gfP/SoxPgi291nKH6heeg8Y8RtCYdKUjZglYRjvx7tde7yJQ55crTJw16LOjwEihPItaOlHjwNDJAjt0g5PxQFR+tYJ/lh74A6411JC+tEPOaq+C6NOsq1d9mqWuvsLf1IaMiqpIiq3AKcfPRD0XxCu0C6/Czqp/FdjwpPE9xNeV21+ltEZ/s+jHaPavUBol+aPMd0I/lVv+K9CT6B+L6KM9WLxWJrEBVN8cxDaZXWtkWtI/jqfxP8BW3RMENql/fuvN8Aqe9zgNyBDTD1Cu6yhSsTuhNEGD42SHkhol4MKuu8V+HFtrneDP4TsxJ3B3u/+cosgGT5WMKfBTZhuQn6xq4hfBW6H/u2Iwmg/bQTil2M4mXa7Z9seunx6O1aDRh4aNPgr8C/fYjKh0zXrqAAAAABJRU5ErkJggg== width=250>
    </center>
    </html>
""")

# Create a sidebar using Streamlit's built-in function
with st.sidebar:
    # Call the sidebar_update() function decorator
    sidebar_update()
    # Create a primary button in the sidebar with the label "Create a new Chat"
    if st.button("Crear un nuevo Chat", type="primary"):
        clear_session_state()
        clear_session_state()
        # Set the value of the session state variable 'chat_id' to the result of calling create_chat()
        # with the 'project_id_selected' value from the session state
        st.session_state['chat_id'] = create_chat(st.session_state["project_id_selected"])
    st.html("""
    <!doctype html>
    <html lang="en">
    <head>
    	<meta charset="utf-8"/>
    <title>AAI Enterprise Knowledge</title>
    </head>
    <body>
    <center>
    <br><br>
    <img src=https://www.automationanywhere.com/sites/default/files/images/products/product-index/pathfinder-tab.png width=250>
    </center>
    </html>
""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get('image', 0) != 0:
            # print(message["image"])
            st.image(message["image"], 'Generated Image(s)')
        else:
            st.markdown(message["content"])
            # pass


# Accept user input
if prompt := st.chat_input("Hola, ¿Cómo puedo ayudarte?"):
    # Add user message to chat history
    session_state_test = st.session_state
    # Check if a chat ID has been set in the session state.
    # If not, check if a project ID has been selected.
    if session_state_test.get('chat_id', 0) == 0:
        # If no chat ID, but a project ID has been selected, create a new chat.
        if session_state_test.get('project_id_selected', 0) == 0:
            # Display a toast message prompting the user to select a project.
            st.toast('Select a project first', icon='🚨')
            st.stop()
        else:
            # Create a new chat with the selected project ID and set it as the chat ID.
            st.session_state["chat_id"] = create_chat(st.session_state['project_id_selected'])

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display user message in chat message container
    with st.chat_message("assistant"):
        chat_id = st.session_state["chat_id"]
        project_id = st.session_state["project_id_selected"]
        print(f"chat with project {project_id}")
        url_message = "https://api.getodin.ai/v2/chat/message"
        payload = f"-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"agent_type\"\r\n\r\nchat_agent\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{chat_id}\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"message\"\r\n\r\n{prompt}\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"project_id\"\r\n\r\n{project_id}\r\n-----011000010111000001101001--"
        chat_headers = {
            "accept": "application/json",
            "X-API-KEY": api_key,
            "X-API-SECRET": api_secret,
            "content-type": "multipart/form-data; boundary=---011000010111000001101001"
        }

        response = requests.post(url_message, data=payload, headers=chat_headers)

        response_message = st.write_stream(response_generator(json.loads(response.text)['message']['response']))
        images = []
        if (json.loads(response.text)['message']).get('image_urls', 0) != 0:
            print('got an image')
            print(json.loads(response.text)['message']['image_urls'][0])

            for index, image in enumerate(json.loads(response.text)['message']['image_urls'], start=1):
                images.append(image)
            image_message = st.image(images, caption=f'Generated Image(s)')
    if len(images) > 0:
        st.session_state.messages.append({"role": "assistant", "content": response_message})
        st.session_state.messages.append({"role": "assistant", "image": images})
    else:
        st.session_state.messages.append({"role": "assistant", "content": response_message})
