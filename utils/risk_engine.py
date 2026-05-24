def calculate_stage(risk):

    if risk < 25:

        return (
            "Stage 1",
            "Low",
            "Early"
        )

    elif risk < 50:

        return (
            "Stage 2",
            "Moderate",
            "Intermediate"
        )

    elif risk < 75:

        return (
            "Stage 3",
            "High",
            "Advanced"
        )

    else:

        return (
            "Stage 4",
            "Critical",
            "Severe"
        )