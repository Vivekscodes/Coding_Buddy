// Code Analysis Integration with Personality Assessment

class CodeAnalyzer {
    constructor() {
        this.setupEventListeners();
        this.apiBaseUrl = window.location.origin; // Use current domain for API calls
    }

    setupEventListeners() {
        document.addEventListener('DOMContentLoaded', () => {
            const analyzeBtn = document.getElementById('analyze-btn');
            if (analyzeBtn) {
                analyzeBtn.addEventListener('click', () => this.analyzeCode());
            }

            // Check if user has completed personality assessment
            this.checkPersonalityStatus();
        });
    }

    checkPersonalityStatus() {
        const personalityType = localStorage.getItem('userPersonalityType');
        const codeAnalyzerSection = document.getElementById('code-analyzer');
        
        if (personalityType && codeAnalyzerSection) {
            // Add personality indicator to code analyzer
            this.addPersonalityIndicator(personalityType);
        }
    }

    addPersonalityIndicator(personalityType) {
        const container = document.querySelector('.code-analyzer');
        const personalityData = this.getPersonalityData(personalityType);
        
        if (container && personalityData) {
            const indicator = document.createElement('div');
            indicator.className = 'personality-indicator';
            indicator.innerHTML = `
                <div class="personality-status">
                    <div class="personality-badge">
                        <span class="personality-icon">${personalityData.icon}</span>
                        <span class="personality-text">Analyzing as: ${personalityData.type}</span>
                    </div>
                    <button class="retake-btn" onclick="personalityAssessment.retakeAssessment()">
                        Change Personality
                    </button>
                </div>
            `;
            
            container.insertBefore(indicator, container.firstChild);
            this.addPersonalityIndicatorStyles();
        }
    }

    addPersonalityIndicatorStyles() {
        if (!document.getElementById('personality-indicator-styles')) {
            const style = document.createElement('style');
            style.id = 'personality-indicator-styles';
            style.textContent = `
                .personality-indicator {
                    background: linear-gradient(135deg, #e3f2fd, #f8f9fa);
                    border: 2px solid #3498db;
                    border-radius: 10px;
                    padding: 1rem;
                    margin-bottom: 2rem;
                    text-align: center;
                }
                
                .personality-status {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    flex-wrap: wrap;
                    gap: 1rem;
                }
                
                .personality-badge {
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    font-weight: 600;
                    color: #2c3e50;
                }
                
                .personality-icon {
                    font-size: 1.5rem;
                }
                
                .retake-btn {
                    background: #6c757d;
                    color: white;
                    border: none;
                    padding: 0.5rem 1rem;
                    border-radius: 20px;
                    font-size: 0.9rem;
                    cursor: pointer;
                    transition: background 0.3s;
                }
                
                .retake-btn:hover {
                    background: #5a6268;
                }
                
                @media (max-width: 768px) {
                    .personality-status {
                        justify-content: center;
                        text-align: center;
                    }
                }
            `;
            document.head.appendChild(style);
        }
    }

    getPersonalityData(personalityType) {
        const personalityMap = {
            analytical: { type: "The Analytical Thinker", icon: "🧠" },
            creative: { type: "The Creative Builder", icon: "🎨" },
            practical: { type: "The Practical Problem Solver", icon: "🔧" },
            collaborative: { type: "The Collaborative Communicator", icon: "🤝" }
        };
        
        return personalityMap[personalityType];
    }

    async analyzeCode() {
        const code = document.getElementById('code-input').value.trim();
        const language = document.getElementById('language-select').value;
        const problemTitle = document.getElementById('problem-title').value.trim();
        const expectedBehavior = document.getElementById('expected-behavior').value.trim();

        if (!code || !problemTitle) {
            alert('Please provide both a problem title and your code.');
            return;
        }

        this.showLoading();
        
        try {
            // Get personality information from localStorage
            const personalityType = localStorage.getItem('userPersonalityType');
            const personalityScores = localStorage.getItem('userPersonalityScores');
            
            const requestBody = {
                code: code,
                language: language,
                problem_title: problemTitle,
                expected_behavior: expectedBehavior
            };
            
            // Add personality information if available
            if (personalityType) {
                requestBody.personality_type = personalityType;
            }
            
            if (personalityScores) {
                try {
                    requestBody.personality_scores = JSON.parse(personalityScores);
                } catch (e) {
                    console.warn('Failed to parse personality scores:', e);
                }
            }

            const response = await fetch(`${this.apiBaseUrl}/api/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody)
            });

            const data = await response.json();

            if (response.ok && data.analysis) {
                this.displayResults(data);
            } else {
                throw new Error(data.error || 'Analysis failed');
            }
        } catch (error) {
            console.error('Analysis error:', error);
            this.showError(error.message);
        } finally {
            this.hideLoading();
        }
    }

    showLoading() {
        const loading = document.getElementById('loading');
        const analyzeBtn = document.getElementById('analyze-btn');
        
        if (loading) loading.classList.add('active');
        if (analyzeBtn) {
            analyzeBtn.disabled = true;
            analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
        }
    }

    hideLoading() {
        const loading = document.getElementById('loading');
        const analyzeBtn = document.getElementById('analyze-btn');
        
        if (loading) loading.classList.remove('active');
        if (analyzeBtn) {
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = '<i class="fas fa-search"></i> Analyze Code';
        }
    }

    showError(message) {
        const resultsSection = document.getElementById('results-section');
        if (resultsSection) {
            resultsSection.style.display = 'block';
            resultsSection.innerHTML = `
                <div class="error-message">
                    <div class="error-icon">⚠️</div>
                    <h3>Analysis Error</h3>
                    <p>${message}</p>
                    <button onclick="location.reload()" class="retry-btn">
                        <i class="fas fa-redo"></i> Try Again
                    </button>
                </div>
            `;
            this.addErrorStyles();
        }
    }

    addErrorStyles() {
        if (!document.getElementById('error-message-styles')) {
            const style = document.createElement('style');
            style.id = 'error-message-styles';
            style.textContent = `
                .error-message {
                    text-align: center;
                    padding: 3rem;
                    background: #fff5f5;
                    border: 2px solid #fed7d7;
                    border-radius: 10px;
                    color: #742a2a;
                }
                
                .error-icon {
                    font-size: 3rem;
                    margin-bottom: 1rem;
                }
                
                .retry-btn {
                    background: #e53e3e;
                    color: white;
                    border: none;
                    padding: 0.8rem 1.5rem;
                    border-radius: 25px;
                    font-weight: 600;
                    cursor: pointer;
                    margin-top: 1rem;
                    transition: background 0.3s;
                }
                
                .retry-btn:hover {
                    background: #c53030;
                }
            `;
            document.head.appendChild(style);
        }
    }

    displayResults(data) {
        const resultsSection = document.getElementById('results-section');
        if (!resultsSection) return;

        // Show results section
        resultsSection.style.display = 'block';

        // Display analysis results
        this.displayAnalysis(data.analysis);
        
        // Display validation results
        if (data.validation) {
            this.displayValidation(data.validation);
        }

        // Display personalized recommendations
        this.displayPersonalizedRecommendations(data);

        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    displayAnalysis(analysis) {
        const analysisContent = document.getElementById('analysis-content');
        if (!analysisContent) return;

        analysisContent.innerHTML = `
            <div class="analysis-metrics">
                <div class="metric-row">
                    <span class="metric-label">Quality Score:</span>
                    <span class="metric-value">${Math.round(analysis.quality_score || 0)}/100</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Complexity Score:</span>
                    <span class="metric-value">${Math.round(analysis.complexity_score || 0)}/100</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Time Complexity:</span>
                    <span class="metric-value">${analysis.time_complexity || 'Unknown'}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Space Complexity:</span>
                    <span class="metric-value">${analysis.space_complexity || 'Unknown'}</span>
                </div>
            </div>

            ${this.renderTags('Patterns', analysis.patterns)}
            ${this.renderTags('Algorithms', analysis.algorithms)}
            ${this.renderTags('Data Structures', analysis.data_structures)}
        `;
    }

    displayValidation(validation) {
        const validationContent = document.getElementById('validation-content');
        if (!validationContent) return;

        const isCorrect = validation.is_correct;
        const statusClass = isCorrect ? 'status-correct' : 'status-error';
        const statusIcon = isCorrect ? '✅' : '❌';
        const statusText = isCorrect ? 'Code is Correct' : 'Issues Found';

        validationContent.innerHTML = `
            <div class="validation-status ${statusClass}">
                <span class="status-icon">${statusIcon}</span>
                <span class="status-text">${statusText}</span>
            </div>

            ${validation.correctness_explanation ? `
                <div class="validation-explanation">
                    <strong>Explanation:</strong>
                    <p>${validation.correctness_explanation}</p>
                </div>
            ` : ''}

            ${this.renderValidationErrors(validation)}
            ${this.renderSolutions(validation.solutions)}
            
            ${validation.overall_assessment ? `
                <div class="overall-assessment">
                    <strong>Overall Assessment:</strong>
                    <p>${validation.overall_assessment}</p>
                </div>
            ` : ''}
        `;
    }

    displayPersonalizedRecommendations(data) {
        const recommendationsContent = document.getElementById('recommendations-content');
        if (!recommendationsContent) return;

        let content = '';

        // Standard recommendations
        if (data.recommendations) {
            const recs = data.recommendations;
            
            if (recs.knowledge_gaps && recs.knowledge_gaps.length > 0) {
                content += `
                    <div class="recommendation-section">
                        <h4><i class="fas fa-exclamation-triangle"></i> Knowledge Gaps</h4>
                        ${recs.knowledge_gaps.map(gap => `
                            <div class="recommendation-item">
                                <strong>${gap.concept}</strong> (${gap.severity})
                                <p>${gap.reason}</p>
                            </div>
                        `).join('')}
                    </div>
                `;
            }

            if (recs.concepts_to_learn && recs.concepts_to_learn.length > 0) {
                content += `
                    <div class="recommendation-section">
                        <h4><i class="fas fa-graduation-cap"></i> Concepts to Learn</h4>
                        ${recs.concepts_to_learn.map(concept => `
                            <div class="recommendation-item">
                                <strong>${concept.concept}</strong> - ${concept.difficulty}
                                <p>Estimated time: ${concept.estimated_time} minutes</p>
                            </div>
                        `).join('')}
                    </div>
                `;
            }

            if (recs.improvement_suggestions && recs.improvement_suggestions.length > 0) {
                content += `
                    <div class="recommendation-section">
                        <h4><i class="fas fa-arrow-up"></i> Improvement Suggestions</h4>
                        ${recs.improvement_suggestions.map(suggestion => `
                            <div class="recommendation-item">
                                <p>${suggestion}</p>
                            </div>
                        `).join('')}
                    </div>
                `;
            }

            // Display personality-specific recommendations from backend
            if (recs.personality_recommendations) {
                const personalityRecs = recs.personality_recommendations;
                const personalityType = data.personality_type || personalityRecs.personality_type;
                
                content += `
                    <div class="personality-recommendations">
                        <h4><i class="fas fa-user"></i> Personalized for ${this.getPersonalityTypeName(personalityType)}</h4>
                        
                        ${personalityRecs.personalized_feedback ? `
                            <div class="personality-feedback">
                                <h5>💬 Personalized Feedback:</h5>
                                <p>${personalityRecs.personalized_feedback}</p>
                            </div>
                        ` : ''}

                        ${personalityRecs.personality_strengths && personalityRecs.personality_strengths.length > 0 ? `
                            <div class="recommendation-section">
                                <h5>💪 Your Strengths:</h5>
                                ${personalityRecs.personality_strengths.map(strength => `
                                    <div class="tip-item">• ${strength}</div>
                                `).join('')}
                            </div>
                        ` : ''}

                        ${personalityRecs.learning_path_suggestions && personalityRecs.learning_path_suggestions.length > 0 ? `
                            <div class="recommendation-section">
                                <h5>🎯 Learning Path Suggestions:</h5>
                                ${personalityRecs.learning_path_suggestions.map(suggestion => `
                                    <div class="tip-item">• ${suggestion}</div>
                                `).join('')}
                            </div>
                        ` : ''}

                        ${personalityRecs.recommended_resources && personalityRecs.recommended_resources.length > 0 ? `
                            <div class="recommendation-section">
                                <h5>📚 Recommended Resources:</h5>
                                ${personalityRecs.recommended_resources.map(resource => `
                                    <div class="resource-item">
                                        <strong>${resource.title}</strong> (${resource.type})
                                        ${resource.reason ? `<br><small>${resource.reason}</small>` : ''}
                                    </div>
                                `).join('')}
                            </div>
                        ` : ''}

                        ${personalityRecs.practice_problems && personalityRecs.practice_problems.length > 0 ? `
                            <div class="recommendation-section">
                                <h5>🧩 Practice Problems:</h5>
                                ${personalityRecs.practice_problems.map(problem => `
                                    <div class="resource-item">
                                        <strong>${problem.title}</strong> (${problem.difficulty})
                                        ${problem.reason ? `<br><small>${problem.reason}</small>` : ''}
                                    </div>
                                `).join('')}
                            </div>
                        ` : ''}

                        ${personalityRecs.motivation_boosters && personalityRecs.motivation_boosters.length > 0 ? `
                            <div class="recommendation-section">
                                <h5>🚀 Motivation Boosters:</h5>
                                ${personalityRecs.motivation_boosters.map(booster => `
                                    <div class="tip-item">• ${booster}</div>
                                `).join('')}
                            </div>
                        ` : ''}

                        ${personalityRecs.learning_strategies && personalityRecs.learning_strategies.length > 0 ? `
                            <div class="recommendation-section">
                                <h5>📖 Learning Strategies:</h5>
                                ${personalityRecs.learning_strategies.map(strategy => `
                                    <div class="tip-item">• ${strategy}</div>
                                `).join('')}
                            </div>
                        ` : ''}
                    </div>
                `;
            }
        }

        // Fallback personality recommendations from frontend
        if (!data.recommendations?.personality_recommendations) {
            const personalizedRecs = window.personalityAssessment ? 
                window.personalityAssessment.getPersonalizedRecommendations(data.analysis) : null;

            if (personalizedRecs) {
                content += `
                    <div class="personality-recommendations">
                        <h4><i class="fas fa-user"></i> Personalized for ${personalizedRecs.personality_type}</h4>
                        
                        ${personalizedRecs.selected_path ? `
                            <div class="selected-path">
                                <strong>Your Learning Focus:</strong> ${personalizedRecs.selected_path}
                            </div>
                        ` : ''}

                        <div class="recommendation-section">
                            <h5>Tips for Your Personality Type:</h5>
                            ${personalizedRecs.personalized_tips.map(tip => `
                                <div class="tip-item">• ${tip}</div>
                            `).join('')}
                        </div>

                        <div class="recommendation-section">
                            <h5>Recommended Resources:</h5>
                            ${personalizedRecs.recommended_resources.map(resource => `
                                <div class="resource-item">
                                    <strong>${resource.title}</strong> (${resource.type})
                                </div>
                            `).join('')}
                        </div>

                        <div class="recommendation-section">
                            <h5>Next Steps:</h5>
                            ${personalizedRecs.next_steps.map(step => `
                                <div class="step-item">• ${step}</div>
                            `).join('')}
                        </div>
                    </div>
                `;
            } else if (!data.personality_type) {
                content += `
                    <div class="no-personality-prompt">
                        <p><strong>Want personalized recommendations?</strong></p>
                        <p>Take our personality assessment to get recommendations tailored to your learning style!</p>
                        <a href="#personality-assessment" class="cta-button">Take Assessment</a>
                    </div>
                `;
            }
        }

        recommendationsContent.innerHTML = content || '<p>No specific recommendations available.</p>';
    }

    getPersonalityTypeName(personalityType) {
        const typeNames = {
            'analytical': 'The Analytical Thinker',
            'creative': 'The Creative Builder',
            'practical': 'The Practical Problem Solver',
            'collaborative': 'The Collaborative Communicator'
        };
        return typeNames[personalityType] || personalityType;
    }

    renderTags(title, items) {
        if (!items || items.length === 0) return '';
        
        return `
            <div class="tags-section">
                <strong>${title}:</strong>
                <div class="tags-container">
                    ${items.map(item => `<span class="tag">${item}</span>`).join('')}
                </div>
            </div>
        `;
    }

    renderValidationErrors(validation) {
        const errorTypes = [
            { key: 'syntax_errors', title: 'Syntax Errors', icon: '🔴' },
            { key: 'logic_errors', title: 'Logic Errors', icon: '🟠' },
            { key: 'runtime_errors', title: 'Runtime Errors', icon: '🟡' },
            { key: 'performance_issues', title: 'Performance Issues', icon: '🔵' },
            { key: 'best_practice_violations', title: 'Best Practice Violations', icon: '🟣' }
        ];

        let content = '';
        
        errorTypes.forEach(type => {
            const errors = validation[type.key] || [];
            if (errors.length > 0) {
                content += `
                    <div class="error-section">
                        <h5>${type.icon} ${type.title}</h5>
                        ${errors.map(error => `
                            <div class="error-item">${error}</div>
                        `).join('')}
                    </div>
                `;
            }
        });

        return content;
    }

    renderSolutions(solutions) {
        if (!solutions || solutions.length === 0) return '';

        return `
            <div class="solutions-section">
                <h4><i class="fas fa-wrench"></i> Suggested Solutions</h4>
                ${solutions.map((solution, index) => `
                    <div class="solution-item">
                        <h5>Solution ${index + 1}:</h5>
                        <p><strong>Issue:</strong> ${solution.issue || 'N/A'}</p>
                        <p><strong>Fix:</strong> ${solution.solution || 'N/A'}</p>
                        ${solution.explanation ? `<p><strong>Why:</strong> ${solution.explanation}</p>` : ''}
                        ${solution.corrected_code ? `
                            <div class="corrected-code">
                                <strong>Corrected Code:</strong>
                                <pre><code>${solution.corrected_code}</code></pre>
                            </div>
                        ` : ''}
                    </div>
                `).join('')}
            </div>
        `;
    }
}

// Initialize code analyzer
const codeAnalyzer = new CodeAnalyzer();

// Add additional styles for results display
document.addEventListener('DOMContentLoaded', () => {
    if (!document.getElementById('results-display-styles')) {
        const style = document.createElement('style');
        style.id = 'results-display-styles';
        style.textContent = `
            .analysis-metrics {
                margin-bottom: 1.5rem;
            }
            
            .metric-row {
                display: flex;
                justify-content: space-between;
                padding: 0.5rem 0;
                border-bottom: 1px solid #e9ecef;
            }
            
            .metric-label {
                font-weight: 600;
            }
            
            .metric-value {
                color: #3498db;
                font-weight: 600;
            }
            
            .tags-section {
                margin: 1rem 0;
            }
            
            .tags-container {
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem;
                margin-top: 0.5rem;
            }
            
            .tag {
                background: #e3f2fd;
                color: #1976d2;
                padding: 0.25rem 0.75rem;
                border-radius: 15px;
                font-size: 0.9rem;
                font-weight: 500;
            }
            
            .validation-status {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                padding: 1rem;
                border-radius: 5px;
                margin-bottom: 1rem;
                font-weight: 600;
            }
            
            .status-correct {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            
            .status-error {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            
            .status-icon {
                font-size: 1.2rem;
            }
            
            .validation-explanation {
                margin: 1rem 0;
            }
            
            .error-section {
                margin: 1rem 0;
            }
            
            .error-item {
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                padding: 0.5rem;
                border-radius: 4px;
                margin-bottom: 0.5rem;
                font-size: 0.9rem;
            }
            
            .solutions-section {
                margin-top: 1.5rem;
            }
            
            .solution-item {
                background: #e8f5e8;
                border: 1px solid #d4edda;
                padding: 1rem;
                border-radius: 5px;
                margin-bottom: 1rem;
            }
            
            .corrected-code {
                margin-top: 0.5rem;
            }
            
            .corrected-code pre {
                background: #f8f9fa;
                padding: 0.5rem;
                border-radius: 4px;
                overflow-x: auto;
                font-size: 0.9rem;
            }
            
            .recommendation-section {
                margin: 1.5rem 0;
            }
            
            .recommendation-item {
                background: #f8f9fa;
                padding: 1rem;
                border-radius: 5px;
                margin-bottom: 0.5rem;
            }
            
            .personality-recommendations {
                background: linear-gradient(135deg, #e3f2fd, #f8f9fa);
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 1.5rem;
                margin-top: 1.5rem;
            }
            
            .selected-path {
                background: #3498db;
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 20px;
                text-align: center;
                margin-bottom: 1rem;
                font-weight: 600;
            }
            
            .tip-item,
            .step-item {
                padding: 0.25rem 0;
                color: #2c3e50;
            }
            
            .resource-item {
                background: white;
                padding: 0.5rem;
                border-radius: 4px;
                margin-bottom: 0.25rem;
                font-size: 0.9rem;
            }
            
            .no-personality-prompt {
                text-align: center;
                padding: 2rem;
                background: linear-gradient(135deg, #fff3cd, #f8f9fa);
                border: 2px solid #ffc107;
                border-radius: 10px;
            }
            
            .overall-assessment {
                background: #e8f5e8;
                padding: 1rem;
                border-radius: 5px;
                margin-top: 1rem;
            }
        `;
        document.head.appendChild(style);
    }
});

// Add personality feedback styles
document.addEventListener('DOMContentLoaded', () => {
    if (!document.getElementById('personality-feedback-styles')) {
        const personalityStyle = document.createElement('style');
        personalityStyle.id = 'personality-feedback-styles';
        personalityStyle.textContent = \
            .personality-feedback {
                background: rgba(52, 152, 219, 0.1);
                border-left: 4px solid #3498db;
                padding: 1rem;
                margin-bottom: 1rem;
                border-radius: 0 5px 5px 0;
            }
            
            .personality-feedback h5 {
                margin-top: 0;
                color: #2980b9;
            }
        \;
        document.head.appendChild(personalityStyle);
    }
});
