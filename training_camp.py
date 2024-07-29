# Import python packages
import streamlit as st
from snowflake.connector.pandas_tools import write_pandas
from snowflake.connector import connect
#from snowflake.snowpark.context import get_active_session

def main():
    st.image("https://www.skogsluffarna.se/skin/default/header/logotype.png?t=1722253244")
    # Write directly to the app
    st.title("Anmälan till Skogsluffarnas Träningsläger i Orsa 2025")
    st.write("Ange namn, epost och telefon till ansvarig för anmälan")
    resp_name = st.text_input("Namn" )
    resp_mail = st.text_input("E-post")
    resp_telefon = st.text_input("Telefon")
    st.write("---------------------------------------------")
    sharing = st.text_input("Vi önskar dela stuga med:")
    st.write("---------------------------------------------")
    trainer = st.radio(f"Kan någon/några i sällskapet ställa upp som tränare/ledare för någon träningsgrupp?", ["Ja, som  huvudtränare", "Ja, som hjälptränare", "Nej tack"], horizontal=True,)
    st.write("---------------------------------------------")
    misc = st.text_area("Övrig information som kan vara bra att veta om")

    st.write("---------------------------------------------")
    # Get the current credentials
    #SSsession = get_active_session()

    #option = st.selectbox(
    #    "Antal personer att anmäla",
    #    ("1","2","3","4","5","6","7"),
    #)
    #st.write("You selected:", option)


    person = 1
    name_1 = st.text_input(f"Namn för person {person}", "Förnamn och Efternamn")
    agegroup1 = st.radio(f"Ange åldersgrupp för person {person}", ["0-6 år", "7-18 år ", "18-64 år", " 65 år eller äldre"], horizontal=True,)
    diet_1 = st.text_input(f"Ange ev diet eller allergier för person {person}", "")
    transport_1 = st.selectbox(f"Önskad transport till Orsa för person {person}",("Tidig buss","Sen buss","Egen Bil"))
    st.write("---------------------------------------------")

    person = 2
    name_2 = st.text_input(f"Namn för person {person}", "Förnamn och Efternamn")
    agegroup_2 = st.radio(f"Ange åldersgrupp för person {person}", ["0-6 år", "7-18 år ", "18-64 år", " 65 år eller äldre"], horizontal=True,)
    diet_2 = st.text_input(f"Ange ev diet eller allergier för person {person}", "")
    transport_2 = st.selectbox(f"Önskad transport till Orsa för person {person}",("Tidig buss","Sen buss","Egen Bil"))
    st.write("---------------------------------------------")

    person = 3
    name_3 = st.text_input(f"Namn för person {person}", "Förnamn och Efternamn")
    agegroup_3 = st.radio(f"Ange åldersgrupp för person {person}", ["0-6 år", "7-18 år ", "18-64 år", " 65 år eller äldre"], horizontal=True,)
    diet_3 = st.text_input(f"Ange ev diet eller allergier för person {person}", "")
    transport_3 = st.selectbox(f"Önskad transport till Orsa för person {person}",("Tidig buss","Sen buss","Egen Bil"))
    st.write("---------------------------------------------")

    person = 4
    name_4 = st.text_input(f"Namn för person {person}", "Förnamn och Efternamn")
    agegroup_4 = st.radio(f"Ange åldersgrupp för person {person}", ["0-6 år", "7-18 år ", "18-64 år", " 65 år eller äldre"], horizontal=True,)
    diet_4 = st.text_input(f"Ange ev diet eller allergier för person {person}", "")
    transport_4 = st.selectbox(f"Önskad transport till Orsa för person {person}",("Tidig buss","Sen buss","Egen Bil"))
    st.write("---------------------------------------------")

    person = 5
    name_5 = st.text_input(f"Namn för person {person}", "Förnamn och Efternamn")
    agegroup_5 = st.radio(f"Ange åldersgrupp för person {person}", ["0-6 år", "7-18 år ", "18-64 år", " 65 år eller äldre"], horizontal=True,)
    diet_5 = st.text_input(f"Ange ev diet eller allergier för person {person}", "")
    transport_5 = st.selectbox(f"Önskad transport till Orsa för person {person}",("Tidig buss","Sen buss","Egen Bil"))
    st.write("---------------------------------------------")

    person = 6
    name_6 = st.text_input(f"Namn för person {person}", "Förnamn och Efternamn")
    agegroup6 = st.radio(f"Ange åldersgrupp för person {person}", ["0-6 år", "7-18 år ", "18-64 år", " 65 år eller äldre"], horizontal=True,)
    diet_6 = st.text_input(f"Ange ev diet eller allergier för person {person}", "")
    transport_6 = st.selectbox(f"Önskad transport till Orsa för person {person}",("Tidig buss","Sen buss","Egen Bil"))
    st.write("---------------------------------------------")


def sflake_connect():
    conn = connect(
        user = '',
        password = '',
        account = '',
        database = '',
        warehouse = '',
        schema = ''
    )
    cursor = conn.cursor()

    return conn, cursor

if __name__ == '__main__':
    main()