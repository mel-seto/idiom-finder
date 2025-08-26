# app.py
import os
from dotenv import load_dotenv
import gradio as gr
from huggingface_hub import InferenceClient

load_dotenv()

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
    # Use Cerebras chat completions API
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )

    # Extract generated text
    generated_text = response.choices[0].message.content.strip()

    # Split lines for UI
    lines = [line.strip() for line in generated_text.split("\n") if line.strip()]
    if len(lines) >= 3:
        idiom = lines[0]
        pinyin = lines[1]
        meaning = " ".join(lines[2:])
        explanation = f"{pinyin}\n\n{meaning}"
    else:
        idiom = generated_text
        explanation = ""

    return idiom, explanation

def launch_app():
    client = InferenceClient(
        provider="cerebras",
        api_key=os.environ["HF_TOKEN"]
    )

    with gr.Blocks() as demo:
        txt = gr.Textbox(label="Situation", lines=3)
        idiom_out = gr.HTML()
        expl_out = gr.HTML()
        btn = gr.Button("✨ Find Idiom")

        def update_ui(s):
            return generate_idiom(s, client)

        btn.click(update_ui, inputs=[txt], outputs=[idiom_out, expl_out])

    demo.launch(debug=True)
