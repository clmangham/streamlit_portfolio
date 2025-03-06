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

    # Alternative image (static and rounded) uncomment it if you prefer this one
    st.write(f"""
    <div style="display: flex; justify-content: center;">
       <img src="{img}" alt="Camaron Mangham" width="300" height="300" style="border-radius: 50%; object-fit: cover; margin-top: 40px; margin-bottom: 40px;">
    </div>
    """, unsafe_allow_html=True)

    # Subtitle
    st.write(f"""<div class="subtitle" style="text-align: center;">AI & Data Systems Architect</div>""", unsafe_allow_html=True)

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
    I’m an AI & Data Systems Architect and all-around tech enthusiast. I’m always exploring new ideas, whether it’s building AI-driven systems, expanding my home lab, or diving deeper into data, security, and automation.

    Currently, I’m obsessed with AI, cybersecurity, and engineering robust data systems. I love working on interesting projects and talking about tech in general. Let’s connect!
    """)

    st.write("##")

    # Download CV button
    # st.download_button(
    #     label="📄 Download my Resume",
    #     data=pdf_bytes,
    #     file_name="CamaronMangham_Resume.pdf",
    #     mime="application/pdf",
    # )

    # st.write("##")

    # st.write(f"""<div class="subtitle" style="text-align: center;">⬅️ Check out my Projects in the navigation menu! (More coming soon...for now checkout my GitHub profile!)</div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    home()
