import gradio as gr
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

# ======================
# Toggle between Mock / Real API
# ======================
USE_MOCK = True  # Set False to use the real Cerebras API

# ======================
# Instantiate client (only if not using mock)
# ======================
if not USE_MOCK:
    client = InferenceClient(
        provider="cerebras",
        model="cerebras/btlm-3b-8k-base",
        api_key=os.environ["HF_TOKEN"]
    )

# ======================
# Mock function for testing UI
# ======================
def generate_idiom_mock(situation: str):
    idiom = "对症下药"
    explanation = "duì zhèng xià yào<br><br>To prescribe the right medicine; to take the right approach to a problem."
    return idiom, explanation

# ======================
# Real API function
# ======================
def generate_idiom(situation: str, client):
    prompt = f"""
You are a wise assistant. Given a situation, respond with exactly:
1. A Chinese idiom (成语)
2. Its pinyin
3. A short English explanation

Format:
Idiom
Pinyin
Explanation

Situation: {situation}
Answer:
"""
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    generated_text = response.choices[0].message.content.strip()

    lines = [line.strip() for line in generated_text.split("\n") if line.strip()]
    if len(lines) >= 3:
        idiom = lines[0]
        pinyin = lines[1]
        meaning = " ".join(lines[2:])
        explanation = f"{pinyin}<br><br>{meaning}"
    else:
        idiom = generated_text
        explanation = ""
    return idiom, explanation

# ======================
# UI logic
# ======================
def update_ui(situation):
    if USE_MOCK:
        idiom, explanation = generate_idiom_mock(situation)
    else:
        idiom, explanation = generate_idiom(situation, client)
    return f"<div class='idiom-output'>{idiom}</div>", f"<div class='explanation-output'>{explanation}</div>"

def launch_app():
    with gr.Blocks(css="style.css") as demo:
        gr.Markdown("## 🀄 Chinese Wisdom Generator\nEnter a situation, get a Chinese idiom with explanation.")
        with gr.Row():
            with gr.Column(scale=1):
                situation = gr.Textbox(
                    label="Describe your situation...",
                    placeholder="e.g. I procrastinated on my homework again...",
                    lines=3
                )
                submit_btn = gr.Button("✨ Find Idiom")
                gr.Examples(
                    examples=[
                        ["I studied hard but still failed my exam."],
                        ["I missed my bus because I woke up late."],
                        ["I finally finished a long project after months."],
                    ],
                    inputs=[situation]
                )
            with gr.Column(scale=1):
                idiom_output = gr.HTML("<div class='idiom-output'>—</div>")
                explanation_output = gr.HTML("<div class='explanation-output'>—</div>")

        submit_btn.click(update_ui, inputs=[situation], outputs=[idiom_output, explanation_output])
    demo.launch(debug=True)

if __name__ == "__main__":
    launch_app()
