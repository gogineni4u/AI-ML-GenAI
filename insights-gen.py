import json
import google.generativeai as genai

def get_insights_from_gemini(file_path, api_key):
    """Fetches insights from Gemini Pro based on the given JSON data.

    Args:
        file_path (str): The path to the JSON file containing the data.
        api_key (str): Your Gemini Pro API key.

    Returns:
        str: The insights generated by Gemini Pro.
    """

    try:
        # Load the JSON data
        with open(file_path, "r") as file:
            data = json.load(file)

        # Set your API key
        genai.configure(api_key=api_key)

        # Define the model to use
        model = genai.GenerativeModel(model_name='models/gemini-pro')

        # Prompt for Gemini Pro
        prompt_template = """
        Analyze the following JSON data containing customer interaction records and provide insights on:
        - Top 3 customer issues categorized by type (billing, account, device, network, etc.)
        - The most frequent issues across all categories
        - Average resolution time per issue type (if available)
        - Any other noteworthy trends or patterns

        Here's the JSON data:

        ```
        {data_json}
        ```
        """

        # Prepare the prompt by formatting the data
        prompt = prompt_template.format(data_json=json.dumps(data))

        # Generate a response from the model
        response = model.generate_text(
            prompt=prompt,
            temperature=0.5,
            max_output_tokens=500
        )

        # Extract the insights from the response
        insights = response.candidates[0].output

        return insights

    except FileNotFoundError:
        return "Error: JSON file not found at the specified path."
    except json.JSONDecodeError:
        return "Error: Invalid JSON format in the file."
    except genai.GenerativeAIError as e:
        return f"Error communicating with Gemini Pro API: {e}"


# Example Usage (replace with your actual API key and file path)
api_key = "AIzaSyDMtJU3t2Ss7XaNZOHtpBt4LfiuXX1kBZk"
file_path = "R:\\Learning\\Python\\Python-WS\\my-python-project\\venv\\merged_insights_data.json"

insights = get_insights_from_gemini("file_path, api_key")
print("Insights from Gemini Pro:\n\n", insights)
