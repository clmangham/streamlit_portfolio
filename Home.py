import streamlit as st
import base64

def home():

    # Page configs (tab title, favicon)
    st.set_page_config(
        page_title="Camaron Mangham's Portfolio",
        # page_icon="🍕",
    )

    # CSS styles file
    with open("styles/main.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Profile image file
    with open("assets/diffusion_me.png", "rb") as img_file:
        img = "data:image/png;base64," + base64.b64encode(img_file.read()).decode()

    # PDF CV file
    with open("assets/CamaronMangham_Resume.pdf", "rb") as pdf_file:
        pdf_bytes = pdf_file.read()

    # Top title
    st.write(f"""<div class="title"><strong>Camaron Mangham</strong></div>""", unsafe_allow_html=True)

    # Profile image
    # st.write(f"""
    # <div class="container">
    #     <div class="box">
    #         <div class="spin-container">
    #             <div class="shape">
    #                 <div class="bd">
    #                     <img src="{img}" alt="Enric Domingo">
    #                 </div>
    #             </div>
    #         </div>
    #     </div>
    # </div>
    # """, 
    # unsafe_allow_html=True)

    # Alternative image (static and rounded) uncomment it if you prefer this one
    st.write(f"""
    <div style="display: flex; justify-content: center;">
       <img src="{img}" alt="Camaron Mangham" width="300" height="300" style="border-radius: 50%; object-fit: cover; margin-top: 40px; margin-bottom: 40px;">
    </div>
    """, unsafe_allow_html=True)
    
    # Subtitle
    st.write(f"""<div class="subtitle" style="text-align: center;">Data Scientist & Machine Learning Engineer</div>""", unsafe_allow_html=True)
    
    # Social Icons
    social_icons = {
        # Platform: [URL, Icon]
        "LinkedIn": ["https://www.linkedin.com/in/clmangham/", "https://cdn-icons-png.flaticon.com/512/174/174857.png"],
        "GitHub": ["https://github.com/clmangham", "https://icon-library.com/images/github-icon-white/github-icon-white-6.jpg"],
    }

    social_icons_html = [f"<a href='{social_icons[platform][0]}' target='_blank' style='margin-right: 20px;'><img class='social-icon' src='{social_icons[platform][1]}'' alt='{platform}''></a>" for platform in social_icons]

    st.write(f"""
    <div style="display: flex; justify-content: center; margin-bottom: 20px;">
        {''.join(social_icons_html)}
    </div>""", 
    unsafe_allow_html=True)

    st.write("##")

    # About me section
    st.subheader("About Me")
    st.write("""
    I am an applied data scientist and machine learning practitioner with a background in biology. I enjoy transforming data into knowledge and bringing structure to ambiguous problems.

    As a neurobiology researcher @ Duke University, I worked on computational approaches to understand how neuronal signals in the visual cortex guide behaviors.

    As a biology consultant @ Cornell University, I worked with diverse groups of researcers, students, and staff while managing a wide range of projects.

    I am passionate about **Data Science & Machine Learning/Deep Learning, MLOps, Data Engineering, Bioinformatics, Automation**, and more!

    I'm also an avid gamer 🎮 and enjoy hiking 🥾 and kickboxing 🥊

    Let's connect!

    📫 How to reach me: camaron.mangham@gmail.com

    🏠 Atlanta, Georgia
    """)

    st.write("##")

    # Download CV button
    st.download_button(
        label="📄 Download my Resume",
        data=pdf_bytes,
        file_name="CamaronMangham_Resume.pdf",
        mime="application/pdf",
    )

    st.write("##")

    st.write(f"""<div class="subtitle" style="text-align: center;">⬅️ Check out my Projects in the navigation menu! (More coming soon...)</div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    home()
