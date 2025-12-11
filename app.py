import gradio as gr
from groq import Groq
import json
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

DB = "database.json"

if not os.path.exists(DB):
    with open(DB, "w") as f:
        json.dump([], f)

def save_to_db(city, days, budget, plan):
    with open(DB, "r") as f:
        data = json.load(f)
    data.append({"city": city, "days": days, "budget": budget, "plan": plan})
    with open(DB, "w") as f:
        json.dump(data, f, indent=4)

pakistan_cities = [
    "Islamabad", "Lahore", "Karachi", "Multan", "Quetta", "Peshawar",
    "Faisalabad", "Skardu", "Hunza", "Naran", "Kaghan", "Murree",
    "Swat", "Gilgit", "Hyderabad"
]

def plan_trip(city, days, budget):

    if not city or not days or not budget:
        return "❌ Please fill all fields."

    prompt = f"""
    Create a detailed trip plan with:
    - Best attractions
    - Best hotels
    - Local food
    - Daily schedule
    - Safety + budget tips
    City: {city}
    Days: {days}
    Budget: {budget} PKR
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        plan = response.choices[0].message.content
        save_to_db(city, days, budget, plan)
        return plan

    except Exception as e:
        return f"❌ Error: {str(e)}"


css = """
#main-box {
    background: linear-gradient(135deg, #0d0d0d, #1f1f1f);
    color: white;
    padding: 30px;
    border-radius: 20px;
    max-width: 750px;
    margin: auto;
    box-shadow: 0 0 40px #ff00ff55;
}
.input-card {
    background: #ffffff15;
    padding: 15px;
    border-radius: 12px;
    backdrop-filter: blur(10px);
}
"""

with gr.Blocks(css=css, theme=gr.themes.Soft(primary_hue="pink")) as demo:
    gr.HTML("<h1 style='text-align:center; color:#ff66cc;'>✨ AI Trip Planner</h1>")

    with gr.Column(elem_id="main-box"):
        city = gr.Dropdown(pakistan_cities, label="🏙 City", value=pakistan_cities[0], elem_classes="input-card")
        days = gr.Textbox(label="📆 Days", elem_classes="input-card")
        budget = gr.Textbox(label="💰 Budget (PKR)", elem_classes="input-card")

        btn = gr.Button("✨ Generate Travel Plan")
        out = gr.Textbox(lines=20, label="📘 Trip Plan")

        btn.click(plan_trip, [city, days, budget], out)

demo.launch()
