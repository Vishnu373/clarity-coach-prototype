def get_score_evaluators(score_evaluation):
    tasks_category = score_evaluation["task_modifier"]
    industry_category = score_evaluation["industry_risk_adjustment"]
    skills_category = score_evaluation["skill_modifier"]

    return tasks_category, industry_category, skills_category

def score_calculator(tasks_category, industry_category, skills_category):
    # Base IMF value
    score = 40

    # Task category scores
    task_scores = {
        'Routine Tasks': 30,
        'Creative Tasks': -10,
        'Hybrid AI Collaboration': -50
    }

    # Industry category scores
    industry_scores = {
        'High-Risk': 20,
        'Medium-Risk': 0,
        'Low-Risk': -15
    }

    # Skills category scores
    skills_scores = {
        'Routine Physical': 20,
        'Routine Cognitive': 15,
        'Creative Problem Solving': -20,
        'Emotional Intelligence': -25,
        'AI Collaboration': -30
    }

    for task in tasks_category:
        score += task_scores.get(task, 0)

    score += industry_scores.get(industry_category, 0)

    for skill in skills_category:
        score += skills_scores.get(skill, 0)

    final_score = max(0, min(100, score))

    # Determine risk level and interpretation
    if 0 <= final_score <= 20:
        risk_level = "Very Low Risk"
        interpretation = "Strong AI resilience. Task mix supports long-term role security."

    elif 21 <= final_score <= 40:
        risk_level = "Low Risk"
        interpretation = "Minor exposure. Upskill in creative/hybrid areas for full insulation."
    
    elif 41 <= final_score <= 60:
        risk_level = "Moderate Risk"
        interpretation = "Near global average. AI may partially automate current workload."
    
    elif 61 <= final_score <= 80:
        risk_level = "High Risk"
        interpretation = "Likely AI disruption. Begin strategic adaptation planning."
    
    elif 81 <= final_score <= 100:
        risk_level = "Very High Risk"
        interpretation = "High automation potential. Pivot or integrate hybrid skills urgently."

    return final_score, risk_level, interpretation
