# 🤖 Fake Bot Detector

An AI-powered text detection system built with React and FastAPI. Rough.js is used for the sketchy, hand-drawn style UI elements. I built this project for learning purposes and to add to my portfolio.

![AI Text Detector](https://img.shields.io/badge/AI-Text%20Detector-blue)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![React](https://img.shields.io/badge/react-18.2+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)

## 🛠️ Technologies

- **React.js** - Frontend framework
- **FastAPI** - Backend framework
- **Tailwind CSS** - Styling
- **NumPy** - Numerical computing
- **Lucide React** - Icons

## ✨ Features

Here's what you can do with AI Text Detector:

- **Detect AI vs Human Text**: Analyzes text to determine if it's AI-generated or human-written with confidence scores.
- **Feature Analysis**: Shows detailed linguistic features like word count, lexical diversity, and sentence structure.
- **Real-time Detection**: Get instant results as you type or paste text.
- **Explainable Results**: Provides clear explanations of why text is classified as AI or human.
- **Minimum 20 Words**: Works best with texts containing 50+ words for accurate detection.

## 📸 Screenshots

<img width="1470" height="956" alt="Screenshot 2026-01-15 at 2 02 34 AM" src="https://github.com/user-attachments/assets/7ab52a83-59be-44f5-b261-36d67340b707" />


## 🚀 The Process

I started by building the backend API with FastAPI to handle all the text analysis. Then, I focused on creating the frontend with React, making sure the user experience was smooth and intuitive.

Next, I implemented the detection algorithm using weighted linguistic features. This was important for getting accurate results. After that, I added detailed explanations to help users understand the detection results.

To make sure everything worked correctly, I tested with various text samples - both AI-generated and human-written. I also added input validation and error handling for better reliability.

Finally, I added responsive design with Tailwind CSS and created comprehensive documentation. With everything functioning, I deployed the application and documented the entire process.

## 🎓 What I Learned

During this project, I've picked up important skills and a better understanding of complex ideas, which improved my development abilities.

### 💡 Pattern Recognition:

- **Linguistic Analysis**: Creating the detection algorithm taught me to analyze text patterns, including lexical diversity and sentence structure variance.
- **Feature Engineering**: I had to identify which features best distinguish AI from human writing and weight them appropriately.

### 🔗 API Development:

- **RESTful Design**: Built a clean API with proper endpoints, request validation, and error handling using FastAPI.
- **CORS Configuration**: Learned about cross-origin resource sharing and how to configure it for frontend-backend communication.

### ⚛️ React Development:

- **State Management**: Working with React hooks like useState to manage application state effectively.
- **Component Design**: Created reusable components with proper props and event handling.

### 🎨 UI/UX Design:

- **Tailwind CSS**: Mastered utility-first CSS for rapid, responsive design implementation.
- **User Feedback**: Implemented loading states, error messages, and clear visual feedback for better UX.

### 📊 Data Processing:

- **NumPy Operations**: Used numerical computing for statistical analysis of text features.
- **Algorithm Optimization**: Balanced accuracy with performance for real-time text analysis.

### 🔧 Overall Growth:

Each part of this project helped me understand more about building full-stack applications, handling complex data, and creating user-friendly interfaces. It was more than just making a tool - it was about solving problems, learning new technologies, and improving my skills for future projects.

## 💡 How can it be improved?

- Add support for multiple languages beyond English
- Implement batch processing for analyzing multiple texts
- Add user authentication and analysis history
- Integrate advanced ML models like BERT or GPT-detector
- Create a browser extension for on-the-fly detection
- Add more detailed statistics and visualizations
- Implement API rate limiting and caching
- Support for file uploads (PDF, DOCX)

## 🏃 Running the Project

To run the project in your local environment, follow these steps:

1. Clone the repository to your local machine.
2. Run `cd backend && python -m venv venv` to create a virtual environment.
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Run `pip install -r requirements.txt` to install backend dependencies.
5. Run `python main.py` to start the backend server (runs on port 8000).
6. Open a new terminal and run `cd frontend && npm install` to install frontend dependencies.
7. Run `npm start` to start the development server (runs on port 3000).
8. Open [http://localhost:3000](http://localhost:3000) (or the address shown in your console) in your web browser to view the app.

📹 Video

https://github.com/user-attachments/assets/fa68e4e4-a2be-4c6d-8708-dd1008b34a37


## 🔗 Links

- **Live Demo**: [Add your deployed link here]
- **API Documentation**: Available at `/docs` endpoint when backend is running

---

**Note**: This project requires texts with at least 20 words (50+ recommended) for reliable detection. Short phrases and generic text may not be accurately classified.
