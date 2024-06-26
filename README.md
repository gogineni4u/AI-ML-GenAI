# Call Center Agent Activity Summarization and Insight Generation

This project aims to provide a comprehensive summary of a call center agent's daily activities, leveraging data from multiple sources. By combining insights from SiteCatalyst, Kibana logs, and CCAI call transcripts, we're building a tool that helps analyze and understand agent performance, customer interactions, and operational efficiency.

## Project Overview

The core goal of this project is to streamline and enhance the understanding of a call center agent's workday. By analyzing:

- **SiteCatalyst Data:** We capture agent interactions with web pages, providing insights into their navigation patterns and usage of the customer service portal.
- **Kibana Logs:** We examine API calls made by agents during customer interactions. This reveals the actions taken in the backend systems to resolve issues or complete tasks.
- **CCAI Call Transcripts:** We delve into the content of conversations between agents and customers, uncovering the types of issues raised, problem-solving approaches, and overall customer sentiment.

By integrating these diverse data sources, we aim to:

- **Identify patterns in customer issues:** Determine the most common problems, their frequencies, and potential correlations with specific actions or pages.
- **Assess agent performance:** Evaluate agent efficiency, identify areas where they excel, and pinpoint areas for improvement.
- **Optimize workflows:** Discover bottlenecks in processes, uncover knowledge gaps, and suggest ways to enhance customer support efficiency.

## Data Generation

This project includes a script (`Dataset.py`) that generates synthetic data to simulate real-world call center interactions. This data includes:

- **Kibana Logs:** Simulated API call logs with timestamps, agent IDs, customer IDs, endpoints, actions, and statuses.
- **SiteCatalyst Data:** Simulated web page interaction data with timestamps, agent IDs, customer IDs, page names, URLs, and time spent on pages.
- **CCAI Transcripts:** Simulated call transcripts with timestamps, agent IDs, customer IDs, and detailed conversations.

The data generation process includes:

- Random timestamp generation to simulate activity within a defined timeframe.
- Random selection of API endpoints and web pages based on predefined dictionaries.
- Realistic conversation generation for CCAI transcripts.

## Data Processing and Analysis

The generated data is processed using Pandas DataFrames. The script performs the following steps:

1. **Data Loading:** The generated Kibana and SiteCatalyst data are loaded into separate DataFrames.
2. **Data Cleaning and Preparation:** Data is cleaned (e.g., removing invalid characters), and timestamps are converted to the correct format for further analysis.
3. **Merging Data:** The Kibana and SiteCatalyst DataFrames are merged into a unified dataset based on timestamp and customer ID.
4. **CCAI Transcript Generation:** CCAI transcripts are generated for each interaction and added to the merged DataFrame.
5. **Insight Generation:** We utilize Gemini Pro to analyze the merged dataset. By providing carefully crafted prompts to the model, we extract valuable insights like the top customer issues, common problems, and potential areas for process improvement.

## Code Files

Following are the code files for the above PoC"

1. **Dataset.py** Main python code for inititing, cleansing and aggregating the Kibana API calls, SiteCatalyst Data and CCAI transcripts.
2. **insights-gen.py:** The actual promting to Gemini Pro LLM to generate the insights from our aggregated dataset. This leverages Google Gemini API Key (used my personal account for this)
3. **kibana_agent_data (csv & json):** Generated Kibana API calls data set
4. **sitecatalyst_agent_data (csv & json):** Generated SiteCatalyst dataset based on sample agent interactions
5. **merged_agent_data (csv & json):** Aggregated dataset without CCAI data
6. **merged_insights_data (csv & json):** Aggregated dataset with CCAI data
7. **text_data_for_llm (Text file):** This is just the aggregated data in text format, as LLM's take plain text input for prompting.

Once Datset.py gets executed all the data sets will be generated.
Next insights-gen.py should be executed which inturn prompts Gemini Pro LLM via API. The aggregated dataset will be fed via file path.
Insights like the top customer issues, common problems, and potential areas for process improvement.
