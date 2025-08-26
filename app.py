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
    # Use Cerebras chat completion API
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )

    generated_text = response.choices[0].message.content.strip()

    # Split lines for clean UI
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
    # Instantiate Cerebras client inside the function
    client = InferenceClient(
        provider="cerebras",
        model="meta-llama/Llama-3.3-70B-Instruct",
        api_key=os.environ["HF_TOKEN"]
    )

    with gr.Blocks(css="""
        .idiom-output {
            font-size: 2rem;
            font-weight: bold;
            text-align: center;
            color: #8B0000;
            margin-bottom: 0.5em;
        }
        .explanation-output {
            font-size: 1rem;
            line-height: 1.5;
            color: #333333;
            text-align: center;
        }
        .gradio-container {
            background-color: #fdfcf7;
        }
    """) as demo:

        gr.Markdown("## 🀄 Chinese Wisdom Generator\nEnter a situation, get a Chinese idiom with explanation.")

        with gr.Row():
            # Left column: input + examples + button
            with gr.Column(scale=1):
                situation_input = gr.Textbox(
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
                    inputs=[situation_input]
                )

            # Right column: outputs
            with gr.Column(scale=1):
                idiom_output = gr.HTML("<div class='idiom-output'>—</div>")
                explanation_output = gr.HTML("<div class='explanation-output'>—</div>")

        # Button callback directly calls generate_idiom
        def update_ui(situation):
            idiom, explanation = generate_idiom(situation, client)
            return f"<div class='idiom-output'>{idiom}</div>", f"<div class='explanation-output'>{explanation}</div>"

        submit_btn.click(update_ui, inputs=[situation_input], outputs=[idiom_output, explanation_output])

    demo.launch(debug=True)


if __name__ == "__main__":
    launch_app()
