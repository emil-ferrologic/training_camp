# Import python packages
import streamlit as st
import pandas as pd
from datetime import datetime


st.set_page_config(layout="wide", page_title='Anmälning till Orsa 2025', page_icon="https://www.skogsluffarna.se/skin/default/header/logotype.png?t=1722515192")

conn = st.connection("snowflake")

cursor = conn.raw_connection.cursor()

def disable():
    st.session_state.disabled = True

if "signup_ID" not in st.session_state:
    st.session_state.signup_ID = 0
if "part" not in st.session_state:
    st.session_state.part = []
if "all_parts" not in st.session_state:
    st.session_state.all_parts = []
if "rc" not in st.session_state:
        st.session_state.rc = 0
if "add_part" not in st.session_state:
    st.session_state.add_part = False
if "disabled" not in st.session_state:
    st.session_state.disabled = False
if "state" not in st.session_state:
    st.session_state.state = "ongoing"
if "load_datetime" not in st.session_state:
    st.session_state.load_datetime = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

st.image("https://www.skogsluffarna.se/skin/default/header/logotype.png?t=1722515192",width=120)

if st.session_state.state == 'ongoing':

    with st.form("update_report"):

        sql_stmt_no_participanst = f"""SELECT count(*) as antal  from participants""";
        test = conn.query(sql_stmt_no_participanst, ttl=600).values.tolist()[0][0]
        print(test)
        # st.session_state.no_of_participants = conn.query(sql_stmt_no_participanst, ttl=600).values.tolist()[0][0]
        # print(st.session_state.no_of_participants)

        # Write directly to the app
        st.title("Anmälan till Skogsluffarnas Träningsläger i Orsa 2025")
        st.write('OBS! Använd med fördel Chrome på dator.')
        st.write('Fält markerade med * är obligatoriska.')
        st.write("Ange namn, adress, epost och telefon till ansvarig för anmälan *")
        resp_name = st.text_input("Namn *" )
        st.session_state.resp_name = resp_name
        print(resp_name)
        
        resp_adress = st.text_area("Fakturaadresss *")
        st.session_state.resp_adress = resp_adress

        resp_mail = st.text_input("E-post *")
        st.session_state.resp_mail = resp_mail
        resp_telefon = st.text_input("Telefon *")
        st.session_state.resp_telefon = resp_telefon
        st.write("---------------------------------------------")
        sharing = st.text_input("Vi önskar dela stuga med:")
        st.session_state.sharing = sharing
        st.write("---------------------------------------------")
        misc = st.text_area("Övrig information som kan vara bra att veta om. Allergier och dieter anges per deltagare senare i anmälan.")
        st.session_state.misc = misc
        st.write("---------------------------------------------")
        sub_comment = st.form_submit_button('Fortsätt, för att lägga till deltagare', on_click=disable, disabled=st.session_state.disabled)

        if sub_comment:
            sql_insert  = f"""insert into signup  
                    (resp_name, resp_adress, resp_mail, resp_telefon, sharing,  misc, load_datetime) 
                    values ('{resp_name}','{resp_adress}', '{resp_mail}', '{resp_telefon}', '{sharing}', '{misc}', '{st.session_state.load_datetime}')""" 
            cursor.execute(sql_insert)
            sql_stmt = f"""SELECT max(signup_ID) as signup_ID  from signup where 
                resp_name = '{resp_name}' and 
                resp_mail = '{resp_mail}' and
                resp_telefon = '{resp_telefon}'
            ; """
            st.session_state.signup_ID = conn.query(sql_stmt, ttl=600).values.tolist()[0][0]
            st.session_state.add_part = True
    
    @st.dialog("Lägg till deltagare")
    def vote(item):
        # st.write(item)
        part_name = st.text_input(f"Förnamn och Efternamn *", "")
        agegroup = st.radio(f"Ange åldersgrupp (ålder vid träningslägret) *", ["Till och med gynmnasiet", "18-64 år", "65 år eller äldre"], horizontal=True,)
        if agegroup =="Till och med gymnasiet":
            age = st.text_input(f"Vänligen ange ålder för barnet/ungdomen", "")
        else:
            age = None
        # print(age)
        # __diet = st.text_input(f"Ange ev diet eller allergier", "")
        diet = st.multiselect("Ange ev diet eller allergier",["Vegetarian", "Vegan", "Gluten","Laktos", "Nötallergi","Kokosallergi","Mandelallergi","Tomatallergi", "Äter fisk"],)
        part_diet = [x for x in diet]
        transport = st.selectbox(f"Önskad transport till Orsa *",("Tidig buss","Sen buss","Egen Bil"))
        part_telefon = st.text_input(f"Telefon (frivilligt)", "")
        part_mail = st.text_input(f"E-post (frivilligt)", "")
        skate = st.radio("Önskar att delta i träningsgrupp med fokus på Skate", ['Ja','Nej','Vet inte/Kanske'], horizontal=True,)
        st.write(f"Kan ställa upp som tränare/ledare för någon träningsgrupp! (frivilligt)")
        trainer = [ st.checkbox("Ja, som  huvudtränare" ), st.checkbox("Ja, som hjälptränare" ), st.checkbox("Nej tack")]
        trainer_txt = ["Ja, som  huvudtränare" ,"Ja, som hjälptränare" , "Nej tack"]
        part_trainer = [trainer_txt[idx]  for idx,x in enumerate(trainer) if x == True]
        # st.write()
        part_bbq_comp = st.text_area('Kan tänka mig att hålla i eller hjälpa till vid aktiviteter som t.ex korvgrillning, lekar efter middag, kexchokladloppet, stugstafetten eller något annat. Skriv en kommentar nedan. (frivilligt)')
        if st.button("Lägg till"):
            st.session_state.all_parts.append([part_name, agegroup,age, part_diet, transport, part_telefon, part_mail,skate, part_trainer,part_bbq_comp])
            # print(st.session_state.all_parts)
            st.rerun()
    if st.session_state.add_part == True:
        st.write('Registrera alla i sällskapet som ska följa med på träningslägret, även den som angetts som ansvarig.')
        if st.button('Lägg till deltagare'):
            vote(st.session_state.signup_ID)

    if st.session_state.all_parts != []:
        st.write('Deltagare som ska följa med. För/Efternamn och Allegi/Diet går att ändra i tabellen.')
        df = pd.DataFrame(st.session_state.all_parts, columns=['För-/Efternamn', 'Åldersgrupp','Ålder','Allergi/Diet', 'Transport', 'Telefon', 'E-post', 'Skategrupp','Tränare', 'Tävlingar mm'])
        edited_df = st.data_editor(df, disabled=['Åldersgrupp','Transport','Skategrupp','Tränare'], hide_index=True)#
        df_insert = edited_df
        df_insert.rename(columns={'För-/Efternamn':'PART_NAME', 'Åldersgrupp':'AGEGROUP', 'Ålder':'AGE','Allergi/Diet':'ALLERGI', 'Transport':'TRANSPORT', 'Telefon':'PHONE','E-post':'MAIL','Skategrupp':'SKATE','Tränare':'TRAINER','Tävlingar mm':'BBQ_COMP'},inplace=True)
        df_insert.insert(0, 'SIGNUP_ID', st.session_state.signup_ID)
        df_insert.insert(5, 'LOAD_DATETIME', st.session_state.load_datetime)
        # print(df_insert)
        if st.button('Slutför anmälan'):
            conn.write_pandas(df_insert, table_name='PARTICIPANTS')
            st.session_state.state = "finished"
            st.rerun()
elif st.session_state.state == "finished":
    st.subheader('Anmälan är mottagen, följande uppgifter har registrerats')
    st.write(f'Ansvarig för anmälan')
    st.write(f'   - {st.session_state.resp_name}')
    st.subheader(f'Kontaktuppgifter till ansvarig för anmälan')
    st.write(f'   - Telefon: {st.session_state.resp_telefon}')
    st.write(f'   - E-post: {st.session_state.resp_mail}')
    st.write(f'   - Adress: {st.session_state.resp_adress}')
    st.write(f'Önskar dela stuga med')
    st.write(f'   - {st.session_state.sharing}')
    st.write(f'Övrig info {st.session_state.misc}')
    st.write("---------------------------------------------")
    st.subheader('Anmälda deltagare')
    df = pd.DataFrame(st.session_state.all_parts, columns=['För-/Efternamn', 'Åldersgrupp','Ålder','Allergi/Diet', 'Transport', 'Telefon', 'E-post', 'Skategrupp','Tränare', 'Tävlingar mm'])
    st.data_editor(df, disabled=['För-/Efternamn', 'Åldersgrupp','Ålder','Allergi/Diet', 'Transport', 'Telefon', 'E-post', 'Skategrupp','Tränare', 'Tävlingar mm'], hide_index=True)
