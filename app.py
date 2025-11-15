import streamlit as st
import datetime
import io
import textwrap

st.set_page_config(page_title="Brent Tolentino — Portfolio", layout="wide")

# Inject custom dark theme with green (#66a04c) accents
st.markdown(
    """
    <style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@300;400;500;600&display=swap');

    /* Base font for all text */
    * {
        font-family: 'Montserrat', sans-serif !important;
    }

    /* Headers use Bebas Neue */
    h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'Bebas Neue', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 1px;
    }
    body, .stApp {
        background-color: #0f0f0f !important;
        color: #e0e0e0 !important;
    }
    .stButton button {
        background-color: #66a04c !important;
        color: black !important;
        border-radius: 6px;
    }
    .stDownloadButton button {
        background-color: #66a04c !important;
        color: black !important;
        border-radius: 6px;
    }
    h1, h2, h3, h4, h5, h6, .stMarkdown, .stText, label, .stCaption {
        color: #d2f8c2 !important;
    }
    .css-1kyxreq, .css-18e3th9, .css-1d391kg { /* input boxes */
        background-color: #1a1a1a !important;
        color: #e0e0e0 !important;
        border: 1px solid #66a04c !important;
    }
    
    /* Sidebar background + text */
    [data-testid="stSidebar"], .css-1lcbmhc, .css-1avcm0n, .css-1d2xq0k {
        background-color: #0f0f0f !important;
        color: #e0e0e0 !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }

    /* Sidebar inputs, uploaders, buttons */
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea,
    [data-testid="stSidebar"] select {
        background-color: #1a1a1a !important;
        color: #e0e0e0 !important;
        border: 1px solid #66a04c !important;
    }

    [data-testid="collapsedControl"] svg {
        fill: #e0e0e0 !important;
    }

    [data-testid="stSidebar"] button {
        background-color: #66a04c !important;
        color: black !important;
    }

        /* Top header / Toolbar (main menu + settings) */
    [data-testid="stHeader"], header, .css-18ni7ap, .css-1rs6os {
        background-color: #0f0f0f !important;
        color: #e0e0e0 !important;
    }

    /* Remove Streamlit default shadow on header */
    [data-testid="stHeader"] {
        box-shadow: none !important;
    }

    /* Top bar text/icons */
    [data-testid="stHeader"] * {
        color: #e0e0e0 !important;
    }

        /* Global text inputs, text areas, select boxes */
    input[type="text"], textarea, select, .stTextInput > div > div > input {
        background-color: #1a1a1a !important;
        color: #e0e0e0 !important;
        border: 1px solid #66a04c !important;
    }

    /* Streamlit new class names for text areas & inputs */
    [data-baseweb="textarea"], [data-baseweb="input"] {
        background-color: #1a1a1a !important;
        color: #e0e0e0 !important;
        border: 1px solid #66a04c !important;
    }

    /* Adjust placeholder text color */
    ::placeholder {
        color: #aaaaaa !important;
        opacity: 0.7 !important;
    }

    /* FILE UPLOADER (dark mode fix) */
    [data-testid="stFileUploader"] > section > div {
        background-color: #1a1a1a !important;  /* background of the box */
        border: 1px solid #2a2a2a !important;
        color: white !important;
        border-radius: 8px !important;
    }

    /* Text inside uploader */
    [data-testid="stFileUploader"] * {
        color: white !important;
    }

    /* Drag-and-drop area */
    [data-testid="stFileUploaderDropzone"] {
        background-color: #1a1a1a !important;
        border: 2px dashed #3cb371 !important;  /* your green accent */
        border-radius: 10px !important;
    }

    /* Hover effect */
    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: #46d48d !important;
        background-color: #1f1f1f !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Helper data (pre-filled from your conversations) ----------
USER = {
    "full_name": "Brent Tolentino",
    "handle": "renthehuman",
    "location": "Philippines",
    "bio": (
        "I'm Brent (aka renthehuman), a software developer and systems tinkerer. "
        "I work on game development, android development, web apps (Django, Spring Boot), experiment with virtualization and GPU passthrough on Linux, "
        "and enjoy debugging hardware/software issues such as Wi‑Fi drivers and system services(on my spare time)."
    ),
    "email": "johndoe@gmail.com",
    "avatar": None,  # leave None so user can upload
}

SKILLS = [
    "Python",
    "Django",
    "Spring Boot / Java",
    "Linux (Mint, kernel tinkering)",
    "System virtualization (QEMU/KVM)",
    "GPU passthrough (vfio, PCI binding)",
    "Containers & systemd",
    "Troubleshooting (networking, drivers)",
    "Game development (Java, LibGDX, Roblox Lua)",
    "Android development (Java, Android Studio)",
]

PROJECTS = [
    { "title": "Geolocator (C#)", "summary": "A project I made during the summer.", "tags": ["C#", "Git", "Backend"], "link": "https://github.com/BrentTolentino/Geolocator", }, { "title": "Calm Code (Android Studio)", "summary": "An Android Studio application used for meditation and coding.", "tags": ["Java", "Android Studio", "Mobile"], "link": "https://github.com/BladeLucas27/CalmCode", }, { "title": "GPU Passthrough Lab", "summary": "Experiments with passing through AMD Radeon 680M and NVIDIA RTX 3060 to Windows guests using vfio-pci and OVMF.", "tags": ["QEMU/KVM", "vfio", "Windows"], "link": "no link available", }, { "title": "Danny German (Pixel Game made in Java)", "summary": "Created an Old School RPG game in Java.", "tags": ["Java", "Game Development"], "link": "https://github.com/BrentTolentino/RPG_GAME", },
]

EXTRA = {
    "education": "BS Computer Science (active student/projects)",
    "interests": ["OS internals", "virtualization", "web development", "system reliability", "open source software", "gaming"],
}

# ----------------- UI -----------------

with st.sidebar:
    st.image("https://static.streamlit.io/examples/dice.jpg", width=120)
    st.title(USER["full_name"])
    st.caption(f"@{USER['handle']} — {USER['location']}")
    st.markdown("---")

    uploaded_avatar = st.file_uploader("Upload avatar (optional)", type=["png", "jpg", "jpeg"])
    if uploaded_avatar is not None:
        USER["avatar"] = uploaded_avatar.read()

    st.markdown("**Quick actions**")
    if st.button("Download resume (MD)"):
        # generate a simple markdown resume and trigger download
        md = textwrap.dedent(f"""
        # {USER['full_name']}
        @{USER['handle']} — {USER['location']}

        ## Bio
        {USER['bio']}

        ## Skills
        {', '.join(SKILLS)}

        ## Projects
        """
        )
        for p in PROJECTS:
            md += f"- **{p['title']}** — {p['summary']}\n"
        st.download_button("Click to download", data=md.encode('utf-8'), file_name="resume.md", mime="text/markdown")

    st.markdown("---")
    st.markdown("Built with Streamlit — edit this app to personalize it.")

# main layout
col1, col2 = st.columns([2, 1])

with col1:
    st.header("About me")
    # editable bio
    bio_text = st.text_area("Short autobiography", value=USER["bio"], height=160)

    st.markdown("**Education & Interests**")
    st.write(EXTRA["education"])
    st.write(', '.join(EXTRA["interests"]))

    st.markdown("---")

    st.subheader("Selected projects")
    for p in PROJECTS:
        st.markdown(f"### {p['title']}")
        st.write(p['summary'])
        if p['tags']:
            st.write("Tags: ", ', '.join(p['tags']))
        if p['link']:
            st.markdown(f"[Project link]({p['link']})")
        st.markdown("---")

    st.subheader("Technical notes & logs")
    st.info(
        "I keep short entries here about kernel logs, virtualization experiments (vfio, OVMF), and troubleshooting steps. "
        "Drop in dmesg excerpts or paste notes for quick reference."
    )
    logs = st.text_area("Paste debugging notes or dmesg excerpts", height=140)

    st.markdown("---")
    st.subheader("Share / Export")
    export_md = st.checkbox("Include biography & projects in export (Markdown)", value=True)
    if st.checkbox("Generate shareable profile link (query params)"):
        # create a simple shareable query param string
        params = {
            "name": USER['full_name'].replace(' ', '+'),
            "bio": bio_text[:200].replace('\n', ' ')
        }
        query = f"?name={params['name']}&bio={params['bio']}"
        st.write("Shareable URL fragment:")
        st.code(query)

with col2:
    st.subheader("Profile")
    if USER['avatar']:
        st.image(USER['avatar'], width=200)
    else:
        st.image("https://avatars.dicebear.com/api/identicon/" + USER['handle'] + ".png", width=200)

    st.markdown(f"**{USER['full_name']}**")
    st.caption(f"@{USER['handle']} — {USER['location']}")

    st.markdown("**Skills**")
    for s in SKILLS:
        st.markdown(f"- {s}")

    st.markdown("---")
    st.subheader("Contact")
    col_a, col_b = st.columns([2,3])
    with col_a:
        email = st.text_input("Email", value=USER.get('email',''))
    with col_b:
        subject = st.text_input("Subject", value="Hello from your portfolio")

    if st.button("Prepare email link"):
        if email:
            mailto = f"mailto:{email}?subject={subject}"
            st.markdown(f"[Click to open email client]({mailto})")
        else:
            st.warning("Please put your contact email first.")

    st.markdown("---")
    st.subheader("Utilities")
    if st.button("Generate short CV (one‑page markdown)"):
        cv = generate_cv(USER, SKILLS, PROJECTS, bio_text)
        st.download_button("Download CV (MD)", data=cv.encode('utf-8'), file_name="cv.md", mime="text/markdown")

# ---------- functions ----------

def generate_cv(user, skills, projects, bio):
    """Return a simple markdown CV string."""
    md = []
    md.append(f"# {user['full_name']}")
    md.append(f"@{user['handle']} — {user['location']}\n")
    md.append("## Bio")
    md.append(bio)
    md.append("\n## Skills")
    md.append('\n'.join([f"- {s}" for s in skills]))
    md.append("\n## Projects")
    for p in projects:
        md.append(f"- **{p['title']}** — {p['summary']}")
    return '\n\n'.join(md)

# Small footer
st.markdown("---")
st.caption(f"Generated: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")

# End of file