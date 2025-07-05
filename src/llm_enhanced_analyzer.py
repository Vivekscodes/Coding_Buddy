import os
import json
from typing import Dict, Any, List, Optional
import google.generativeai as genai
from .code_analyzer import CodeAnalyzer


class LLMEnhancedAnalyzer(CodeAnalyzer):
    """
    Enhanced code analyzer that combines traditional static analysis 
    with Gemini 2.0 Flash-powered deep code understanding and personality-based recommendations.
    """

    def __init__(self):
        super().__init__()
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.use_llm = bool(self.api_key)
        if self.use_llm:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Define personality types and their characteristics
        self.personality_types = {
            'analytical': {
                'name': 'The Analytical Thinker',
                'description': 'Loves algorithms, data structures, and understanding systems deeply',
                'focus_areas': ['algorithms', 'complexity_analysis', 'mathematical_foundations', 'optimization'],
                'learning_style': 'systematic and thorough',
                'preferred_feedback': 'detailed technical explanations with mathematical rigor'
            },
            'creative': {
                'name': 'The Creative Builder',
                'description': 'Enjoys building unique solutions and creative applications',
                'focus_areas': ['innovation', 'user_experience', 'alternative_approaches', 'experimentation'],
                'learning_style': 'exploratory and experimental',
                'preferred_feedback': 'creative alternatives and innovative approaches'
            },
            'practical': {
                'name': 'The Practical Problem Solver',
                'description': 'Focuses on real-world applications and best practices',
                'focus_areas': ['best_practices', 'maintainability', 'scalability', 'industry_standards'],
                'learning_style': 'structured and methodical',
                'preferred_feedback': 'practical improvements and industry best practices'
            },
            'collaborative': {
                'name': 'The Collaborative Communicator',
                'description': 'Thrives in team environments and values knowledge sharing',
                'focus_areas': ['code_readability', 'documentation', 'team_collaboration', 'mentoring'],
                'learning_style': 'social and discussion-based',
                'preferred_feedback': 'communication tips and collaborative development practices'
            }
        }

    def analyze_code_with_llm(self, code: str, language: str, personality_type: Optional[str] = None) -> Dict[str, Any]:
        """Enhanced analysis combining traditional methods with Gemini insights and personality-based recommendations."""
        traditional_analysis = self.analyze_code(code, language)

        if not self.use_llm:
            print("⚠️ Gemini API key not found. Using traditional analysis only.")
            return traditional_analysis

        llm_insights = self._get_llm_insights(code, language, traditional_analysis, personality_type)
        return self._merge_analyses(traditional_analysis, llm_insights)

    def analyze_with_personality(self, code: str, language: str, personality_type: str, 
                               personality_scores: Optional[Dict[str, int]] = None) -> Dict[str, Any]:
        """Analyze code with personality-specific recommendations and learning paths."""
        # Get base analysis
        analysis = self.analyze_code_with_llm(code, language, personality_type)
        
        # Add personality-specific insights
        personality_insights = self._get_personality_insights(
            code, language, analysis, personality_type, personality_scores
        )
        
        analysis['personality_insights'] = personality_insights
        return analysis

    def _get_llm_insights(self, code: str, language: str, traditional_analysis: Dict[str, Any], 
                         personality_type: Optional[str] = None) -> Dict[str, Any]:
        """Get insights from Gemini LLM about the code."""
        prompt = self._create_analysis_prompt(code, language, traditional_analysis, personality_type)
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=1500,
                    temperature=0.3,
                )
            )
            return self._parse_llm_response(response.text)
        except Exception as e:
            print(f"Gemini analysis failed: {e}")
            return {}

    def _get_personality_insights(self, code: str, language: str, analysis: Dict[str, Any], 
                                personality_type: str, personality_scores: Optional[Dict[str, int]] = None) -> Dict[str, Any]:
        """Generate personality-specific insights and recommendations."""
        if not self.use_llm or personality_type not in self.personality_types:
            return self._get_fallback_personality_insights(personality_type)
        
        personality_data = self.personality_types[personality_type]
        prompt = self._create_personality_prompt(code, language, analysis, personality_type, personality_data, personality_scores)
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2000,
                    temperature=0.4,
                )
            )
            return self._parse_personality_response(response.text, personality_type)
        except Exception as e:
            print(f"Personality analysis failed: {e}")
            return self._get_fallback_personality_insights(personality_type)

    def _create_analysis_prompt(self, code: str, language: str, traditional_analysis: Dict[str, Any], 
                              personality_type: Optional[str] = None) -> str:
        """Create a comprehensive prompt for LLM analysis."""
        personality_context = ""
        if personality_type and personality_type in self.personality_types:
            personality_data = self.personality_types[personality_type]
            personality_context = f"""
Student Personality Type: {personality_data['name']}
Learning Style: {personality_data['learning_style']}
Preferred Feedback: {personality_data['preferred_feedback']}
Focus Areas: {', '.join(personality_data['focus_areas'])}
"""

        return f"""
You are an expert coding mentor and computer science teacher.
Analyze the following {language} code and provide educational insights.

```{language}
{code}
```

Traditional analysis detected:
- Patterns: {traditional_analysis.get('patterns', [])}
- Algorithms: {traditional_analysis.get('algorithms', [])}
- Data Structures: {traditional_analysis.get('data_structures', [])}
- Time Complexity: {traditional_analysis.get('time_complexity', 'Unknown')}
- Space Complexity: {traditional_analysis.get('space_complexity', 'Unknown')}

{personality_context}

Please provide a JSON response with:

{{
"algorithm_explanation": "Detailed explanation of the algorithm used",
"optimization_suggestions": ["specific suggestions for improvement"],
"learning_concepts": ["key concepts student should understand"],
"alternative_approaches": ["other ways to solve this problem"],
"code_quality_feedback": "specific feedback on code style and structure",
"complexity_explanation": "why this complexity is correct/incorrect",
"interview_tips": ["tips for explaining this in interviews"],
"related_problems": ["similar problems to practice"],
"conceptual_gaps": ["concepts the student might be missing"],
"positive_aspects": ["what the student did well"]
}}
        """

    def _create_personality_prompt(self, code: str, language: str, analysis: Dict[str, Any], 
                                 personality_type: str, personality_data: Dict[str, Any], 
                                 personality_scores: Optional[Dict[str, int]] = None) -> str:
        """Create a prompt for personality-specific recommendations."""
        scores_context = ""
        if personality_scores:
            scores_context = f"Personality Scores: {personality_scores}"

        return f"""
You are a personalized coding education specialist who tailors learning recommendations to individual personality types.

Student Profile:
- Personality Type: {personality_data['name']} ({personality_type})
- Description: {personality_data['description']}
- Learning Style: {personality_data['learning_style']}
- Focus Areas: {', '.join(personality_data['focus_areas'])}
- Preferred Feedback Style: {personality_data['preferred_feedback']}
{scores_context}

Code Analysis Results:
- Language: {language}
- Time Complexity: {analysis.get('time_complexity', 'Unknown')}
- Space Complexity: {analysis.get('space_complexity', 'Unknown')}
- Quality Score: {analysis.get('quality_score', 'Unknown')}
- Patterns Used: {analysis.get('patterns', [])}
- Algorithms: {analysis.get('algorithms', [])}

Based on this student's personality type and code analysis, provide personalized learning recommendations in JSON format:

{{
"personalized_feedback": "Feedback tailored to their personality type and learning style",
"learning_path_suggestions": ["specific next steps aligned with their personality"],
"personality_strengths": ["how their personality type helps with this code/problem"],
"growth_opportunities": ["areas where their personality type might face challenges"],
"recommended_resources": [
    {{
        "title": "resource title",
        "type": "book/course/tutorial/practice",
        "reason": "why this fits their personality",
        "difficulty": "beginner/intermediate/advanced"
    }}
],
"practice_problems": [
    {{
        "title": "problem title",
        "difficulty": "easy/medium/hard",
        "reason": "why this problem suits their learning style",
        "focus_area": "what skill this develops"
    }}
],
"collaboration_tips": ["how to leverage their personality in team settings"],
"motivation_boosters": ["personality-specific encouragement and motivation"],
"learning_strategies": ["study methods that work best for their type"]
}}
        """

    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse the JSON response from the LLM."""
        try:
            # Clean the response in case it has markdown formatting
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]  # Remove ```json
            if response.endswith('```'):
                response = response[:-3]  # Remove ```
            
            return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"Failed to parse LLM response as JSON: {e}")
            print(f"Response was: {response}")
            return {
                "algorithm_explanation": "Unable to parse LLM response",
                "optimization_suggestions": [],
                "learning_concepts": [],
                "alternative_approaches": [],
                "code_quality_feedback": "Response parsing failed",
                "complexity_explanation": "Unknown",
                "interview_tips": [],
                "related_problems": [],
                "conceptual_gaps": [],
                "positive_aspects": []
            }

    def _parse_personality_response(self, response: str, personality_type: str) -> Dict[str, Any]:
        """Parse the personality-specific response from the LLM."""
        try:
            # Clean the response
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            
            parsed = json.loads(response)
            parsed['personality_type'] = personality_type
            return parsed
        except json.JSONDecodeError as e:
            print(f"Failed to parse personality response: {e}")
            return self._get_fallback_personality_insights(personality_type)

    def _get_fallback_personality_insights(self, personality_type: str) -> Dict[str, Any]:
        """Provide fallback personality insights when LLM is unavailable."""
        if personality_type not in self.personality_types:
            personality_type = 'practical'  # Default fallback
        
        personality_data = self.personality_types[personality_type]
        
        fallback_insights = {
            'analytical': {
                'personalized_feedback': 'Focus on understanding the algorithmic complexity and mathematical foundations of your solution.',
                'learning_path_suggestions': [
                    'Study algorithm design and analysis',
                    'Practice complexity analysis',
                    'Learn formal verification methods',
                    'Explore mathematical optimization techniques'
                ],
                'personality_strengths': [
                    'Strong logical thinking helps in algorithm design',
                    'Attention to detail aids in finding edge cases',
                    'Systematic approach leads to robust solutions'
                ],
                'growth_opportunities': [
                    'Consider user experience and practical applications',
                    'Practice explaining complex concepts simply',
                    'Balance theoretical perfection with practical constraints'
                ]
            },
            'creative': {
                'personalized_feedback': 'Explore alternative approaches and consider the user experience of your solution.',
                'learning_path_suggestions': [
                    'Experiment with different programming paradigms',
                    'Study user interface and experience design',
                    'Practice creative problem-solving techniques',
                    'Build projects that showcase innovation'
                ],
                'personality_strengths': [
                    'Innovative thinking leads to unique solutions',
                    'Adaptability helps in learning new technologies',
                    'Creative approach makes code more engaging'
                ],
                'growth_opportunities': [
                    'Focus on code efficiency and optimization',
                    'Learn systematic debugging approaches',
                    'Practice following established patterns and conventions'
                ]
            },
            'practical': {
                'personalized_feedback': 'Focus on code maintainability, best practices, and real-world applicability.',
                'learning_path_suggestions': [
                    'Study software engineering best practices',
                    'Learn design patterns and architectural principles',
                    'Practice test-driven development',
                    'Focus on scalable and maintainable code'
                ],
                'personality_strengths': [
                    'Focus on best practices ensures quality code',
                    'Practical mindset leads to usable solutions',
                    'Systematic approach aids in project management'
                ],
                'growth_opportunities': [
                    'Explore innovative and creative approaches',
                    'Study theoretical computer science concepts',
                    'Practice thinking outside conventional solutions'
                ]
            },
            'collaborative': {
                'personalized_feedback': 'Focus on code readability, documentation, and team collaboration aspects.',
                'learning_path_suggestions': [
                    'Practice code review and pair programming',
                    'Learn technical communication skills',
                    'Study open source contribution practices',
                    'Focus on mentoring and knowledge sharing'
                ],
                'personality_strengths': [
                    'Strong communication aids in team development',
                    'Collaborative mindset improves code quality',
                    'Teaching others reinforces your own learning'
                ],
                'growth_opportunities': [
                    'Develop independent problem-solving skills',
                    'Practice deep technical analysis',
                    'Focus on individual coding challenges'
                ]
            }
        }
        
        base_insights = fallback_insights.get(personality_type, fallback_insights['practical'])
        base_insights.update({
            'personality_type': personality_type,
            'recommended_resources': [
                {
                    'title': f'{personality_data["name"]} Learning Path',
                    'type': 'course',
                    'reason': f'Designed for {personality_data["learning_style"]} learners',
                    'difficulty': 'intermediate'
                }
            ],
            'practice_problems': [
                {
                    'title': 'Personality-matched coding challenges',
                    'difficulty': 'medium',
                    'reason': f'Suits {personality_data["learning_style"]} approach',
                    'focus_area': ', '.join(personality_data['focus_areas'][:2])
                }
            ],
            'collaboration_tips': ['Share your solutions with the community', 'Seek feedback from peers'],
            'motivation_boosters': [f'Your {personality_data["name"]} approach is valuable in software development'],
            'learning_strategies': [f'Use {personality_data["learning_style"]} methods for best results']
        })
        
        return base_insights

    def _merge_analyses(self, traditional: Dict[str, Any], llm: Dict[str, Any]) -> Dict[str, Any]:
        """Merge traditional and LLM analyses into a comprehensive result."""
        merged = traditional.copy()
        
        # Add LLM-specific insights
        merged['llm_analysis'] = llm
        
        # Enhance existing fields with LLM insights
        if 'algorithm_explanation' in llm:
            merged['enhanced_algorithm_explanation'] = llm['algorithm_explanation']
        
        if 'optimization_suggestions' in llm:
            merged['optimization_suggestions'] = llm['optimization_suggestions']
        
        if 'learning_concepts' in llm:
            merged['learning_concepts'] = llm['learning_concepts']
        
        # Add educational value
        merged['educational_insights'] = {
            'interview_tips': llm.get('interview_tips', []),
            'related_problems': llm.get('related_problems', []),
            'conceptual_gaps': llm.get('conceptual_gaps', []),
            'positive_aspects': llm.get('positive_aspects', [])
        }
        
        return merged

    def get_educational_summary(self, analysis: Dict[str, Any]) -> str:
        """Generate a human-readable educational summary."""
        if 'llm_analysis' not in analysis:
            return "No LLM analysis available."
        
        llm_data = analysis['llm_analysis']
        
        summary = []
        summary.append("🎯 **Algorithm Analysis:**")
        summary.append(f"   {llm_data.get('algorithm_explanation', 'No explanation available')}")
        
        if llm_data.get('positive_aspects'):
            summary.append("\n✅ **What you did well:**")
            for aspect in llm_data['positive_aspects']:
                summary.append(f"   • {aspect}")
        
        if llm_data.get('optimization_suggestions'):
            summary.append("\n🚀 **Optimization suggestions:**")
            for suggestion in llm_data['optimization_suggestions']:
                summary.append(f"   • {suggestion}")
        
        if llm_data.get('learning_concepts'):
            summary.append("\n📚 **Key concepts to understand:**")
            for concept in llm_data['learning_concepts']:
                summary.append(f"   • {concept}")
        
        if llm_data.get('interview_tips'):
            summary.append("\n💼 **Interview tips:**")
            for tip in llm_data['interview_tips']:
                summary.append(f"   • {tip}")
        
        return "\n".join(summary)

    def get_personality_summary(self, analysis: Dict[str, Any]) -> str:
        """Generate a human-readable personality-based summary."""
        if 'personality_insights' not in analysis:
            return "No personality insights available."
        
        personality_data = analysis['personality_insights']
        personality_type = personality_data.get('personality_type', 'unknown')
        
        if personality_type in self.personality_types:
            type_info = self.personality_types[personality_type]
            type_name = type_info['name']
            type_icon = '🧠' if personality_type == 'analytical' else '🎨' if personality_type == 'creative' else '🔧' if personality_type == 'practical' else '🤝'
        else:
            type_name = 'Unknown Type'
            type_icon = '❓'
        
        summary = []
        summary.append(f"{type_icon} **Personalized Feedback for {type_name}:**")
        summary.append(f"   {personality_data.get('personalized_feedback', 'No personalized feedback available')}")
        
        if personality_data.get('personality_strengths'):
            summary.append(f"\n💪 **Your {type_name} Strengths:**")
            for strength in personality_data['personality_strengths']:
                summary.append(f"   • {strength}")
        
        if personality_data.get('learning_path_suggestions'):
            summary.append(f"\n🎯 **Recommended Learning Path:**")
            for suggestion in personality_data['learning_path_suggestions']:
                summary.append(f"   • {suggestion}")
        
        if personality_data.get('growth_opportunities'):
            summary.append(f"\n🌱 **Growth Opportunities:**")
            for opportunity in personality_data['growth_opportunities']:
                summary.append(f"   • {opportunity}")
        
        if personality_data.get('motivation_boosters'):
            summary.append(f"\n🚀 **Motivation Boosters:**")
            for booster in personality_data['motivation_boosters']:
                summary.append(f"   • {booster}")
        
        if personality_data.get('learning_strategies'):
            summary.append(f"\n📖 **Learning Strategies for You:**")
            for strategy in personality_data['learning_strategies']:
                summary.append(f"   • {strategy}")
        
        return "\n".join(summary)

    def get_comprehensive_summary(self, analysis: Dict[str, Any]) -> str:
        """Generate a comprehensive summary including both technical and personality insights."""
        technical_summary = self.get_educational_summary(analysis)
        personality_summary = self.get_personality_summary(analysis)
        
        if personality_summary == "No personality insights available.":
            return technical_summary
        
        return f"{technical_summary}\n\n{personality_summary}"

    def analyze_and_explain(self, code: str, language: str, personality_type: Optional[str] = None) -> str:
        """Analyze code and return a comprehensive educational explanation."""
        if personality_type:
            analysis = self.analyze_with_personality(code, language, personality_type)
            return self.get_comprehensive_summary(analysis)
        else:
            analysis = self.analyze_code_with_llm(code, language)
            return self.get_educational_summary(analysis)

    def get_personality_types(self) -> Dict[str, Dict[str, Any]]:
        """Get all available personality types and their descriptions."""
        return self.personality_types.copy()

    def assess_personality_from_code(self, code: str, language: str) -> Dict[str, Any]:
        """Attempt to assess personality traits from code style and approach."""
        if not self.use_llm:
            return {'error': 'LLM not available for personality assessment'}
        
        prompt = f"""
Analyze the following {language} code and assess the programmer's likely personality traits based on their coding style, approach, and choices.

```{language}
{code}
```

Based on the code style, variable naming, approach to problem-solving, and overall structure, provide a JSON assessment:

{{
"likely_personality_traits": {{
    "analytical": 0-10,
    "creative": 0-10,
    "practical": 0-10,
    "collaborative": 0-10
}},
"reasoning": "explanation of why you assigned these scores",
"dominant_trait": "most likely personality type",
"code_style_indicators": ["specific aspects of the code that indicate personality"],
"recommendations": ["suggestions based on inferred personality"]
}}
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=1000,
                    temperature=0.3,
                )
            )
            
            # Parse response
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            return json.loads(response_text)
        except Exception as e:
            print(f"Personality assessment from code failed: {e}")
            return {'error': f'Assessment failed: {str(e)}'}