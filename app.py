import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

MODEL_ID = "bigscience/bloom-560m"

# load once globally
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    device_map="auto",   # GPU if available, otherwise CPU
    trust_remote_code=True
)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=200,
    temperature=0.7
)

def generate_idiom(situation: str):
    prompt = f"""You are a wise assistant. Given a situation, respond with exactly:
1. A single Chinese idiom (成语).
2. Its pinyin.
3. A short English explanation.

Format:
Idiom
Pinyin
Explanation

Situation: {situation}
Answer:
"""
    response = pipe(prompt)[0]["generated_text"]
    clean_response = response.split("Answer:")[-1].strip()

    # Try to split into lines
    lines = [line.strip() for line in clean_response.split("\n") if line.strip()]
    if len(lines) >= 3:
        idiom = lines[0]
        pinyin = lines[1]
        meaning = " ".join(lines[2:])
        explanation = f"{pinyin}\n\n{meaning}"
    else:
        # fallback if formatting is off
        idiom = clean_response
        explanation = ""

    return idiom, explanation


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

    def update_ui(situation):
        idiom, explanation = generate_idiom(situation)
        return f"<div class='idiom-output'>{idiom}</div>", f"<div class='explanation-output'>{explanation}</div>"

    submit_btn.click(update_ui, inputs=[situation], outputs=[idiom_output, explanation_output])


if __name__ == "__main__":
    demo.launch()
