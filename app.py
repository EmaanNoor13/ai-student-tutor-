import gradio as gr
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_content(topic, difficulty, content_type):
    if not topic.strip():
        return "⚠️ Please enter a topic first!"

    if content_type == "Full Lesson (Explain + Quiz)":
        prompt = f"You are a student tutor. Explain '{topic}' for a {difficulty} level student. Include: simple explanation, 3 key points, a real life example, and 3 MCQ quiz questions with answers."
    elif content_type == "Explanation Only":
        prompt = f"You are a student tutor. Explain '{topic}' for a {difficulty} level student with 3 key points and a real life example."
    else:
        prompt = f"You are a student tutor. Generate 5 MCQ quiz questions about '{topic}' for a {difficulty} level student. Include 4 options and the correct answer for each."

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"


with gr.Blocks() as demo:
    gr.Markdown("""
    # 🎓 AI Student Tutor
    ### Generate lessons, explanations & quizzes on any topic instantly!
    Powered by **Llama 3** via Groq
    """)

    with gr.Row():
        with gr.Column(scale=1):
            topic_input = gr.Textbox(
                label="📚 Enter Topic",
                placeholder="e.g. Photosynthesis, World War 2...",
                lines=2
            )
            difficulty = gr.Radio(
                choices=["Beginner", "Intermediate", "Advanced"],
                value="Beginner",
                label="🎯 Difficulty Level"
            )
            content_type = gr.Radio(
                choices=["Full Lesson (Explain + Quiz)", "Explanation Only", "Quiz Only"],
                value="Full Lesson (Explain + Quiz)",
                label="📝 What do you want?"
            )
            generate_btn = gr.Button("✨ Generate", variant="primary")

        with gr.Column(scale=2):
            output = gr.Textbox(
                label="📖 AI Tutor Response",
                lines=20
            )

    gr.Examples(
        examples=[
            ["Photosynthesis", "Beginner", "Full Lesson (Explain + Quiz)"],
            ["Newton's Laws", "Intermediate", "Explanation Only"],
            ["Python Loops", "Beginner", "Quiz Only"],
        ],
        inputs=[topic_input, difficulty, content_type],
        label="💡 Try these examples"
    )

    generate_btn.click(
        fn=generate_content,
        inputs=[topic_input, difficulty, content_type],
        outputs=output
    )

demo.launch()
