// Archivo script.js
const questions = [
    {
        sentence: "I ___ to the park every morning.",
        options: ["go", "went", "going", "goes"],
        correct: "go"
    },
    {
        sentence: "She ___ playing soccer yesterday.",
        options: ["is", "are", "was", "were"],
        correct: "was"
    },
    {
        sentence: "We ___ dinner at 7 PM last night.",
        options: ["have", "had", "having", "has"],
        correct: "had"
    },
    {
        sentence: "They ___ swimming every weekend.",
        options: ["enjoy", "enjoys", "enjoyed", "enjoying"],
        correct: "enjoy"
    },
    {
        sentence: "He ___ his homework before the deadline.",
        options: ["do", "did", "does", "doing"],
        correct: "did"
    }
];

let currentQuestionIndex = 0;
let score = 0;

function showQuestion() {
    const question = questions[currentQuestionIndex];
    document.getElementById("question").innerText = question.sentence;
    
    const optionsContainer = document.getElementById("options");
    optionsContainer.innerHTML = "";

    question.options.forEach(option => {
        const btn = document.createElement("button");
        btn.innerText = option;
        btn.onclick = () => checkAnswer(option);
        optionsContainer.appendChild(btn);
    });

    document.getElementById("result").innerText = "";
    document.getElementById("next-btn").disabled = true;
}

function checkAnswer(selectedOption) {
    const question = questions[currentQuestionIndex];
    if (selectedOption === question.correct) {
        document.getElementById("result").innerText = "✅ correcto!";
        score++;
    } else {
        document.getElementById("result").innerText = `❌ incorrecto! la respuesta correcta es "${question.correct}".`;
    }

    document.querySelectorAll("#options button").forEach(button => {
        button.disabled = true;
        if (button.innerText === question.correct) {
            button.style.backgroundColor = "#4CAF50";
        } else {
            button.style.backgroundColor = "#f44336";
        }
    });

    document.getElementById("next-btn").disabled = false;
    document.getElementById("score").innerText = `puntos: ${score} / ${questions.length}`;
}

function nextQuestion() {
    currentQuestionIndex++;
    if (currentQuestionIndex < questions.length) {
        showQuestion();
    } else {
        document.getElementById("question").innerText = "Test completo!";
        document.getElementById("options").innerHTML = "";
        document.getElementById("next-btn").style.display = "none";
        document.getElementById("result").innerText = `tu puntaje fue ${score} / ${questions.length}.`;
    }
}

window.onload = showQuestion;