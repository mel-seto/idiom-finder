import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

pipe = pipeline(task="text-generation", model="bigscience/bloomz-560m")
    
def generate_idiom(situation):
    response = pipe(f"Give me a Chinese idiom for this: {situation}.")
    print(response)
    pinyin = ""
    meaning = ""
    return response, f"{pinyin}\n\n{meaning}"

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