import os

import gradio as gr
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv
from opencc import OpenCC

from utils.utils import get_pinyin
from verification.verifier import verify_idiom_exists

# ======================
# Config
# ======================
load_dotenv()

MODEL = "gpt-oss-120b"
USE_MOCK = False  # ✅ Toggle between mock and real API

# simplified to traditional Chinese character converter
char_converter = OpenCC('s2t')

# ======================
# Instantiate client (if not mocking)
# ======================
CLIENT = None
if not USE_MOCK:
    CLIENT = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))


# ======================
# Mock function for UI testing
# ======================
def find_idiom_mock():
    idiom = "对症下药"
    trad_idiom = char_converter.convert(idiom)
    explanation = """duì zhèng xià yào<br><br>
    To prescribe the right medicine; to take the right approach to a problem."""
    idiom_output = f"{idiom}<br>{trad_idiom}"
    return idiom_output, explanation


# ======================
# Real API function
# ======================

# Global cache for repeated situations
EXAMPLE_CACHE = {}


def find_idiom(situation: str, max_attempts: int = 3):
    """
    Find a verified Chinese idiom for a given situation.

    Uses verify_idiom_exists() to confirm idiom validity.
    """
    if situation in EXAMPLE_CACHE:
        return EXAMPLE_CACHE[situation]

    for attempt in range(1, max_attempts + 1):
        prompt = f"""You are a wise assistant. Given a situation, respond with exactly:
1. A Chinese idiom (includes 成語、俗語、諺語), 
   written in simplified Chinese characters,
   that conveys the idea of the given situation.
2. Its literal English translationx
3. Explain idiom in English. Keep explanation to 2-3 concise sentences.

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

        generated_text = response.choices[0].message.content.strip()
        lines = [line.strip() for line in generated_text.split("\n") if line.strip()]

        llm_idiom = lines[0] if lines else generated_text
        trad_idiom = char_converter.convert(llm_idiom) if char_converter else None

        # 2️⃣ Verify idiom using CC-CEDICT + Wiktionary
        if verify_idiom_exists(llm_idiom):
            pinyin_text = get_pinyin(llm_idiom)

            if len(lines) >= 3:
                translation = lines[1]
                meaning = " ".join(lines[2:])
            else:
                translation = ""
                meaning = " ".join(lines[1:])

            explanation = f"""
                <div style="line-height: 1.6;">
                    <p style="margin: 0;">
                        {pinyin_text}
                    </p>
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 8px 0;">
                    <p style="margin: 0;">
                        <i>{translation}</i><br>
                        {meaning}
                    </p>
                </div>
            """
            EXAMPLE_CACHE[situation] = (llm_idiom, explanation)
            idiom_output = f"{llm_idiom}<br>{trad_idiom}"
            return idiom_output, explanation
        else:
            print(f"Attempt {attempt}: '{idiom_output}' failed verification, retrying...")

    # Fallback if no verified idiom found
    fallback_idiom = "未找到成语"
    fallback_explanation = "No verified idiom found for this situation."
    return fallback_idiom, fallback_explanation

# ======================
# UI Wrapper
# ======================
def update_ui(situation):
    if USE_MOCK:
        idiom, explanation = find_idiom_mock()
    else:
        idiom, explanation = find_idiom(situation)

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
            inputs=[situation],
            outputs=[idiom_output, explanation_output],
        )


    demo.launch()


if __name__ == "__main__":
    launch_app()
