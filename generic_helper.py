import re


def extract_session_id(query_result):

    output_contexts = query_result.get("outputContexts", [])

    if not output_contexts:
        return None

    context_name = output_contexts[0]["name"]

    match = re.search(
        r"/sessions/(.*?)/contexts/",
        context_name
    )

    if match:
        return match.group(1)

    return None


def get_str_from_food_dict(food_dict):

    return ", ".join(
        [f"{qty} {item}" for item, qty in food_dict.items()]
    )