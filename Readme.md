# 🤖 Job-Pilot

**Job-Pilot** is an AI-powered agent that automatically fills job application forms by intelligently parsing resumes and job application PDFs. It leverages vector databases, embeddings, and language models to extract, reason, and generate appropriate answers to job-related questions.

## 🚀 Features

- 📄 Resume and PDF parsing
- 🤖 AI-powered form filling
- 🎯 Intelligent answer generation
- 🔊 Audio transcription support
- 🖥️ User-friendly Gradio interface

## 🛠️ Tech Stack

- Python 3.11+
- LlamaIndex for document processing
- HuggingFace embeddings
- AssemblyAI for audio processing
- Gradio for the web interface

## 📦 Installation

1. Clone the repository
2. Install Poetry (dependency management tool)
3. Install dependencies:
   ```bash
   poetry install
   ```
4. Copy `.env.example` to `.env` and fill in your API keys

## 🚀 Usage

1. Activate the virtual environment:
   ```bash
   poetry shell
   ```
2. Place your resume and job application PDFs in the `data` directory
3. Run the application (check Makefile for available commands)

## 📁 Project Structure

- `src/`: Source code
- `data/`: Input documents
- `notebooks/`: Jupyter notebooks for development
- `storage/`: Vector store and embeddings

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 🚧 Status

- 📦 In Development
