def score_calculator(task_category, industry_category, skills_category):
    """
    Calculates the AI risk score based on task, industry, and skills categories.
    
    Parameters:
    - task_category (list of str)
    - industry_category (str)
    - skills_category (list of str)
    
    Returns:
    - final_score (int): Clamped score between 0 and 100
    - risk_level (str)
    - interpretation (str)
    """

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

    # Add task score
    score += task_scores.get(task_category, 0)

    # Add industry score
    score += industry_scores.get(industry_category, 0)

    # Add all skills scores
    for skill in skills_category:
        score += skills_scores.get(skill, 0)

    # Clamp between 0 and 100
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
