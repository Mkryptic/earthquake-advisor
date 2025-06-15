import json
import random
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class SimulationResult:
    scenario_id: str
    user_choices: List[str]
    total_score: int
    max_score: int
    performance_level: str
    feedback: List[str]
    lessons_learned: List[str]

class ScenarioEngine:
    def __init__(self, scenarios_file: str = "data/scenarios.json"):
        self.scenarios = self._load_scenarios(scenarios_file)
        self.current_scenario = None
        self.user_choices = []
        self.score = 0
        self.max_score = 0
        self.feedback = []
    
    def _load_scenarios(self, file_path: str) -> Dict:
        """Load scenarios from JSON file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            return {"scenarios": []}
    
    def get_available_scenarios(self) -> List[Dict]:
        """Get list of available scenarios"""
        return [
            {
                "id": scenario["id"],
                "title": scenario["title"],
                "description": scenario["description"],
                "location": scenario.get("location", "unknown"),
                "difficulty": self._calculate_difficulty(scenario)
            }
            for scenario in self.scenarios.get("scenarios", [])
        ]
    
    def _calculate_difficulty(self, scenario: Dict) -> str:
        """Calculate scenario difficulty based on choices and complexity"""
        num_choices = len(scenario.get("choices", []))
        has_follow_up = "follow_up" in scenario
        
        if num_choices <= 2 and not has_follow_up:
            return "beginner"
        elif num_choices <= 3 or has_follow_up:
            return "intermediate"
        else:
            return "advanced"
    
    def start_scenario(self, scenario_id: str) -> Dict:
        """Start a specific scenario"""
        scenario = self._find_scenario(scenario_id)
        if not scenario:
            return {"error": "Scenario not found"}
        
        self.current_scenario = scenario
        self.user_choices = []
        self.score = 0
        self.max_score = 0
        self.feedback = []
        
        # Calculate max possible score
        for choice in scenario.get("choices", []):
            self.max_score += choice.get("score", 0)
        
        if "follow_up_choices" in scenario:
            for choice in scenario.get("follow_up_choices", []):
                self.max_score += choice.get("score", 0)
        
        return {
            "scenario": {
                "id": scenario["id"],
                "title": scenario["title"],
                "description": scenario["description"],
                "location": scenario.get("location"),
                "magnitude": scenario.get("magnitude"),
                "time": scenario.get("time")
            },
            "choices": [
                {
                    "id": choice["id"],
                    "text": choice["text"]
                }
                for choice in scenario.get("choices", [])
            ]
        }
    
    def _find_scenario(self, scenario_id: str) -> Optional[Dict]:
        """Find scenario by ID"""
        for scenario in self.scenarios.get("scenarios", []):
            if scenario["id"] == scenario_id:
                return scenario
        return None
    
    def submit_choice(self, choice_id: str) -> Dict:
        """Submit a choice for the current scenario"""
        if not self.current_scenario:
            return {"error": "No active scenario"}
        
        # Find the choice in current scenario
        choice = self._find_choice(choice_id)
        if not choice:
            return {"error": "Choice not found"}
        
        self.user_choices.append(choice_id)
        self.score += choice.get("score", 0)
        self.feedback.append(choice.get("explanation", ""))
        
        # Check if there's a follow-up question
        if "follow_up" in self.current_scenario and len(self.user_choices) == 1:
            return {
                "choice_result": {
                    "correct": choice.get("correct", False),
                    "explanation": choice.get("explanation", ""),
                    "score": choice.get("score", 0)
                },
                "follow_up": {
                    "question": self.current_scenario["follow_up"],
                    "choices": [
                        {
                            "id": follow_choice["id"],
                            "text": follow_choice["text"]
                        }
                        for follow_choice in self.current_scenario.get("follow_up_choices", [])
                    ]
                }
            }
        else:
            # Scenario complete
            return self._complete_scenario()
    
    def _find_choice(self, choice_id: str) -> Optional[Dict]:
        """Find choice by ID in current scenario"""
        if not self.current_scenario:
            return None
        
        # Check main choices
        for choice in self.current_scenario.get("choices", []):
            if choice["id"] == choice_id:
                return choice
        
        # Check follow-up choices
        for choice in self.current_scenario.get("follow_up_choices", []):
            if choice["id"] == choice_id:
                return choice
        
        return None
    
    def _complete_scenario(self) -> Dict:
        """Complete the current scenario and return results"""
        if not self.current_scenario:
            return {"error": "No active scenario"}
        
        # Calculate performance level
        score_percentage = (self.score / self.max_score) * 100 if self.max_score > 0 else 0
        performance_level = self._get_performance_level(score_percentage)
        
        # Generate lessons learned
        lessons = self._generate_lessons_learned()
        
        result = SimulationResult(
            scenario_id=self.current_scenario["id"],
            user_choices=self.user_choices.copy(),
            total_score=self.score,
            max_score=self.max_score,
            performance_level=performance_level,
            feedback=self.feedback.copy(),
            lessons_learned=lessons
        )
        
        # Reset for next scenario
        self.current_scenario = None
        self.user_choices = []
        self.score = 0
        self.max_score = 0
        self.feedback = []
        
        return {
            "scenario_complete": True,
            "results": {
                "score": result.total_score,
                "max_score": result.max_score,
                "percentage": score_percentage,
                "performance": result.performance_level,
                "feedback": result.feedback,
                "lessons_learned": result.lessons_learned
            }
        }
    
    def _get_performance_level(self, score_percentage: float) -> str:
        """Get performance level based on score"""
        scoring = self.scenarios.get("scoring", {})
        
        if score_percentage >= scoring.get("excellent", {}).get("min_score", 90):
            return "excellent"
        elif score_percentage >= scoring.get("good", {}).get("min_score", 70):
            return "good"
        elif score_percentage >= scoring.get("needs_improvement", {}).get("min_score", 50):
            return "needs_improvement"
        else:
            return "dangerous"
    
    def _generate_lessons_learned(self) -> List[str]:
        """Generate lessons based on the scenario and choices made"""
        lessons = []
        
        if self.current_scenario:
            scenario_type = self.current_scenario.get("location", "general")
            
            if scenario_type == "apartment":
                lessons.extend([
                    "🏠 Keep emergency supplies in your bedroom for nighttime earthquakes",
                    "🔦 Have a flashlight and sturdy shoes beside your bed",
                    "📋 Practice Drop, Cover, Hold On from your bed"
                ])
            elif scenario_type == "office":
                lessons.extend([
                    "🏢 Know your building's evacuation routes",
                    "🚪 Never use elevators during or after an earthquake",
                    "👥 Help colleagues but don't endanger yourself"
                ])
            elif scenario_type == "school":
                lessons.extend([
                    "🏫 Schools should practice earthquake drills regularly",
                    "📚 Take cover under desks, away from windows",
                    "👨‍🏫 Teachers: Stay calm and give clear directions"
                ])
            elif scenario_type == "mall":
                lessons.extend([
                    "🏬 In crowded places, avoid panic and stampedes",
                    "🚪 Know multiple exit routes",
                    "🛍️ Don't stop to collect belongings during evacuation"
                ])
            
            # Add general lessons
            lessons.extend([
                "⚡ Remember: DROP, COVER, HOLD ON is the universal response",
                "📱 Have emergency contacts saved in your phone",
                "🎒 Prepare an emergency kit for your home and workplace"
            ])
        
        return lessons
    
    def get_random_scenario(self) -> Dict:
        """Get a random scenario for quick practice"""
        scenarios = self.scenarios.get("scenarios", [])
        if not scenarios:
            return {"error": "No scenarios available"}
        
        random_scenario = random.choice(scenarios)
        return self.start_scenario(random_scenario["id"])
    
    def get_scenario_by_location(self, location: str) -> Dict:
        """Get a scenario for a specific location"""
        matching_scenarios = [
            scenario for scenario in self.scenarios.get("scenarios", [])
            if scenario.get("location", "").lower() == location.lower()
        ]
        
        if not matching_scenarios:
            return {"error": f"No scenarios available for location: {location}"}
        
        scenario = random.choice(matching_scenarios)
        return self.start_scenario(scenario["id"])

# Global scenario engine instance
scenario_engine = ScenarioEngine() 