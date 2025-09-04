import gradio as gr
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# ======================
# Config
# ======================
load_dotenv()

MODEL = "meta-llama/Llama-3.3-70B-Instruct"
USE_MOCK = False  # ✅ Toggle between mock and real API

# ======================
# Instantiate client (if not mocking)
# ======================
client = None
if not USE_MOCK:
    client = InferenceClient(
        provider="cerebras",
        model=MODEL,
        api_key=os.environ["HF_TOKEN"]
    )

# ======================
# Mock function for UI testing
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
1. A traditional Chinese idiom (which includes 成語、俗語、諺語)， that conveys the idea of the given situation. 
2. Its pinyin
3. Its literal English translation
4. Explain idiom. Keep explanation to 2-3 concise sentences.

Format:
Idiom
Pinyin
Literal translation
Explanation

Situation: {situation}
Answer:
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )

    generated_text = response.choices[0].message.content.strip()
    lines = [line.strip() for line in generated_text.split("\n") if line.strip()]

    if len(lines) >= 3:
        idiom = lines[0]
        pinyin = lines[1]
        translation = lines[2]
        meaning = " ".join(lines[3:])
        explanation = f"{pinyin}<br><br>{translation}<br><br>{meaning}"
    else:
        idiom = generated_text
        explanation = ""

    return idiom, explanation

# ======================
# UI Wrapper
# ======================
def update_ui(situation):
    if USE_MOCK:
        idiom, explanation = generate_idiom_mock(situation)
    else:
        idiom, explanation = generate_idiom(situation, client)

    return (
        f"<div class='idiom-output'>{idiom}</div>",
        f"<div class='explanation-output'>{explanation}</div>"
    )

# ======================
# Launch app
# ======================
def launch_app():
    with gr.Blocks(css="style.css") as demo:
        gr.Markdown("# 🎋 Chinese Idioms Finder")

        with gr.Row():
            with gr.Column():
                situation = gr.Textbox(
                    label="Enter a situation",
                    lines=2,
                    placeholder="e.g., When facing a big challenge"
                )
                generate_btn = gr.Button("✨ Find Idiom")

                # ✅ Example situations
                gr.Examples(
                    examples=[
                        ["When facing a big challenge"],
                        ["When someone helps you in a time of need"],
                        ["When you need to stay calm under pressure"],
                        ["When teamwork is important to succeed"],
                        ["When rushing leads to mistakes"]
                    ],
                    inputs=situation
                )

            with gr.Column():
                idiom_output = gr.HTML(label="Idiom")
                explanation_output = gr.HTML(label="Explanation")

        generate_btn.click(
            fn=update_ui,
            inputs=situation,
            outputs=[idiom_output, explanation_output]
        )

    demo.launch()

if __name__ == "__main__":
    launch_app()
