# Import python packages
import streamlit as st
import pandas as pd
from datetime import datetime
from training_send_mail import send_email

# secrets o credentials lokalt finns i mapp C:\Users\Emil Karlsson\.streamlit

st.set_page_config(layout="wide", page_title='Anmälning till Orsa 2026', page_icon="https://www.skogsluffarna.se/skin/default/header/logotype.png?t=1722515192")

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

closing_date = st.secrets["variabler"]["closing_date"]
#closing_date = '2025-10-10'
print(st.session_state.state)
print(closing_date)
st.image("https://www.skogsluffarna.se/skin/default/header/logotype.png?t=1722515192",width=120)

if st.session_state.state == 'ongoing' and datetime.now().date() <= datetime.strptime(closing_date, '%Y-%m-%d').date():

    with st.form("update_report"):

        sql_stmt_no_participanst = f"""SELECT count(*) as antal  from participants;"""
        st.session_state.no_of_participants = conn.query(sql_stmt_no_participanst, ttl=600).values.tolist()[0][0]
        # st.write(st.session_state.no_of_participants)

        sql_stmt_no_early_bus = f"""SELECT count(*) as antal  from participants  where transport = 'Tidig buss';"""
        st.session_state.no_earlys_bus = conn.query(sql_stmt_no_early_bus, ttl=600).values.tolist()[0][0]
        # Write directly to the app
        st.title("Anmälan till Skogsluffarnas Träningsläger i Orsa 2026")

        if st.session_state.no_earlys_bus >= 48:
            st.write('OBS! Den tidiga bussen är fullsatt! Platserna fördelas efter anmälningstidpunkt.')
        else:
            st.write('OBS! Nu är det bara ett fåtal platser kvar på den tidiga bussen!')
        
        if st.session_state.no_of_participants == 98:
            st.write('Det är begränsat med platser kvar. Vi gör allt för att alla ska komma med. Invänta besked ifall ni är placerade i kön.')
        elif st.session_state.no_of_participants >= 100:
            st.subheader('Det finns tyvärr inga platser kvar. Gör en anmälan så blir ni placerade på väntelistan!')

        st.write('Använd med fördel Chrome på dator.')
        st.write('Fält markerade med * är obligatoriska.')
        st.write("Ange namn, adress, epost och telefon till ansvarig för anmälan *")
        resp_name = st.text_input("Namn *" )
        st.session_state.resp_name = resp_name
        # print(resp_name)
        
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
        agegroup = st.radio(f"Ange åldersgrupp (ålder vid träningslägret) *", ["Till och med gymnasiet", "18-64 år", "65 år eller äldre"], horizontal=True,)
        if agegroup =="Till och med gymnasiet":
            age = st.text_input(f"Vänligen ange ålder för barnet/ungdomen", "")
            part_ol_traingrp = st.selectbox(f"Ange vilken träningsgrupp i orienteringen du tillhör *",("Rävar","Kaniner","Vit", "Gul", "Orange","Violett", "Vet Ej", "Deltar inte i någon träningsgrupp"))
        else:
            age = None
            part_ol_traingrp = None

           
        # print(age)
        # __diet = st.text_input(f"Ange ev diet eller allergier", "")
        diet = st.multiselect("Ange ev diet eller allergier",["Vegetarian", "Vegan", "Gluten","Laktos", "Nötallergi","Kokosallergi","Mandelallergi","Tomatallergi", "Äter fisk"])
        part_diet = [x for x in diet]

        if st.session_state.no_earlys_bus >= 46:
            st.write('OBS! Den tidiga bussen är fullsatt!')
            transport = st.selectbox(f"Önskad transport till Orsa *",("Tidig buss","Sen buss","Egen Bil"))
        else:
            st.write('OBS! Nu är det bara ett fåtal platser kvar på den tidiga bussen!')
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
            st.session_state.all_parts.append([part_name, agegroup,age,part_ol_traingrp, part_diet, transport, part_telefon, part_mail,skate, part_trainer,part_bbq_comp])
            # print(st.session_state.all_parts)
            st.rerun()
    if st.session_state.add_part == True:
        st.write('Även den som som står som ansvarig, behöver registreras som deltagare!')
        st.write('Registrera alla i sällskapet som ska följa med på träningslägret.')
        if st.button('Lägg till deltagare'):
            vote(st.session_state.signup_ID)

    if st.session_state.all_parts != []:
        st.write('Deltagare som ska följa med. För/Efternamn och Allegi/Diet går att ändra i tabellen.')
        df = pd.DataFrame(st.session_state.all_parts, columns=['För-/Efternamn', 'Åldersgrupp','Ålder','Träningsgrupp OL','Allergi/Diet', 'Transport', 'Telefon', 'E-post', 'Skategrupp','Tränare', 'Tävlingar mm'])
        
        edited_df = st.data_editor(df, disabled=['Åldersgrupp','Transport','Skategrupp','Tränare'], hide_index=True)#
        df_insert = edited_df
        df_insert.rename(columns={'För-/Efternamn':'PART_NAME', 'Åldersgrupp':'AGEGROUP', 'Ålder':'AGE','Träningsgrupp OL':'TRAINING_GROUP','Allergi/Diet':'ALLERGI', 'Transport':'TRANSPORT', 'Telefon':'PHONE','E-post':'MAIL','Skategrupp':'SKATE','Tränare':'TRAINER','Tävlingar mm':'BBQ_COMP'},inplace=True)
        df_insert.insert(0, 'SIGNUP_ID', st.session_state.signup_ID)
        df_insert.insert(5, 'LOAD_DATETIME', st.session_state.load_datetime)
        # print(df_insert)
        if st.button('Slutför anmälan'):
            conn.write_pandas(df_insert, table_name='PARTICIPANTS')
            st.session_state.state = "finished"

            sender_email = st.secrets["send_mail"]["sender_email"] #"k.emil.o.karlsson@gmail.com"
            sender_password = st.secrets["send_mail"]["sender_password"] #"seqj lpou mhcy brbp"
            receiver_email = st.session_state.resp_mail #"emil@sharpedge.se"
            subject = f"Bekräftelse på anmälan till Skogsluffarnas träningsläger ({st.session_state.signup_ID})"
            for idx,item in enumerate(st.session_state.all_parts):
                if idx == 0:
                        msg = 'Amälnda deltagare \n--------------------------\n'
                msg = f'''
                {msg}Deltagare {idx+1}:\n
                - För-/Efternamn: {str(item[0]).replace('[','').replace(']','')}
                - Åldersgrupp: {str(item[1]).replace('[','').replace(']','')}
                - Ålder: {str(item[2]).replace('[','').replace(']','')}
                - Träningsgrupp OL: {str(item[3]).replace('[','').replace(']','')}
                - Allergi/Diet: {str(item[4]).replace('[','').replace(']','')}
                - Transport: {str(item[5]).replace('[','').replace(']','')}
                - Telefon: {str(item[6]).replace('[','').replace(']','')}
                - E-post: {str(item[7]).replace('[','').replace(']','')}
                - Skategrupp: {str(item[8]).replace('[','').replace(']','')}
                - Tränare: {str(item[9]).replace('[','').replace(']','')}
                - Tävlingar mm: {str(item[10]).replace('[','').replace(']','')}
                  --------------------------    
                  '''
            
            
            message = f"""Tack för anmälan
            Bokningsnummer {st.session_state.signup_ID}
            Ansvarig för anmälan {st.session_state.resp_name}
            Epost till ansvarig {st.session_state.resp_mail}
            Telefon till ansvarig {st.session_state.resp_telefon}

            Anmälda deltagare
            {msg}

            Om någon saknas eller någon uppgift blivit fel, kontakta Orsa-gruppen på orsa@skogsluffarna.se. Om ni har fått ett bokningsnummer, skicka gärna med det.        
            """
            send_email(sender_email, sender_password, receiver_email, subject, message)
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
    st.write('Saknas någon eller någon uppgift blivit fel, kontakta Orsa-gruppen på orsa@skogsluffarna.se Om ni har fått ett bokningsnummer, skicka gärna med det.')
    df = pd.DataFrame(st.session_state.all_parts, columns=['För-/Efternamn', 'Åldersgrupp','Ålder','Träningsgrupp OL','Allergi/Diet', 'Transport', 'Telefon', 'E-post', 'Skategrupp','Tränare', 'Tävlingar mm'])
    st.data_editor(df, disabled=['För-/Efternamn', 'Åldersgrupp','Ålder','Träningsgrupp OL','Allergi/Diet', 'Transport', 'Telefon', 'E-post', 'Skategrupp','Tränare', 'Tävlingar mm'], hide_index=True)
elif datetime.now().date() > datetime.strptime(closing_date, '%Y-%m-%d').date():
    st.title('Anmälan till Skogsluffarnas Träningsläger är stängd')