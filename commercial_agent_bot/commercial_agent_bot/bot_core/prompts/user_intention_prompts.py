class UserIntentionPrompts:
    GOAL = "Analyze the following user message to identify their intents."
    RETURN_FORMAT = "JSON"
    WARNINGS = "Important: ONLY return the JSON object. Do not include any other text, explanations, or markdown formatting before or after the JSON."
    CONTEXT_DUMP = """
            Analyze the following user message to identify their intents.
            User message: "{customer_message}"

            Your response MUST be a single JSON object with the exact following structure:
            {{
            "intents": [
                {{
                "type": "string (must be one of: {intent_types})",
                "attributes": ["string"],
                "entities": {{ "key": "value" }},
                "missing_info": ["string"],
                "details": "any (can be a string, number, boolean, list, or a nested JSON object/null)"
                }}
                // ... more intents if identified
            ]
            }}

            Take in count each intent: {intent_types}

            - For each identified intent in the "intents" list:
            - "attributes": Extract key phrases or words from the user message that relate to this intent. For example, if the user is asking about a car, the attributes should be the car model, year, price an so on.
            - "entities": Extract specific entities relevant to the intent. For example, if the user is asking about a car, for car recommendation the entities should be the kilometers,price_min,price_max,brand,model,year_min,year_max,version,measures,features (bluetooth,car_play,etc) if apply at least one of these attributes try not to return empty values.
            - "missing_info": If the user's message for this intent is incomplete and requires more information to be processed by a specialized agent later, list the questions that need to be asked. If no info is missing, provide an empty list [].
            - "details": Provide any other relevant information or context extracted for this specific intent. Can be a simple string, or a more complex JSON object if applicable. Use null if no specific details.

            Example of a user message: "Hola, quiero información sobre el KAVAK_MODEL_X y si tienen planes de financiamiento."
            Example of the EXACT JSON structure you should return for that message (remember to use the actual tracking_id provided above):
            {json_example}

            Important: ONLY return the JSON object. Do not include any other text, explanations, or markdown formatting before or after the JSON.
      """

    INTENT_TYPES = {
            "car_recommendation":"if the user needs to compare cars, doesn't know exactly which car they want, or needs help choosing a car according to the price, the user could ask for an attribute of the car for example 'Tengo N pesos para qué auto me alcanza'",
            "financing_info":"if the user needs information about financing plans, credits, etc.",
            "greetings":"if the user says hello, good afternoon, etc.",
            "general_info":"if the user needs information about Kavak, its history, mission, values, addresses, this intent is for general purpose etc.",
            "sales_agent":"convince customers to use kavak, this intent is for sales purposes"
            }
    
    example_json_structure = {
            "intents": [
                {
                    "type": "financing_info",
                    "attributes": ["planes financieros", "información"],
                    "entities": {"topic": "financial plans"},
                    "missing_info": [],
                    "details": {"notes": "User is asking for general information about financial plans."}
                },
                {
                    "type": "car_recommendation",
                    "attributes": ["información", "presupuesto"],
                    "entities": {"price_min": "200000", "price_max": "300000", "features": ["bluetooth, car_play"], "year_min": "2015", "year_max": "2020"},
                    "missing_info": [],
                    "details": {"notes": "User is asking for a car recommendation according to their price."}
                },
            ]
        }