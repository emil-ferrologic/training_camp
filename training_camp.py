# Import python packages
import streamlit as st
import pandas as pd
#from snowflake.connector.pandas_tools import write_pandas
#from snowflake.connector import connect
#from snowflake.snowpark.context import get_active_session

def main():
    conn = st.connection("snowflake")

    cursor = conn.raw_connection.cursor()
    # df = conn.query('SELECT * from "TEST";', ttl=600)
    # print(df)


    # Load the table as a dataframe using the Snowpark Session.
    # @st.cache_data
    # def load_table():
    #     session = conn.session()
    #     return session.table("TEST").to_pandas()

    # df = load_table()

    # # Print results.
    # for row in df.itertuples():
    #     st.write(f"{row.ID} has a :{row.TEXT}:")
    if "signup_ID" not in st.session_state:
        st.session_state.signup_ID = 0
    if "part" not in st.session_state:
        st.session_state.part = []
    if "all_parts" not in st.session_state:
        st.session_state.all_parts = []
    if "rc" not in st.session_state:
        st.session_state.rc = 0

    st.image("https://www.skogsluffarna.se/skin/default/header/logotype.png?t=1722515192",width=120)

    with st.form("update_report"):
        # Write directly to the app
        st.title("Anmälan till Skogsluffarnas Träningsläger i Orsa 2025")
        st.write("Ange namn, epost och telefon till ansvarig för anmälan")
        resp_name = st.text_input("Namn" )
        resp_mail = st.text_input("E-post")
        resp_telefon = st.text_input("Telefon")
        st.write("---------------------------------------------")
        sharing = st.text_input("Vi önskar dela stuga med:")
        st.write("---------------------------------------------")
        # trainer = st.radio(f"Kan någon/några i sällskapet ställa upp som tränare/ledare för någon träningsgrupp?", ["Ja, som  huvudtränare", "Ja, som hjälptränare", "Nej tack"], horizontal=True,)
        st.write(f"Kan någon/några i sällskapet ställa upp som tränare/ledare för någon träningsgrupp?")
        trainer_1 = [ st.checkbox("Ja, som  huvudtränare" ), st.checkbox("Ja, som hjälptränare" ), st.checkbox("Nej tack")]
        # print(str(trainer_1))
        # chk = st.checkbox("Ja, som hjälptränare" )
        # chk = st.checkbox("Nej tack")
        st.write("---------------------------------------------")
        misc = st.text_area("Övrig information som kan vara bra att veta om")

        st.write("---------------------------------------------")
        
        sub_comment = st.form_submit_button('Submit')
    
    if sub_comment:
        sql_insert  = f"""insert into signup  
                (resp_name,
                resp_mail,
                resp_telefon,
                sharing,
                trainer,
                misc)
                values (
                '{resp_name}',
                '{resp_mail}',
                '{resp_telefon}',
                '{sharing}',
                '{trainer}',
                '{misc}'
                )"""
        
        cursor.execute(sql_insert)
        sql_stmt = f"""SELECT max(signup_ID) as signup_ID  from signup where 
            resp_name = '{resp_name}' and 
            resp_mail = '{resp_mail}' and
            resp_telefon = '{resp_telefon}'
        ; """
        st.session_state.signup_ID = conn.query(sql_stmt, ttl=600).values.tolist()[0][0]
        # print(signup_ID[0][0])
    st.write(st.session_state.signup_ID)

    # st.session_state.all_parts = []
    @st.dialog("Lägg till deltagare")
    def vote(item):
        st.write(item)
        name = st.text_input(f"Namn", "Förnamn och Efternamn")
        agegroup = st.radio(f"Ange åldersgrupp", ["0-6 år", "7-18 år ", "18-64 år", " 65 år eller äldre"], horizontal=True,)
        diet = st.text_input(f"Ange ev diet eller allergier", "")
        transport = st.selectbox(f"Önskad transport till Orsa",("Tidig buss","Sen buss","Egen Bil"))

        if st.button("Lägg till"):
            st.session_state.all_parts.append([name, agegroup, diet, transport])
            st.rerun()
    
    if st.button('Lägg till deltagare'):
        vote(st.session_state.signup_ID)
        
    st.write(st.session_state)

    df = pd.DataFrame(st.session_state.all_parts, columns=['För-/Efternamn', 'Åldersgrupp','Allergi/Diet', 'Transport'])
    edited_df = st.data_editor(df, disabled=['Åldersgrupp', 'Transport'])





if __name__ == '__main__':
    main()