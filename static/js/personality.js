// Personality Assessment and Learning Path Recommendation System

class PersonalityAssessment {
    constructor() {
        this.currentQuestionIndex = 0;
        this.answers = {};
        this.personalityScores = {
            analytical: 0,
            creative: 0,
            practical: 0,
            collaborative: 0
        };
        
        this.questions = [
            {
                id: 1,
                question: "When approaching a new coding problem, what's your first instinct?",
                options: [
                    { text: "Break it down into smaller, logical components", type: "analytical", weight: 3 },
                    { text: "Think of creative, innovative solutions", type: "creative", weight: 3 },
                    { text: "Look for proven patterns and best practices", type: "practical", weight: 3 },
                    { text: "Discuss it with others to get different perspectives", type: "collaborative", weight: 3 }
                ]
            },
            {
                id: 2,
                question: "What motivates you most when learning to code?",
                options: [
                    { text: "Understanding how things work under the hood", type: "analytical", weight: 2 },
                    { text: "Building something unique and original", type: "creative", weight: 2 },
                    { text: "Solving real-world problems efficiently", type: "practical", weight: 2 },
                    { text: "Working on projects with a team", type: "collaborative", weight: 2 }
                ]
            },
            {
                id: 3,
                question: "How do you prefer to learn new programming concepts?",
                options: [
                    { text: "Reading documentation and technical resources", type: "analytical", weight: 2 },
                    { text: "Experimenting and building personal projects", type: "creative", weight: 2 },
                    { text: "Following structured tutorials and courses", type: "practical", weight: 2 },
                    { text: "Pair programming or study groups", type: "collaborative", weight: 2 }
                ]
            },
            {
                id: 4,
                question: "When debugging code, what's your typical approach?",
                options: [
                    { text: "Systematically trace through the logic step by step", type: "analytical", weight: 3 },
                    { text: "Try different approaches until something works", type: "creative", weight: 3 },
                    { text: "Use proven debugging tools and techniques", type: "practical", weight: 3 },
                    { text: "Ask for help or rubber duck with someone", type: "collaborative", weight: 3 }
                ]
            },
            {
                id: 5,
                question: "What type of coding projects excite you most?",
                options: [
                    { text: "Algorithms and data structure challenges", type: "analytical", weight: 2 },
                    { text: "Creative applications like games or art", type: "creative", weight: 2 },
                    { text: "Business applications and productivity tools", type: "practical", weight: 2 },
                    { text: "Open source contributions and community projects", type: "collaborative", weight: 2 }
                ]
            },
            {
                id: 6,
                question: "How do you handle learning new frameworks or technologies?",
                options: [
                    { text: "Study the architecture and design principles first", type: "analytical", weight: 2 },
                    { text: "Jump in and start building something interesting", type: "creative", weight: 2 },
                    { text: "Follow official guides and best practice examples", type: "practical", weight: 2 },
                    { text: "Join communities and learn from others' experiences", type: "collaborative", weight: 2 }
                ]
            },
            {
                id: 7,
                question: "What's your ideal coding environment?",
                options: [
                    { text: "Quiet space with minimal distractions for deep focus", type: "analytical", weight: 1 },
                    { text: "Inspiring environment that sparks creativity", type: "creative", weight: 1 },
                    { text: "Well-organized setup with all necessary tools", type: "practical", weight: 1 },
                    { text: "Collaborative space where I can interact with others", type: "collaborative", weight: 1 }
                ]
            },
            {
                id: 8,
                question: "When reviewing others' code, what do you focus on most?",
                options: [
                    { text: "Logic correctness and algorithmic efficiency", type: "analytical", weight: 2 },
                    { text: "Innovative approaches and creative solutions", type: "creative", weight: 2 },
                    { text: "Code quality, maintainability, and standards", type: "practical", weight: 2 },
                    { text: "Providing constructive feedback and learning from it", type: "collaborative", weight: 2 }
                ]
            }
        ];

        this.learningPaths = {
            analytical: {
                type: "The Analytical Thinker",
                description: "You excel at breaking down complex problems and understanding systems deeply. You thrive on logic, algorithms, and structured thinking.",
                icon: "🧠",
                paths: [
                    {
                        title: "Algorithm & Data Structures Mastery",
                        description: "Deep dive into computational thinking, algorithm design, and optimization techniques.",
                        skills: ["Algorithms", "Data Structures", "Big O Analysis", "Problem Solving"],
                        duration: "8-12 weeks",
                        difficulty: "Intermediate to Advanced"
                    },
                    {
                        title: "Systems Programming",
                        description: "Learn low-level programming, operating systems, and computer architecture.",
                        skills: ["C/C++", "System Calls", "Memory Management", "Concurrency"],
                        duration: "12-16 weeks",
                        difficulty: "Advanced"
                    },
                    {
                        title: "Database & Backend Engineering",
                        description: "Master database design, query optimization, and backend architecture.",
                        skills: ["SQL", "Database Design", "API Development", "Performance Tuning"],
                        duration: "10-14 weeks",
                        difficulty: "Intermediate"
                    }
                ]
            },
            creative: {
                type: "The Creative Builder",
                description: "You love bringing ideas to life through code. You enjoy experimentation, user experience, and building unique solutions.",
                icon: "🎨",
                paths: [
                    {
                        title: "Frontend Development & UI/UX",
                        description: "Create beautiful, interactive user interfaces and engaging user experiences.",
                        skills: ["React/Vue", "CSS Animations", "UX Design", "Modern JavaScript"],
                        duration: "8-12 weeks",
                        difficulty: "Beginner to Intermediate"
                    },
                    {
                        title: "Game Development",
                        description: "Build games and interactive applications using modern game engines.",
                        skills: ["Unity/Unreal", "Game Design", "3D Graphics", "Physics"],
                        duration: "12-16 weeks",
                        difficulty: "Intermediate"
                    },
                    {
                        title: "Creative Coding & Generative Art",
                        description: "Explore the intersection of code and art through creative programming.",
                        skills: ["P5.js", "Three.js", "Shaders", "Algorithmic Art"],
                        duration: "6-10 weeks",
                        difficulty: "Beginner to Intermediate"
                    }
                ]
            },
            practical: {
                type: "The Practical Problem Solver",
                description: "You focus on building reliable, efficient solutions that solve real-world problems. You value best practices and proven methodologies.",
                icon: "🔧",
                paths: [
                    {
                        title: "Full-Stack Web Development",
                        description: "Build complete web applications using industry-standard tools and practices.",
                        skills: ["React", "Node.js", "Databases", "Testing", "Deployment"],
                        duration: "12-16 weeks",
                        difficulty: "Beginner to Advanced"
                    },
                    {
                        title: "DevOps & Cloud Engineering",
                        description: "Learn deployment, scaling, and infrastructure management in cloud environments.",
                        skills: ["AWS/Azure", "Docker", "Kubernetes", "CI/CD", "Monitoring"],
                        duration: "10-14 weeks",
                        difficulty: "Intermediate to Advanced"
                    },
                    {
                        title: "Enterprise Software Development",
                        description: "Master large-scale application development with focus on maintainability and scalability.",
                        skills: ["Java/C#", "Spring/ASP.NET", "Design Patterns", "Testing", "Architecture"],
                        duration: "14-18 weeks",
                        difficulty: "Intermediate to Advanced"
                    }
                ]
            },
            collaborative: {
                type: "The Collaborative Communicator",
                description: "You excel in team environments and enjoy working with others. You value communication, mentoring, and community-driven development.",
                icon: "🤝",
                paths: [
                    {
                        title: "Open Source Contribution",
                        description: "Learn to contribute effectively to open source projects and build your developer network.",
                        skills: ["Git/GitHub", "Code Review", "Community Building", "Documentation"],
                        duration: "6-8 weeks",
                        difficulty: "Beginner to Intermediate"
                    },
                    {
                        title: "Technical Leadership Track",
                        description: "Develop skills in technical communication, team leadership, and project management.",
                        skills: ["Team Management", "Technical Writing", "Mentoring", "Architecture Design"],
                        duration: "8-12 weeks",
                        difficulty: "Intermediate to Advanced"
                    },
                    {
                        title: "Community-Driven Development",
                        description: "Focus on building applications that serve communities and foster collaboration.",
                        skills: ["User Research", "Agile Methods", "Social Impact", "Product Management"],
                        duration: "10-14 weeks",
                        difficulty: "Intermediate"
                    }
                ]
            }
        };
    }

    init() {
        this.renderCurrentQuestion();
        this.setupEventListeners();
    }

    setupEventListeners() {
        document.addEventListener('change', (e) => {
            if (e.target.name && e.target.name.startsWith('question')) {
                this.handleAnswerSelection(e);
            }
        });

        // Navigation toggle for mobile
        const navToggle = document.querySelector('.nav-toggle');
        const navMenu = document.querySelector('.nav-menu');
        
        if (navToggle && navMenu) {
            navToggle.addEventListener('click', () => {
                navMenu.classList.toggle('active');
            });
        }
    }

    renderCurrentQuestion() {
        const quizContainer = document.getElementById('personality-quiz');
        if (!quizContainer) return;

        if (this.currentQuestionIndex < this.questions.length) {
            const question = this.questions[this.currentQuestionIndex];
            quizContainer.innerHTML = this.createQuestionHTML(question);
        } else {
            this.calculateResults();
        }
    }

    createQuestionHTML(question) {
        return `
            <div class="question-card fade-in">
                <div class="question-title">
                    Question ${this.currentQuestionIndex + 1} of ${this.questions.length}
                </div>
                <h3>${question.question}</h3>
                <div class="question-options">
                    ${question.options.map((option, index) => `
                        <div class="option">
                            <input type="radio" 
                                   id="q${question.id}_option${index}" 
                                   name="question${question.id}" 
                                   value="${index}"
                                   data-type="${option.type}"
                                   data-weight="${option.weight}">
                            <label for="q${question.id}_option${index}">${option.text}</label>
                        </div>
                    `).join('')}
                </div>
                <div class="mt-3">
                    <button onclick="personalityAssessment.nextQuestion()" 
                            class="cta-button" 
                            id="nextBtn" 
                            disabled>
                        ${this.currentQuestionIndex === this.questions.length - 1 ? 'See Results' : 'Next Question'}
                    </button>
                </div>
            </div>
        `;
    }

    handleAnswerSelection(event) {
        const questionId = event.target.name.replace('question', '');
        const selectedOption = this.questions[this.currentQuestionIndex].options[event.target.value];
        
        this.answers[questionId] = {
            option: event.target.value,
            type: selectedOption.type,
            weight: selectedOption.weight
        };

        // Enable next button
        document.getElementById('nextBtn').disabled = false;
    }

    nextQuestion() {
        this.currentQuestionIndex++;
        this.renderCurrentQuestion();
    }

    calculateResults() {
        // Calculate personality scores
        Object.values(this.answers).forEach(answer => {
            this.personalityScores[answer.type] += answer.weight;
        });

        // Find dominant personality type
        const dominantType = Object.keys(this.personalityScores).reduce((a, b) => 
            this.personalityScores[a] > this.personalityScores[b] ? a : b
        );

        // Find secondary type (for hybrid recommendations)
        const sortedTypes = Object.keys(this.personalityScores)
            .sort((a, b) => this.personalityScores[b] - this.personalityScores[a]);
        
        const secondaryType = sortedTypes[1];

        this.displayResults(dominantType, secondaryType);
    }

    displayResults(dominantType, secondaryType) {
        const quizContainer = document.getElementById('personality-quiz');
        const resultData = this.learningPaths[dominantType];
        
        // Store results in localStorage for integration with code analyzer
        localStorage.setItem('userPersonalityType', dominantType);
        localStorage.setItem('userPersonalityScores', JSON.stringify(this.personalityScores));

        quizContainer.innerHTML = `
            <div class="personality-result fade-in">
                <div class="personality-type">
                    ${resultData.icon} ${resultData.type}
                </div>
                <div class="personality-description">
                    ${resultData.description}
                </div>
                
                <div class="personality-scores mt-3">
                    <h4>Your Personality Breakdown:</h4>
                    <div class="scores-grid">
                        ${Object.entries(this.personalityScores).map(([type, score]) => `
                            <div class="score-item">
                                <span class="score-label">${this.capitalize(type)}:</span>
                                <div class="score-bar">
                                    <div class="score-fill" style="width: ${(score / Math.max(...Object.values(this.personalityScores))) * 100}%"></div>
                                </div>
                                <span class="score-value">${score}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <div class="mt-4">
                    <button onclick="personalityAssessment.showLearningPaths('${dominantType}')" 
                            class="cta-button">
                        View My Learning Paths
                    </button>
                    <button onclick="personalityAssessment.retakeAssessment()" 
                            class="cta-button mt-2" 
                            style="background: #6c757d;">
                        Retake Assessment
                    </button>
                </div>
            </div>
        `;

        // Add CSS for score bars
        this.addScoreBarStyles();
    }

    addScoreBarStyles() {
        if (!document.getElementById('score-bar-styles')) {
            const style = document.createElement('style');
            style.id = 'score-bar-styles';
            style.textContent = `
                .scores-grid {
                    display: grid;
                    gap: 1rem;
                    margin-top: 1rem;
                }
                .score-item {
                    display: flex;
                    align-items: center;
                    gap: 1rem;
                }
                .score-label {
                    min-width: 100px;
                    font-weight: 600;
                }
                .score-bar {
                    flex: 1;
                    height: 20px;
                    background: #e9ecef;
                    border-radius: 10px;
                    overflow: hidden;
                }
                .score-fill {
                    height: 100%;
                    background: linear-gradient(90deg, #3498db, #2980b9);
                    transition: width 1s ease-in-out;
                }
                .score-value {
                    min-width: 30px;
                    text-align: right;
                    font-weight: 600;
                    color: #3498db;
                }
            `;
            document.head.appendChild(style);
        }
    }

    showLearningPaths(personalityType) {
        const pathsSection = document.getElementById('learning-paths-section');
        const resultData = this.learningPaths[personalityType];
        
        pathsSection.innerHTML = `
            <div class="container">
                <div class="text-center mb-4">
                    <h2>Recommended Learning Paths for ${resultData.type}</h2>
                    <p>Based on your personality assessment, here are the learning paths that match your style:</p>
                </div>
                
                <div class="learning-paths">
                    ${resultData.paths.map((path, index) => `
                        <div class="learning-path-card fade-in" style="animation-delay: ${index * 0.1}s">
                            <div class="path-icon">${resultData.icon}</div>
                            <div class="path-title">${path.title}</div>
                            <div class="path-description">${path.description}</div>
                            <div class="path-skills">
                                ${path.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
                            </div>
                            <div class="path-duration">📅 ${path.duration}</div>
                            <div class="path-difficulty">🎯 ${path.difficulty}</div>
                            <button class="start-path-btn" onclick="personalityAssessment.startLearningPath('${path.title}')">
                                Start This Path
                            </button>
                        </div>
                    `).join('')}
                </div>
                
                <div class="text-center mt-4">
                    <a href="#code-analyzer" class="cta-button">
                        Try Code Analysis
                    </a>
                </div>
            </div>
        `;
        
        pathsSection.style.display = 'block';
        pathsSection.scrollIntoView({ behavior: 'smooth' });
    }

    startLearningPath(pathTitle) {
        // Store selected learning path
        localStorage.setItem('selectedLearningPath', pathTitle);
        
        // Show confirmation and redirect to code analyzer
        alert(`Great choice! "${pathTitle}" has been set as your learning focus. Now try analyzing some code to get personalized recommendations!`);
        
        // Scroll to code analyzer
        document.getElementById('code-analyzer').scrollIntoView({ behavior: 'smooth' });
    }

    retakeAssessment() {
        this.currentQuestionIndex = 0;
        this.answers = {};
        this.personalityScores = {
            analytical: 0,
            creative: 0,
            practical: 0,
            collaborative: 0
        };
        
        // Clear stored results
        localStorage.removeItem('userPersonalityType');
        localStorage.removeItem('userPersonalityScores');
        localStorage.removeItem('selectedLearningPath');
        
        // Hide learning paths section
        document.getElementById('learning-paths-section').style.display = 'none';
        
        // Restart quiz
        this.renderCurrentQuestion();
        
        // Scroll back to quiz
        document.getElementById('personality-assessment').scrollIntoView({ behavior: 'smooth' });
    }

    capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    // Get personality-based recommendations for code analysis
    getPersonalizedRecommendations(analysisResults) {
        const personalityType = localStorage.getItem('userPersonalityType');
        const selectedPath = localStorage.getItem('selectedLearningPath');
        
        if (!personalityType) {
            return null;
        }

        const personalityData = this.learningPaths[personalityType];
        
        // Generate personality-specific suggestions
        let suggestions = {
            personality_type: personalityData.type,
            selected_path: selectedPath,
            personalized_tips: this.getPersonalityTips(personalityType, analysisResults),
            recommended_resources: this.getPersonalityResources(personalityType),
            next_steps: this.getPersonalityNextSteps(personalityType, analysisResults)
        };

        return suggestions;
    }

    getPersonalityTips(personalityType, analysis) {
        const tips = {
            analytical: [
                "Focus on understanding the algorithmic complexity of your solution",
                "Consider edge cases and error handling thoroughly",
                "Look into formal verification methods for critical code",
                "Study the mathematical foundations of algorithms you're using"
            ],
            creative: [
                "Experiment with different approaches to the same problem",
                "Consider the user experience and interface design",
                "Look for opportunities to add innovative features",
                "Try implementing your solution in multiple languages for comparison"
            ],
            practical: [
                "Focus on code maintainability and readability",
                "Implement proper error handling and logging",
                "Consider scalability and performance implications",
                "Follow established design patterns and best practices"
            ],
            collaborative: [
                "Document your code thoroughly for other developers",
                "Consider writing unit tests to help teammates understand your intent",
                "Look for opportunities to share your solution with the community",
                "Seek feedback from peers and incorporate their suggestions"
            ]
        };

        return tips[personalityType] || [];
    }

    getPersonalityResources(personalityType) {
        const resources = {
            analytical: [
                { title: "Introduction to Algorithms (CLRS)", type: "Book" },
                { title: "Algorithm Design Manual", type: "Book" },
                { title: "MIT OpenCourseWare - Algorithms", type: "Course" },
                { title: "LeetCode - Algorithm Problems", type: "Practice" }
            ],
            creative: [
                { title: "Creative Coding with p5.js", type: "Course" },
                { title: "The Nature of Code", type: "Book" },
                { title: "Processing Community", type: "Community" },
                { title: "CodePen - Creative Experiments", type: "Platform" }
            ],
            practical: [
                { title: "Clean Code by Robert Martin", type: "Book" },
                { title: "Effective Java/Python/C++", type: "Book" },
                { title: "Design Patterns: Elements of Reusable OO Software", type: "Book" },
                { title: "Stack Overflow", type: "Community" }
            ],
            collaborative: [
                { title: "GitHub - Open Source Projects", type: "Platform" },
                { title: "Dev.to - Developer Community", type: "Community" },
                { title: "First Timers Only", type: "Initiative" },
                { title: "Mozilla Developer Network", type: "Documentation" }
            ]
        };

        return resources[personalityType] || [];
    }

    getPersonalityNextSteps(personalityType, analysis) {
        const steps = {
            analytical: [
                "Analyze the time and space complexity of your solution",
                "Research alternative algorithms for the same problem",
                "Implement unit tests to verify correctness",
                "Study the underlying data structures used"
            ],
            creative: [
                "Brainstorm alternative creative solutions",
                "Add visual or interactive elements to your code",
                "Share your solution in a creative coding community",
                "Experiment with different programming paradigms"
            ],
            practical: [
                "Refactor your code for better maintainability",
                "Add comprehensive error handling",
                "Create documentation for your solution",
                "Consider how this fits into a larger system"
            ],
            collaborative: [
                "Share your solution for peer review",
                "Contribute to open source projects with similar problems",
                "Write a blog post explaining your approach",
                "Mentor someone else working on similar problems"
            ]
        };

        return steps[personalityType] || [];
    }
}

// Initialize the personality assessment
const personalityAssessment = new PersonalityAssessment();

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    personalityAssessment.init();
});
