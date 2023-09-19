import streamlit as st
import os
import vobject
import webbrowser
from datetime import datetime, time
from streamlit_lottie import st_lottie
import requests
import requests.exceptions

def main():
    try:
        # Your Streamlit app code here

        # Lottie animation code
        lottie_url = "https://assets2.lottiefiles.com/packages/lf20_ffsp22rc.json"
        lottie_json = requests.get(lottie_url).json()
        st_lottie(lottie_json)

        # Rest of your code

    except requests.exceptions.ConnectionError:
        st.error("Failed to establish an internet connection. Please check your network settings and try again.")


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
          
lottie_coding = load_lottieurl('https://assets2.lottiefiles.com/packages/lf20_ffsp22rc.json') 
lottie_coding2 = load_lottieurl('https://assets1.lottiefiles.com/packages/lf20_rbte8rwr.json')


# Add CSS to hide the Streamlit watermark
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def save_contact(name, phone_number):
    contact = vobject.vCard()
    contact.add('n')
    contact.n.value = vobject.vcard.Name(family=f"{name.split()[-1]} MSV", given=name.split()[0])

    # Add the full name (FN) component
    contact.add('fn')
    contact.fn.value = name

    contact.add('tel')
    contact.tel.value = phone_number

    with open('contacts.vcf', 'a') as file:
        file.write(contact.serialize())

def get_contact_count():
    if os.path.exists('contacts.vcf'):
        with open('contacts.vcf', 'r') as file:
            count = file.read().count('BEGIN:VCARD')
            return count
    else:
        return 0

def is_download_allowed():
    current_time = datetime.now().time()
    end_time = time(21, 40)  # 9:40 PM

    return current_time >= end_time

def is_not_allowed():
    current_time = datetime.now().time()
    start_time = time(24, 00) #12:00 PM

def main():
    

    # Create navigation menu
    menu = ["Home", "Download Vcf", "Website developer", "Privacy policy"]
    choice = st.sidebar.radio ("Menu", menu)

    # Place the menu at the top of the page
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            padding-top: 20px;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    ) 

    if choice == "Home":
        st.header("More Status Views")
        st.write("""Are you tired of your WhatsApp status posts going unnoticed?
        Do you wish to captivate a wider audience with your engaging content? Look no further! Welcome to MSV. Here we give you More WhatsApp status views for free. Feel free to hang by. All we do is host your contact so people with similar interest could download. Tap Submit Contact to get started
        We give free whatsapp VCF file download. Free vcf file for whatsapp to increase your WhatsApp views. All you have to do is to submit your contact now and come back by 9:40 pm to download your assigned VCF file.""")

        st_lottie(lottie_coding, height=400, key="coding")

        st.title("Submit your contact info")
        st.write("Note that Everyday submission is necessary for it to work *Except you go with the premium plan")
        
        # Input fields for name and phone number
        plan = st.selectbox("Select Plan", ["Free", "Premium"])

        if plan == "Free":
            name = st.text_input("Enter your name (Max 8 characters, no spaces)", max_chars=8, key="name_input",
                                help="Enter your name here, maximum characters = 8")
        else:
            name = st.text_input("Enter your name (Unlimited characters, allow spaces)", key="name_input",
                                help="Enter your name here, no character limit")

        phone_number = st.text_input("Phone Number")

        # Save button
        if plan == "Free":
            if st.button("Save Contact"):
                if name and phone_number:
                    save_contact(name, phone_number)
                    st.success("Contact saved successfully!")
                    st.text("")  # Add an empty line for visual separation
                    # Clear the input fields
                    name = ''
                    phone_number = ''
                else:
                    st.error("Please provide both name and phone number.")
        elif plan == "Premium":
            st.write("Please be aware that the premium plan is 200 naira per month")
            if st.button("Save Contact"):
                if name and phone_number:
                    save_contact(name, phone_number)
                    st.success("Contact saved successfully!")
                    st.text("")  # Add an empty line for visual separation
                    # Clear the input fields
                    # Save the VCF entry to a file

                    # Create a VCF entry
                    vcf = vobject.vCard()
                    vcf.add('fn').value = name
                    vcf.add('tel').value = phone_number

                    # Serialize the VCF entry to a string and encode it as bytes
                    vcf_data = vcf.serialize().encode('utf-8')

                    # Save the VCF entry to a file in binary write mode ('wb')
                    with open('premium_contacts.vcf', 'wb') as vcf_file:
                        vcf_file.write(vcf_data)

                    name = ''
                    phone_number = ''
                    # Redirect to external link
                    webbrowser.open_new_tab("https://tinyurl.com/MSVpremium")  # Replace with your desired external link
                else:
                    st.error("Please provide both name and phone number.")

        # Display contact count
        contact_count = get_contact_count()
        #st.header("Compiled Contacts")
        st.write(str(contact_count) +" compiled contacts today")


    elif choice == "Download Vcf":
        st_lottie(lottie_coding2, height=400, key="coding")
        if is_download_allowed():
            # Download button
            if os.path.exists('contacts.vcf'):
                st.download_button("Download Contacts", data='contacts.vcf', file_name='contacts.vcf')
            else:
                st.info("No contacts found.")
        else:
            st.warning("Downloads are only available after 9:40 PM.")
        st.write("Downloads are only available from 9:40pm to 12:00 midnight")
        
    elif choice == "Website developer":
        st.header("About the maker of this website")
        st.write("Name: Goldman Precious Kalu ")
        st.write("Age: 14")
        st.write("Status: Done with secondary School")
        st.header("About")
        st.write("")
        st.write("Goldman precious is a web developer who studied in primewill city colleg during his secondary school and finished at the age of 13, and then ventured into web development where he obtained a certificate in python.")
        st.write("This website was made with python, the idea behind it, the algorithm and the code belongs to him, he is a promising young man looking to find a future in the world of technology.")
        
    
    elif choice == "Privacy policy":
        st.header("Privacy policy")
        with open("privacypolicy.txt", "r") as file:
            text_content = file.read()
        st.write(text_content)
        #st.write("All you need to do is Click the link or button below where you will be redirected to speak with us directly on whatsapp")


        #if st.button("Talk with admin on whatsapp"):
        #    link = "https://tinyurl.com/MSVpremium"
        #    st.markdown(f'<a href="{link}" target="_blank">Talk with Admin on whatsapp</a>', unsafe_allow_html=True)
    
    # Disclaimer text at the bottom
    st.markdown(
        """
        <br><br>
        <div style="text-align: center;">
        <p style="font-size: 10px; color: #888888;">
        Disclaimer: This website is not affiliated with WhatsApp or any of its subsidiaries in any way. All activities here are not related to WhatsApp LLC
        Disclaimer: All transactions carried out involving any MSV contact is at your discretion. Be Wise!\n
        © Copyright 2023 MoreStatusViews - Get more WhatsApp Status views
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == '__main__':
    main()
