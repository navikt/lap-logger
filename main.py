import streamlit as st
import streamlit.components.v1 as components

from config import ANTALL_RUNDER, EVENT_DATO, RUNDE_START_TIME
from sider import registrering, runder, totaloversikt, leaderboard
from datetime import datetime


st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        .block-container { padding-top: 1.5rem; }
        [data-testid="stStatusWidget"] { display: none !important; }
        header [data-testid="stStatusWidget"] { display: none !important; }
        .stAppRunningIcon { display: none !important; }
        #stStatusWidget { display: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Overskrift med countdown til arrangementet
event_start = datetime(*EVENT_DATO, hour=RUNDE_START_TIME)
naa = datetime.now()
col_title, col_cd = st.columns([3, 2])
with col_title:
    st.title("Nav Backyard 2026 🤘🏻💥")
with col_cd:
    if naa < event_start:
        components.html(f"""
        <style>html,body{{background:transparent;margin:0;padding:0;}}</style>
        <div id="cd" style="text-align:right;padding-top:0.8rem;font-family:'Source Sans Pro',sans-serif;">
            <span style="font-size:0.9rem;">⏱️ Starter om</span><br>
            <span id="t" style="font-size:1.5rem;font-weight:700;">…</span>
        </div>
        <script>
        const T=new Date("{event_start.isoformat()}").getTime();
        function u(){{let d=Math.max(0,Math.floor((T-Date.now())/1000));
        const D=Math.floor(d/86400);d%=86400;const h=Math.floor(d/3600);d%=3600;
        const m=Math.floor(d/60),s=d%60,p=n=>String(n).padStart(2,'0');
        let t="";if(D>0)t+=D+"d ";if(D>0||h>0)t+=p(h)+"t ";t+=p(m)+"m "+p(s)+"s";
        document.getElementById("t").textContent=t;}}
        u();setInterval(u,1000);
        try{{const bg=window.parent.document.querySelector('[data-testid="stAppViewContainer"]');
        const c=bg?window.parent.getComputedStyle(bg).backgroundColor:'';const m=c.match(/\\d+/g);
        document.getElementById("cd").style.color=m&&(+m[0]+ +m[1]+ +m[2])/3<128?"rgba(255,255,255,0.87)":"rgba(0,0,0,0.87)";
        }}catch(e){{}}
        </script>
        """, height=70)

# --------------- faner ---------------

fane_navn = (
    ["Registrering"]
    + [f"Runde {i}" for i in range(1, ANTALL_RUNDER + 1)]
    + ["Totaloversikt", "Leaderboard"]
)

faner = st.tabs(fane_navn)

registrering.vis(faner[0])
runder.vis(faner)
totaloversikt.vis(faner[ANTALL_RUNDER + 1])
leaderboard.vis(faner[ANTALL_RUNDER + 2])
