import gradio as gr

with gr.Blocks() as app:
  input_file = gr.File(label="Upload CSV file", file_count='single', type='filepath')
  input_query = gr.Textbox(label="Query", lines=5, placeholder="Enter a query")
  submit_button = gr.Button("Submit")
  output_response = gr.Textbox(label="Response", lines=5, placeholder="Response will appear here")
  pdf_file = gr.File(label="Download PDF")

app.launch(debug=True)

