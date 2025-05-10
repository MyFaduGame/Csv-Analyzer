# 🤖 CSV Analyzer Chatbot

This project is a web-based AI assistant that analyzes uploaded CSV files, generates visual insights, and allows you to ask questions about your data using natural language. It combines **FastAPI**, **OpenAI GPT-4o**, **Pandas**, **Matplotlib**, and **Seaborn** to provide an interactive chatbot experience tailored to CSV datasets.

---

## 🚀 Features

- 📤 Upload CSV files for instant analysis
- 📊 Auto-generated data visualizations (histograms and pie charts)
- 🧠 Natural language Q&A about your dataset using OpenAI's GPT-4o
- 💬 Chat-like UI with Markdown rendering and typing indicators
- 🔒 Local and customizable API integration (no data sent to third-party dashboards)

---

## 📦 Tech Stack

- **Frontend**: HTML, JavaScript (vanilla), CSS
- **Backend**: FastAPI, Uvicorn
- **AI**: OpenAI GPT-4o via `openai` API
- **Visualization**: Matplotlib, Seaborn
- **Data Handling**: Pandas

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/csv-analyzer-chatbot.git
cd csv-analyzer-chatbot
````

### 2. Create and Activate Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

<details>
<summary><strong>requirements.txt</strong> (if you need it)</summary>

```
fastapi
uvicorn
pandas
matplotlib
seaborn
python-multipart
requests
openai
```

</details>

### 4. Set Your OpenAI API Key

Edit the `main.py` file and set your OpenAI API key:

```python
OPENAI_API_KEY = "your-openai-api-key"
```

> ⚠️ Do not share your API key publicly!

---

## ▶️ Running the App

```bash
python main.py
```

This will start the FastAPI server at `http://localhost:8000`.

Then, open the `index.html` file in your browser to use the chatbot interface.

---

## 🖼️ Project Structure

```
csv-analyzer-chatbot/
│
├── main.py               # FastAPI backend
├── index.html            # Frontend chatbot UI
├── uploads/              # Uploaded CSV files (auto-created)
├── graphs/               # Saved chart images (auto-created)
├── requirements.txt      # Dependencies
└── README.md             # Project overview
```

---

## 📌 Notes

* Images and CSVs are saved locally in `graphs/` and `uploads/`.
* Graphs include:

  * Histogram (for numeric columns)
  * Pie chart (for categorical columns with ≤ 10 unique values)

---

## 🧩 To-Do / Ideas

* Support time-series line plots
* Add CSV download of AI-generated summary
* Deploy to cloud (e.g., Vercel frontend + Render backend)

---

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## 👨‍💻 Author

Made with 💡 by MyFaduGame(https://github.com/MyFaduGame)



