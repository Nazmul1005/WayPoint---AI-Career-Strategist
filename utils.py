"""
Utility functions for WayPoint AI Career Strategist
"""
import random
from typing import List, Dict, Optional
from config import TECH_STACKS, RESOURCES, GUARDRAILS
from prompts import PERSONA_KEYWORDS, VALIDATION_STATEMENTS, OUT_OF_SCOPE_RESPONSES


def detect_persona(user_input: str) -> Optional[str]:

    user_input_lower = user_input.lower()
    
    scores = {
        "student": 0,
        "mid_career": 0,
        "pivot_seeker": 0
    }
    
    for persona, keywords in PERSONA_KEYWORDS.items():
        for keyword in keywords:
            if keyword in user_input_lower:
                scores[persona] += 1
    
    max_score = max(scores.values())
    if max_score == 0:
        return None
    
    return max(scores, key=scores.get)


def check_guardrails(user_input: str) -> Optional[Dict[str, str]]:

    user_input_lower = user_input.lower()
    
    for keyword in GUARDRAILS["legal_keywords"]:
        if keyword in user_input_lower:
            return {"type": "legal", "topic": keyword}
    
    for keyword in GUARDRAILS["medical_keywords"]:
        if keyword in user_input_lower:
            return {"type": "medical", "topic": keyword}
    
    for keyword in GUARDRAILS["unethical_keywords"]:
        if keyword in user_input_lower:
            return {"type": "unethical", "topic": keyword}
    
    return None


def get_validation_statement() -> str:
 
    return random.choice(VALIDATION_STATEMENTS)


def get_tech_recommendations(area: str) -> List[str]:
 
    return TECH_STACKS.get(area, [])


def get_learning_resources(category: str) -> List[str]:
 
    return RESOURCES.get(category, [])


def format_tech_stack_response(areas: List[str]) -> str:
 
    output = []
    
    area_names = {
        "web_frontend": "Frontend Development",
        "web_backend": "Backend Development",
        "data_ai": "Data Science & AI",
        "mobile": "Mobile Development",
        "devops": "DevOps & Cloud",
        "tools": "Essential Tools"
    }
    
    for area in areas:
        if area in TECH_STACKS:
            output.append(f"**{area_names.get(area, area)}:** {', '.join(TECH_STACKS[area])}")
    
    return "\n".join(output)


def format_milestone_list(milestones: List[str]) -> str:
 
    return "\n".join([f"{i+1}. **{milestone}**" for i, milestone in enumerate(milestones)])


def is_vague_query(user_input: str) -> bool:
 
    vague_patterns = [
        "i want a job",
        "i want to work",
        "get a remote job",
        "find a job",
        "career advice",
        "help me",
        "what should i do",
        "i'm lost",
        "need guidance"
    ]
    
    user_input_lower = user_input.lower()
    
    # Check if input is very short (likely vague)
    if len(user_input.split()) < 10:
        for pattern in vague_patterns:
            if pattern in user_input_lower:
                return True
    
    return False


def extract_context_from_history(conversation_history: List[Dict]) -> Dict[str, any]:
 
    context = {
        "mentioned_skills": [],
        "mentioned_technologies": [],
        "career_goals": [],
        "constraints": []
    }
    
    # Flatten all tech stacks for searching
    all_techs = []
    for tech_list in TECH_STACKS.values():
        all_techs.extend([tech.lower() for tech in tech_list])
    
    # Search through conversation history
    for message in conversation_history:
        content = message.get("content", "").lower()
        
        # Look for mentioned technologies
        for tech in all_techs:
            if tech.lower() in content and tech not in context["mentioned_technologies"]:
                context["mentioned_technologies"].append(tech)
        
        # Look for career goals indicators
        if any(word in content for word in ["want to", "goal", "aim", "hoping to"]):
            context["career_goals"].append(message.get("content", ""))
    
    return context


def create_out_of_scope_response(guardrail_result: Dict[str, str]) -> str:
  
    response_type = guardrail_result["type"]
    topic = guardrail_result["topic"]
    
    template = OUT_OF_SCOPE_RESPONSES.get(response_type, "")
    return template.format(topic=topic)
