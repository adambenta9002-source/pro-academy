
import streamlit as st
import json
from pathlib import Path

st.set_page_config(
    page_title="PRO | Football Academy",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- STYLE ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 85% 0%, #153c2b 0%, transparent 38%),
        linear-gradient(140deg, #080d0b, #111b15 55%, #080d0b);
    color: #f4f7f3;
    font-family: 'Inter', sans-serif;
}
.block-container {max-width: 1050px; padding-top: 2rem;}
h1, h2, h3 {font-family: 'Barlow Condensed', sans-serif !important;}
h1 {font-size: 4rem !important; font-weight: 900 !important;}
h2 {font-size: 2.3rem !important;}
h3 {font-size: 1.5rem !important;}
p, label {color: #d1dbd3;}
.eyebrow {
    color: #7df7a2; letter-spacing: 4px;
    font-size: 12px; font-weight: 800;
}
.hero {
    padding: 30px; border-radius: 22px;
    border: 1px solid #2c4635;
    background: linear-gradient(120deg, #172b20, #101813);
    margin-bottom: 22px;
}
.metric {
    background: #142019; border: 1px solid #2b4031;
    padding: 17px; border-radius: 15px; text-align: center;
}
.metric strong {font-size: 26px; color: #80f5a1;}
.metric span {font-size: 12px; color: #aab9ae;}
.drill {
    background: #121b15; border: 1px solid #2b3d30;
    padding: 14px 18px; border-radius: 12px; margin: 7px 0;
}
div.stButton > button {
    background: #82f5a1; color: #07120a;
    border: none; border-radius: 10px;
    font-weight: 800; min-height: 46px;
}
div.stButton > button:hover {
    background: #b1ffc3; color: #07120a;
}
div[data-testid="stProgressBar"] > div > div {
    background: #82f5a1;
}
</style>
""", unsafe_allow_html=True)

# ---------- TRAINING PLAN ----------
days = [
    {
        "name": "DAY 1",
        "title": "SPEED & DRIBBLING",
        "day": "MONDAY",
        "duration": "65–75 MIN",
        "focus": "Acceleration, close control and attacking space.",
        "drills": [
            ("Warm-up jog", "3 minutes", "Easy pace."),
            ("Dynamic warm-up", "5 minutes", "Leg swings, hip movements and high knees."),
            ("Progressive accelerations", "3 runs", "Build speed gradually."),
            ("10-metre sprints", "4 reps", "Fast, controlled starts. Rest 60–90 seconds."),
            ("20-metre sprints", "4 reps", "Fast with good form. Rest 90–120 seconds."),
            ("Right-foot cone dribbling", "4 runs", "Keep the ball close."),
            ("Left-foot cone dribbling", "4 runs", "Use small touches and look up."),
            ("Alternating-feet dribbling", "4 runs", "Change pace after the final cone."),
            ("Wall passing", "3 × 2 minutes", "Alternate one-touch and two-touch passes."),
            ("First touch", "5 minutes", "Receive across your body and turn."),
            ("Cooldown walk", "5 minutes", "Walk until your breathing settles.")
        ]
    },
    {
        "name": "DAY 2",
        "title": "BALL CONTROL & PASSING",
        "day": "TUESDAY",
        "duration": "60–70 MIN",
        "focus": "First touch, weak foot, passing and midfielder turns.",
        "drills": [
            ("Warm-up", "10 minutes", "Light jog and dynamic movements."),
            ("Toe taps", "2 × 45 seconds", "Stay balanced over the ball."),
            ("Foundations", "2 × 45 seconds", "Move the ball between both feet."),
            ("Inside-outside touches", "2 × 45 seconds", "Use both feet."),
            ("Sole rolls", "2 × 45 seconds", "Roll the ball across your body."),
            ("Pull-push", "2 × 45 seconds", "Pull back, push forward."),
            ("Weak-foot dribbling", "5 minutes", "Keep control while moving."),
            ("Right-foot wall passes", "50 passes", "Aim for the same target."),
            ("Left-foot wall passes", "50 passes", "Focus on accuracy."),
            ("One-touch passing", "20 each foot", "Stay relaxed and balanced."),
            ("Receive and turn", "10 minutes", "Scan before receiving when possible."),
            ("Cooldown", "5 minutes", "Walk and relax.")
        ]
    },
    {
        "name": "DAY 3",
        "title": "STAMINA & CONDITIONING",
        "day": "THURSDAY",
        "duration": "50–65 MIN",
        "focus": "Aerobic fitness and recovering between runs.",
        "drills": [
            ("Warm-up", "10 minutes", "Jog easily and move dynamically."),
            ("Easy continuous run", "15–20 minutes", "Conversational pace. Walk when needed."),
            ("20-metre controlled runs", "6 reps", "Run at 75–85% effort; walk back."),
            ("Recovery", "2–3 minutes", "Rest before continuing."),
            ("Optional extra runs", "2–4 reps", "Only if you feel recovered and move well."),
            ("Ball intervals", "8 minutes", "30 seconds controlled, 30 seconds quicker."),
            ("Cooldown walk", "5 minutes", "Let your breathing settle.")
        ]
    },
    {
        "name": "DAY 4",
        "title": "WINGER SKILLS & AGILITY",
        "day": "SATURDAY",
        "duration": "65–80 MIN",
        "focus": "One-v-one moves, acceleration with the ball and finishing.",
        "drills": [
            ("Warm-up", "10 minutes", "Jog, dynamic movements and light touches."),
            ("Agility runs", "4 reps", "Change direction under control."),
            ("Zigzag cone dribbling", "4 runs", "Use both feet."),
            ("Cut inside", "6–8 reps", "Feint, move inside and accelerate."),
            ("Go down the line", "6–8 reps", "Push into space and accelerate."),
            ("Crossing or target passing", "10 reps each side", "Aim for a specific target."),
            ("Match-style circuit", "4 rounds", "Dribble, change direction, then recover."),
            ("Finishing", "20 shots", "Prioritise accuracy with both feet."),
            ("Cooldown walk", "5 minutes", "Walk and recover.")
        ]
    }
]

# ---------- SAVE PROGRESS ----------
PROGRESS_FILE = Path.home() / "football-training-progress.json"

if "progress" not in st.session_state:
    try:
        st.session_state.progress = json.loads(
            PROGRESS_FILE.read_text()
        )
    except (FileNotFoundError, json.JSONDecodeError):
        st.session_state.progress = {}

if "week" not in st.session_state:
    st.session_state.week = 1

if "day_index" not in st.session_state:
    st.session_state.day_index = 0

def save_progress():
    PROGRESS_FILE.write_text(json.dumps(st.session_state.progress))

# ---------- HEADER ----------
st.markdown('<div class="eyebrow">YOUR PERSONAL FOOTBALL DEVELOPMENT PLAN</div>',
            unsafe_allow_html=True)
st.markdown("# PRO<span style='color:#82f5a1'>.</span> ACADEMY",
            unsafe_allow_html=True)
st.write("Eight weeks. Four sessions per week. Get better every session.")

# Week selector
week_options = list(range(1, 9))
st.select_slider(
    "TRAINING WEEK",
    options=week_options,
    key="week"
)

day = days[st.session_state.day_index]
session_key = f"week_{st.session_state.week}_day_{st.session_state.day_index}"

# ---------- HERO ----------
st.markdown(f"""
<div class="hero">
  <div class="eyebrow">WEEK {st.session_state.week:02d} / 08 &nbsp; • &nbsp; {day['day']}</div>
  <h1 style="margin:4px 0 0 0">{day['title']}</h1>
  <p>{day['focus']}</p>
  <div style="color:#82f5a1;font-weight:800">{day['duration']}</div>
</div>
""", unsafe_allow_html=True)

# Day navigation
nav = st.columns([1, 2, 1])
with nav[0]:
    if st.button("← PREVIOUS", use_container_width=True):
        st.session_state.day_index = (st.session_state.day_index - 1) % len(days)
        st.rerun()
with nav[1]:
    st.markdown(
        f"<p style='text-align:center;font-weight:800'>"
        f"{st.session_state.day_index + 1} / {len(days)} TRAINING SESSIONS</p>",
        unsafe_allow_html=True
    )
with nav[2]:
    if st.button("NEXT DAY →", use_container_width=True):
        st.session_state.day_index = (st.session_state.day_index + 1) % len(days)
        st.rerun()

st.progress((st.session_state.day_index + 1) / len(days),
            text="Weekly session sequence")

# ---------- DRILLS ----------
st.markdown("## YOUR SESSION")
st.write("Complete each drill and tick it off below.")

completed = 0
for i, (name, amount, instructions) in enumerate(day["drills"]):
    key = f"{session_key}_drill_{i}"
    if key not in st.session_state:
        st.session_state[key] = st.session_state.progress.get(key, False)

    with st.container():
        left, right = st.columns([5, 1])
        with left:
            st.markdown(f"**{i + 1:02d}  {name}**")
            st.caption(f"{amount}  ·  {instructions}")
        with right:
            st.checkbox("Done", key=key, label_visibility="visible")

    st.divider()
    if st.session_state[key]:
        completed += 1
        st.session_state.progress[key] = True
    else:
        st.session_state.progress[key] = False

save_progress()
percentage = int(completed / len(day["drills"]) * 100)

st.markdown("## SESSION PROGRESS")
st.progress(percentage / 100, text=f"{completed}/{len(day['drills'])} drills completed · {percentage}%")

if completed == len(day["drills"]):
    st.success("SESSION COMPLETE! Great work. Recover, hydrate and get ready for the next session.")

# ---------- NOTES ----------
st.markdown("## SESSION NOTES")
note_key = f"{session_key}_notes"
if note_key not in st.session_state:
    st.session_state[note_key] = st.session_state.progress.get(note_key, "")

st.text_area(
    "Record your sprint times, how you felt, and what to improve next time.",
    key=note_key
)
st.session_state.progress[note_key] = st.session_state[note_key]
save_progress()

st.markdown("---")
st.caption("Train smart. Rest between sprints. Stop if you feel pain. Progress comes from consistency.")
import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="Pro Football Training", page_icon="⚽", layout="centered")

st.markdown("""
<style>
.stApp {background-color: #101510; color: white;}
h1, h2, h3 {color: #70ef83;}
div.stButton > button {border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

st.title("⚽ PRO FOOTBALL")
st.subheader("Your 8-Week Training Plan")

workouts = {
    "Monday — Speed": [
        ("Warm-up jog", "3 min"),
        ("Dynamic stretches", "4 min"),
        ("Gradual accelerations", "3 min"),
        ("10-metre sprints", "4 reps — rest 60–90 sec"),
        ("20-metre sprints", "4 reps — rest 90–120 sec"),
        ("Right-foot cone dribbling", "4 runs"),
        ("Left-foot cone dribbling", "4 runs"),
        ("Alternating-feet dribbling", "4 runs"),
        ("Wall passing", "3 × 2 min"),
        ("First-touch practice", "5 min"),
        ("Finishing", "10 shots each foot"),
        ("Cooldown walk", "5 min"),
    ],
    "Tuesday — Ball Control": [
        ("Warm-up", "10 min"),
        ("Toe taps", "45 sec"),
        ("Foundations", "45 sec"),
        ("Inside-outside touches", "45 sec"),
        ("Sole rolls", "45 sec"),
        ("Pull-push movements", "45 sec"),
        ("Weak-foot dribbling", "45 sec"),
        ("Repeat ball mastery circuit", "2 rounds"),
        ("Right-foot wall passes", "50 passes"),
        ("Left-foot wall passes", "50 passes"),
        ("One-touch passing", "20 each foot"),
        ("First touch across body", "20 reps"),
        ("Turning drills", "10 min"),
        ("Cooldown", "5 min"),
    ],
    "Thursday — Stamina": [
        ("Warm-up", "10 min"),
        ("Easy conversational run", "20 min"),
        ("20-metre controlled runs", "6 reps at 75–85%"),
        ("Walk back and recover", "After each run"),
        ("Extra runs if recovered", "4 reps"),
        ("Ball dribbling intervals", "10 min: 30 sec quick, 30 sec easy"),
        ("Cooldown walk", "5 min"),
    ],
    "Saturday — Winger Skills": [
        ("Warm-up", "10 min"),
        ("Agility runs without ball", "4 reps"),
        ("Zigzag cone dribbling", "4 runs"),
        ("Change-of-direction drills", "4 reps"),
        ("Cut inside and accelerate", "8 reps"),
        ("Go down the line", "8 reps"),
        ("Match-conditioning circuit", "5 rounds"),
        ("Finishing practice", "30 shots"),
        ("Cooldown walk", "5 min"),
    ],
}

day = st.selectbox("Choose your training day", list(workouts.keys()))

st.markdown("---")
st.header(day)

st.write("Tick each exercise when you finish it.")

if "completed" not in st.session_state:
    st.session_state.completed = {}

if "selected_day" not in st.session_state:
    st.session_state.selected_day = day

if st.session_state.selected_day != day:
    st.session_state.selected_day = day

items = workouts[day]
done = 0

for i, (exercise, amount) in enumerate(items):
    key = f"{day}_{i}"
    checked = st.checkbox(f"{exercise} — {amount}", key=key)
    if checked:
        done += 1

progress = done / len(items)
st.progress(progress)
st.write(f"**Progress: {done}/{len(items)} exercises ({int(progress * 100)}%)**")

if done == len(items):
    st.success("🔥 Session completed! Great work!")

st.markdown("---")
st.header("⏱️ Training Timer")

minutes = st.number_input("Minutes", min_value=0, max_value=120, value=1)
seconds = st.number_input("Seconds", min_value=0, max_value=59, value=0)
total_seconds = int(minutes * 60 + seconds)

if st.button("Start timer"):
    st.session_state.timer_seconds = total_seconds

if "timer_seconds" in st.session_state:
    st.write(f"Timer set: {st.session_state.timer_seconds} seconds")
    st.caption("Use your phone's timer or stopwatch to count down during your drill.")

st.markdown("---")
st.header("📈 8-Week Progress")

week = st.select_slider("Current training week", options=list(range(1, 9)), value=1)
st.write(f"Week {week} of 8")

notes = st.text_area("Training notes", placeholder="Record your sprint times, passing progress, or how you felt today...")
st.caption("Tip: Aim for quality, rest between sprints, and stop if you feel pain.")
