import json
import os

import gradio as gr
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv

from retrieval.retriever import retrieve_idiom
from utils.utils import get_pinyin

# ======================
# Config
# ======================
load_dotenv()

MODEL = "gpt-oss-120b"
USE_MOCK = False  # ✅ Toggle between mock and real API

# ======================
# Idiom dataset
# ======================
IDIOM_FILE_PATH = "idiom_dataset/chid_idiom_reference.json"
with open(IDIOM_FILE_PATH, "r", encoding="utf-8") as f:
    idiom_list = json.load(f)
VALID_IDIOMS = set(idiom_list)

# ======================
# Instantiate client (if not mocking)
# ======================
CLIENT = None
if not USE_MOCK:
    CLIENT = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))


# ======================
# Mock function for UI testing
# ======================
def generate_idiom_mock():
    idiom = "对症下药"
    explanation = """duì zhèng xià yào<br><br>
    To prescribe the right medicine; to take the right approach to a problem."""
    return idiom, explanation


# ======================
# Real API function
# ======================


def generate_idiom(situation: str):
    prompt = f"""You are a wise assistant. Given a situation, respond with exactly:
1. A Chinese idiom (includes 成語、俗語、諺語), 
   written in simplified Chinese characters,
   that conveys the idea of the given situation.
2. Its literal English translation
3. Explain idiom. Keep explanation to 2-3 concise sentences.

Format:
Idiom
Literal translation
Explanation

Situation: {situation}
Answer:"""

    response = CLIENT.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    print(response)

    generated_text = response.choices[0].message.content.strip()
    lines = [line.strip() for line in generated_text.split("\n") if line.strip()]

    llm_idiom = lines[0] if lines else generated_text

    if llm_idiom not in VALID_IDIOMS:
        explanation = "The LLM generated an invalid idiom. Try again!"
        return llm_idiom, explanation

    pinyin_text = get_pinyin(llm_idiom)

    if len(lines) >= 3:
        translation = lines[1]
        meaning = " ".join(lines[2:])
        explanation = f"{pinyin_text}<br><br>{translation}<br><br>{meaning}"
    else:
        explanation = f"{pinyin_text}<br><br>{' '.join(lines[1:])}"

    return llm_idiom, explanation


# ======================
# UI Wrapper
# ======================
def update_ui(situation, mode):
    if mode == "LLM":
        if USE_MOCK:
            idiom, explanation = generate_idiom_mock()
        else:
            idiom, explanation = generate_idiom(situation)
    elif mode == "RAG":
        top_idioms = retrieve_idiom(situation, top_k=3)
        formatted_idioms = []
        for idiom_entry in top_idioms:
            # Split "<Chinese>: <English>" format
            if ": " in idiom_entry:
                chinese, english = idiom_entry.split(": ", 1)
            else:
                chinese, english = idiom_entry, ""
            pinyin_text = get_pinyin(chinese)
            formatted_idioms.append(f"<div class='idiom-entry'><b>{chinese}</b><br>{pinyin_text}<br>{english}</div>")

        # Combine all entries with horizontal separators
        idiom = "<hr>".join(formatted_idioms)
        explanation = "Retrieved using embeddings (RAG)."
    else:
        idiom = "Unknown mode"
        explanation = ""

    return (
        f"<div class='idiom-output'>{idiom}</div>",
        f"<div class='explanation-output'>{explanation}</div>",
    )


# ======================
# Launch app
# ======================
def launch_app():
    
    with gr.Blocks(css="style.css") as demo:
        gr.Markdown("# 🎋 Chinese Idiom Finder")
        with gr.Row():
            with gr.Column():
                situation = gr.Textbox(
                    label="Enter a situation",
                    lines=2,
                    placeholder="e.g., When facing a big challenge",
                )
                mode_dropdown = gr.Dropdown(
                    ["LLM", "RAG"],
                    label="Mode",
                    value="LLM",
                )
                generate_btn = gr.Button("✨ Find Idiom")

                # ✅ Example situations
                gr.Examples(
                    examples=[
                        ["When facing a big challenge"],
                        ["When someone helps you in a time of need"],
                        ["When you need to stay calm under pressure"],
                        ["When teamwork is important to succeed"],
                        ["When rushing leads to mistakes"],
                    ],
                    inputs=situation,
                )

            with gr.Column():
                idiom_output = gr.HTML(label="Idiom")
                explanation_output = gr.HTML(label="Explanation")

        # pylint: disable=no-member
        generate_btn.click(
            fn=update_ui,
            inputs=[situation, mode_dropdown],
            outputs=[idiom_output, explanation_output],
        )


    demo.launch()


if __name__ == "__main__":
    launch_app()
