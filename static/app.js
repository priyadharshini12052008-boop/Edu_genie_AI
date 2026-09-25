const task = document.getElementById("task");
const inputText = document.getElementById("inputText");
const submitBtn = document.getElementById("submitBtn");
const sampleBtn = document.getElementById("sampleBtn");
const statusBox = document.getElementById("status");
const resultBox = document.getElementById("result");

let quizQuestions = [];

const samples = {
    qa: "Which is the largest ocean?",
    explain: "Explain the Pythagoras theorem to a beginner.",
    quiz: "The water cycle describes the continuous movement of water between the Earth's surface, atmosphere, and underground. Evaporation changes liquid water into water vapor. Condensation forms clouds, and precipitation returns water to Earth.",
    summarize: "Artificial intelligence is a field of computer science concerned with creating systems that can perform tasks that normally require human intelligence. These tasks include learning, reasoning, language understanding, perception, and decision-making.",
    learn: "SQL"
};

task.addEventListener("change", () => {
    inputText.placeholder = {
        qa: "Example: Which is the largest ocean?",
        explain: "Example: Explain the Pythagoras theorem to a beginner.",
        quiz: "Paste a paragraph or topic here to generate a quiz.",
        summarize: "Paste a long educational passage here.",
        learn: "Example: SQL"
    }[task.value];
});

sampleBtn.addEventListener("click", () => {
    inputText.value = samples[task.value];
});

submitBtn.addEventListener("click", submitTask);

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function renderText(text) {
    const safe = escapeHtml(text);
    return safe
        .replace(/\n\n+/g, "</p><p>")
        .replace(/\n/g, "<br>");
}

function renderQuiz(questions) {
    return `
        <h3>Generated Quiz</h3>
        <div id="quiz-container">
            ${questions.map((item, index) => `
                <div class="quiz-question" data-question-index="${index}">
                    <strong>${index + 1}. ${escapeHtml(item.question)}</strong>

                    <div class="quiz-options">
                        ${item.options.map((option, optionIndex) => `
                            <label class="quiz-option">
                                <input
                                    type="radio"
                                    name="question-${index}"
                                    value="${escapeHtml(option)}"
                                >
                                <span>${escapeHtml(option)}</span>
                            </label>
                        `).join("")}
                    </div>

                    <button
                        type="button"
                        class="check-answer-btn"
                        onclick="checkQuizAnswer(${index})"
                    >
                        Check Answer
                    </button>

                    <div
                        id="quiz-feedback-${index}"
                        class="quiz-feedback"
                    ></div>

                    <div
                        id="quiz-explanation-${index}"
                        class="quiz-explanation hidden"
                    ></div>
                </div>
            `).join("")}
        </div>
    `;
}

async function submitTask() {
    const text = inputText.value.trim();

    if (!text) {
        statusBox.textContent = "Please enter something first.";
        return;
    }

    const endpointMap = {
        qa: "/qa",
        explain: "/explain",
        quiz: "/quiz",
        summarize: "/summarize",
        learn: "/learn/recommendations"
    };

    const endpoint = endpointMap[task.value];

    submitBtn.disabled = true;
    statusBox.textContent = "EduGenie is thinking...";
    resultBox.classList.add("hidden");
    resultBox.innerHTML = "";

    try {
        const body = task.value === "quiz"
            ? { text, count: 3 }
            : { text };

        const response = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.result || "Something went wrong.");
        }
        if (Array.isArray(data.result)) {
            quizQuestions = data.result;
            resultBox.innerHTML = renderQuiz(data.result);
        } else {
             resultBox.innerHTML = `<p>${renderText(data.result)}</p>`;
        }

        resultBox.classList.remove("hidden");
        statusBox.textContent = "Done!";
    } catch (error) {
        resultBox.innerHTML = `<p><strong>Error:</strong> ${escapeHtml(error.message)}</p>`;
        resultBox.classList.remove("hidden");
        statusBox.textContent = "Request failed.";
    } finally {
        submitBtn.disabled = false;
    }
}
function checkQuizAnswer(questionIndex) {
    const questionBox = document.querySelector(
        `[data-question-index="${questionIndex}"]`
    );

    const selectedOption = questionBox.querySelector(
        `input[name="question-${questionIndex}"]:checked`
    );

    const feedbackBox = document.getElementById(
        `quiz-feedback-${questionIndex}`
    );

    const explanationBox = document.getElementById(
        `quiz-explanation-${questionIndex}`
    );

    if (!selectedOption) {
        feedbackBox.innerHTML = "<strong>Please select an answer.</strong>";
        return;
    }

    const selectedAnswer = selectedOption.value;

    // Get the correct answer from the quiz data stored on the page
    const correctAnswer = quizQuestions[questionIndex].correct_answer;
    const explanation = quizQuestions[questionIndex].explanation;

    if (selectedAnswer === correctAnswer) {
        feedbackBox.innerHTML = "✅ <strong>Correct!</strong>";
    } else {
        feedbackBox.innerHTML =
            `❌ <strong>Wrong.</strong> The correct answer is: ` +
            `<strong>${escapeHtml(correctAnswer)}</strong>`;
    }

    explanationBox.innerHTML =
        `<strong>Explanation:</strong> ${escapeHtml(explanation || "")}`;

    explanationBox.classList.remove("hidden");
}