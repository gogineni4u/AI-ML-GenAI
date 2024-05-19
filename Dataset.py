import csv
import json
import random
import datetime
import argparse
import pandas as pd

# Configuration
num_records = 500
# Configuration
num_agents = 20  # Limit the number of total agents to 20
agents = ["agent" + str(i).zfill(2) for i in range(1, num_agents + 1)]  # Generate a pool of agent IDs
customer_ids = [str(i).zfill(5) for i in range(10000, 10000 + num_records)]  # Generate customer IDs based on the number of records

api_endpoints = {
    "Billing": ["invoices", "payment", "update/address", "dispute", "add/paymentmethod", "remove/paymentmethod",
                "add/roamingpackage", "payment/history/download", "downloadstatements", "scheduleautopay", "refund"],
    "Account": ["update/profile", "reset/password", "update/notifications", "update/security", "close", "addnote",
                "update/email", "password/reset", "updatesecurityquestions", "activate", "addline",
                "activate/internationalcalling", "update/language"],
    "Device": ["activate", "update/firmware", "reboot", "reset", "update/datalimit", "configure", "replacement/request",
               "fileclaim", "upgrade", "checkcompatibility"],
    "Network": ["troubleshoot/signal", "status", "speedtest", "diagnostics", "optimize", "outage/report",
                "update/wifi-password", "updateqos", "troubleshooting", "issueresolved", "outage/status"],
    "Plans & Perks": ["plans/compare", "perks/redeem", "plans/features"],
    "Upgrades": ["upgrade/device", "upgrade/plan", "upgrade/checkEligibility"]
}

sitecatalyst_pages = {
    "Billing": ["Customer Dashboard", "Billing Details", "Payment History", "Invoice Details", "Dispute Charge",
                "Payment Options", "International Roaming Charges"],
    "Account": ["Account Overview", "Update Contact Information", "Notification Settings", "Account Security",
                "Account Closure", "Device Replacement Options"],
    "Device": ["Device Details", "Troubleshooting Guide", "Firmware Update", "Device Reset", "Device Usage",
               "Phone Upgrade Options", "Device Compatibility List"],
    "Network": ["Network Diagnostics", "Speed Test Results", "Coverage Map", "Network Optimization Settings",
                "Network Usage History", "Network Troubleshooting Tips"],
    "Plans & Perks": ["Compare Plans", "Redeem Perks", "Plan Features"],
    "Upgrades": ["Upgrade Device", "Upgrade Plan", "Eligibility Check"]
}

# Function to generate a random timestamp between two dates
def generate_timestamp(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_datetime = start_date + datetime.timedelta(days=random_number_of_days)
    return random_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

# Set start and end dates for timestamps (adjust as needed)
start_date = datetime.datetime(2024, 5, 18, 9, 0, 0)
end_date = datetime.datetime(2024, 5, 19, 17, 0, 0)

# Data Generation Functions

def generate_kibana_record():
    timestamp = generate_timestamp(start_date, end_date)
    log_level = random.choice(["INFO", "WARN", "ERROR", "DEBUG"])
    category = random.choice(list(api_endpoints.keys()))
    endpoint = f"/api/{category.lower()}/{random.choice(api_endpoints[category])}/{random.randint(10000, 99999)}"
    user_id = random.choice(agents)
    customer_id = customer_ids.pop(0)  # Ensure unique customer IDs
    response_code = random.choice([200, 400, 401, 403, 500, 503])
    status = "success" if response_code == 200 else "failed"
    response_time = random.randint(50, 500)

    # Generate action and button based on api_endpoint
    if "billing" in endpoint.lower():
        action = random.choice(["fetched invoice", "processed payment", "updated billing address", "initiated dispute",
                                "added payment method", "removed payment method", "added roaming package",
                                "downloaded payment history", "downloaded billing statements", "scheduled autopay",
                                "processed refund"])
        button_name = None if action.startswith("fetched") else action.replace(" ", "_")
    elif "account" in endpoint.lower():
        action = random.choice(
            ["updated profile", "reset password", "updated notification preferences", "updated security settings",
             "closed account", "added account note", "updated email address", "initiated password reset",
             "updated security questions", "activated account", "added new line", "activated international calling",
             "updated language"])
        button_name = None if action.startswith("updated") or action.startswith("closed") or action.startswith(
            "added") else action.replace(" ", "_")
    elif "device" in endpoint.lower():
        action = random.choice(
            ["activated device", "updated firmware", "rebooted device", "reset device", "updated data limit",
             "configured device", "requested device replacement", "filed device claim", "upgraded device",
             "checked device compatibility"])
        button_name = None if action.startswith("updated") or action.startswith("configured") or action.startswith(
            "checked") else action.replace(" ", "_")
    elif "network" in endpoint.lower():
        action = random.choice(
            ["troubleshot signal", "checked network status", "ran speed test", "ran network diagnostics",
             "optimized network settings", "reported outage", "updated Wi-Fi password", "adjusted QoS settings",
             "viewed troubleshooting guide", "resolved network issue", "checked outage status"])
        button_name = None if action.startswith("checked") or action.startswith("viewed") or action.startswith(
            "troubleshot") else action.replace(" ", "_")
    elif "plans" in endpoint.lower():
        action = random.choice(["compared plans", "viewed plan features"])
        button_name = None
    elif "perks" in endpoint.lower():
        action = "redeemed perks"
        button_name = None
    else:  # Upgrades
        action = random.choice(["initiated upgrade", "completed upgrade", "checked upgrade eligibility"])
        button_name = None if action.startswith("checked") else action.replace(" ", "_")

    message = f"Agent {user_id} {action} for customer {customer_id}."

    return [timestamp, message, "api_call", button_name, customer_id, endpoint, status, response_time]

def generate_sitecatalyst_record(customer_id, agent_id, kibana_timestamp):
    # Use the Kibana timestamp as a base
    hit_time_gmt = (datetime.datetime.strptime(kibana_timestamp, "%Y-%m-%dT%H:%M:%SZ") - datetime.timedelta(seconds=random.randint(1, 60))).strftime("%Y-%m-%dT%H:%M:%SZ")

    visid_high = random.randint(1000000000, 9999999999)
    visid_low = random.randint(1000000000, 9999999999)
    visit_num = random.randint(1, 5)
    category = random.choice(list(sitecatalyst_pages.keys()))
    page_name = random.choice(sitecatalyst_pages[category])
    page_url = f"/{category.lower()}/{page_name.replace(' ', '-')}/{customer_id}"
    event_list = random.choice(["", "1"])
    events = f"event{random.randint(1, 10)}" if event_list == "1" else ""
    time_spent = random.randint(30, 300)  # Generate a random time spent between 30 to 300 seconds

    return [
        hit_time_gmt,  # Use calculated timestamp instead of current time
        visid_high,
        visid_low,
        visit_num,
        page_name,
        page_url,
        event_list,
        events,
        agent_id,
        category,
        page_name,
        customer_id,
        time_spent
    ]

def generate_ccai_log(agent_id, customer_id, timestamp_millis):
    """Generates a simulated Google CCAI call transcript in the specified format."""

    greetings = [
        "Hello, how can I assist you today?",
        "Hi there, what can I help you with today?",
        "Greetings, how can I help you?",
        "Hi, welcome to support, how can I help you today?",
        "Hello, what can I assist you with?",
    ]

    devices = [
        "television",
        "laptop",
        "router",
        "mobile phone",
        "smart watch",
        "tablet",
        "streaming device",
    ]

    problems = [
        "The {0} doesn't seem to turn on. The {0} does not respond to any buttons or commands. The power light on the {0} does not turn on.",
        "The {0} is not connecting to the internet. The {0} cannot connect to a Wi-Fi network. The {0} cannot connect to the internet when plugged into a wired network.",
        "I cannot download any apps on my {0}. I am only able to access the messaging app on my {0}. I am not able to access other apps.",
        "I have not been able to connect to my account from my {0}. I cannot log into my account on my {0}. I cannot access my account on the {0}. I do not know what to do to fix my account.",
        "The battery on my {0} only lasts 30 minutes. The battery drains quickly after being fully charged. The {0} battery does not last as long as it used to.",
    ]

    problem_detail = [
        "The {0} says that there is an error with the latest update. The {0} is stuck on the previous update. The update is not working properly on the {0}.",
        "It's been happening for the last 4 days, when I dropped the {0}. It's possible that the fall caused some damage to the {0}.",
        "The {0} isn't responding when I try to factory reset it. I changed the power settings a few days ago, and the {0} hasn't been working correctly since then.",
        "I tried using the troubleshooting wizard on the {0}, but it didn't help. There was a warning to check that the {0} has enough storage space and if it's compatible with the software I'm trying to use.",
        "The problem with the {0} is still happening since I last called in. I tried restarting the {0} 3 times and the issue is still happening. It's reporting a memory error about once an hour.",
    ]

    statuses = [
        "Error: Failed update. The update is not available for your current major version. Please check for updates again later.",
        "All systems normal. Your device is connected to the internet and functioning normally. There are no issues to report.",
        "Warning: No available storage. Your computer's hard drive is full. Please delete some files and try again. You can also try to free up some space by moving some files to an external storage device.",
        "Error: Your account is not authorized to access this resource. Please contact the administrator for assistance.",
        "Warning: No connection to the internet. Your internet connection is blocked by a firewall. Please contact the administrator to unblock it.",
    ]

    solutions = [
        "Have you tried turning the {0} off and on again? The {0} should be connected to the internet in order to contact our servers. If it is not, check your internet connection and make sure that your {0} is connected.",
        "Can you update your {0} to the latest firmware version? You can check if your {0}'s firmware is up to date by going to the {0}'s settings and looking for a firmware update option. If there is an update available, install it.",
        "Check if your {0} is able to access streaming content. You can check if your {0} is able to access streaming content by trying to watch a show or movie on a streaming service. If you are unable to watch anything, check your internet connection and make sure that your {0} is connected to the correct network.",
        "Check if your {0} are receiving a signal? You can check if your {0} are receiving a signal by using a signal strength meter. If the signal strength is low, you may need to move your {0} closer to the router.",
        "Have you tried to factory reset the {0}? You can check if your {0}'s settings are correct by going to the {0}'s settings and looking for a default settings option. If there is a default settings option, reset your {0} to the default settings.",
    ]

    check_solved = [
        "Sure, does that cover everything for today?",
        "No problem, is there anything else that I can help with?",
        "Sure thing, did that solve the issue for you?",
        "Sounds good, are there any other issues that I can help with?",
        "Great, did that fix the problem?",
    ]

    problem_solved = [
        "Yes, my problem is solved now. I have checked the settings on my {0} and made sure that everything is set up correctly.",
        "No, I'm still having the same problem. I will try contacting the manufacturer of the {0} for help.",
        "Yes, everything is working fine now. I have tried using a different connection to see if the problem is with the {0} or with the internet service provider.",
        "Yes, the {0} seems to be working now. I have checked the connections and made sure that everything is plugged in properly.",
        "No, I'm having a different problem now with the {0}. I have tried using a different website or app to see if the problem is with the website or app itself.",
    ]

    device = random.choice(devices)
    # timestamp = int(timestamp_millis * 1e6)  # Convert to microseconds
    # call_start_time = timestamp - random.randint(0, 300) * 1e6  # Start time up to 5 mins before
    #
    # # Calculate a random call duration between 1 and 10 minutes
    # call_duration_seconds = random.randint(60, 600)  # 1 to 10 minutes
    # call_end_time = call_start_time + (call_duration_seconds * 1e6)

    # Convert the given timestamp_millis (in epoch milliseconds) to a timezone-aware datetime object in UTC
    event_time_utc = datetime.datetime.utcfromtimestamp(timestamp_millis / 1000).replace(tzinfo=datetime.timezone.utc)

    # Calculate a random call start time within 5 minutes before the event time
    call_start_time_utc = event_time_utc - datetime.timedelta(seconds=random.randint(0, 300))

    # Calculate a random call duration between 1 and 10 minutes
    call_duration_seconds = random.randint(60, 600)  # 1 to 10 minutes
    call_end_time_utc = call_start_time_utc + datetime.timedelta(seconds=call_duration_seconds)

    # Construct the conversation transcript (using the correct call_start_time_utc variable)
    conversation_text = (
        f"Customer {customer_id} called at {call_start_time_utc.timestamp() * 1000}:\n"  # Convert to milliseconds for display
        f"- Agent Introduction: {random.choice(greetings)}\n"
        f"- Customer Inquiry: 'I'm having an issue with my {device}.'\n"
        f"- Agent Assistance: 'Can you tell me what the problem is?'\n"
        f"- Customer Response: '{random.choice(problems).format(device)}'\n"
        f"- Agent Processing: 'Can you give me more details about the problem?'\n"
        f"- Customer Response: '{random.choice(problem_detail).format(device)}'\n"
        f"- Agent Processing: 'What is the status shown in the settings on the {device}?'\n"
        f"- Customer Response: '{random.choice(statuses)}'\n"
        f"- Agent Assistance: 'Can you tell me your account number?'\n"
        f"- Customer Response: 'Sure, it's {random.randint(100000000, 999999999)}'\n"
        f"- Agent Assistance: {random.choice(solutions).format(device)}\n"
        f"- Customer Confirmation: 'I see, thanks for the information, I will give that a try.'\n"
        f"- Agent Check: {random.choice(check_solved)}\n"
        f"- Customer Confirmation: {random.choice(problem_solved).format(device)}\n"
        f"- Call Conclusion: 'Is there anything else I can assist you with today?'\n"
        f"- Customer Farewell: 'No, that's all. Thank you.'\n"
        f"- Agent Farewell: 'You're welcome. Have a great day!'"
    )

    return {
        "call_start_time": call_start_time_utc.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        # Convert to milliseconds for display
        "call_end_time": call_end_time_utc.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "call_duration_seconds": call_duration_seconds,
        "transcript": conversation_text,
        "agent_id": agent_id,
        "customer_id": customer_id
    }


# call_start_time_sec = call_start_time // 1e6  # Convert to seconds
    # call_end_time_sec = call_end_time // 1e6  # Convert to seconds
    #
    # return {
    #     "call_start_time": datetime.datetime.fromtimestamp(call_start_time_sec).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
    #     "call_end_time": datetime.datetime.fromtimestamp(call_end_time_sec).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
    #     "call_duration_seconds": call_duration_seconds,
    #     "transcript": conversation_text,
    #     "agent_id": agent_id,
    #     "customer_id": customer_id
    # }


# Generate data
kibana_data = [generate_kibana_record() for _ in range(num_records)]
sitecatalyst_data = [generate_sitecatalyst_record(record[4], random.choice(agents), record[0]) for record in kibana_data]  # Generating SiteCatalyst data for each Kibana record

# Convert the data to dictionaries for JSON output
# Create DataFrames
kibana_df = pd.DataFrame(
    kibana_data,
    columns=[
        "@timestamp",
        "message",
        "event.action",
        "event.button_name",
        "event.customer_id",
        "event.api_endpoint",
        "event.status",
        "event.response_time",
    ],
)
sitecatalyst_df = pd.DataFrame(
    sitecatalyst_data,
    columns=[
        "hit_time_gmt",
        "post_visid_high",
        "post_visid_low",
        "visit_num",
        "page_name",
        "page_url",
        "event_list",
        "events",
        "evar1",
        "prop1",
        "prop2",
        "event.customer_id",
        "time_spent",
    ],
)

# Convert to correct data types
kibana_df["event.customer_id"] = kibana_df["event.customer_id"].astype(str)
sitecatalyst_df["event.customer_id"] = sitecatalyst_df["event.customer_id"].astype(str)

# Convert timestamps to datetime objects
kibana_df["@timestamp"] = pd.to_datetime(kibana_df["@timestamp"])
sitecatalyst_df["hit_time_gmt"] = pd.to_datetime(sitecatalyst_df["hit_time_gmt"])

# Sort by timestamp and customer ID
kibana_df.sort_values(by=["@timestamp", "event.customer_id"], inplace=True)
sitecatalyst_df.sort_values(by=["hit_time_gmt", "event.customer_id"], inplace=True)

# Merge dataframes, allowing for slight timestamp differences
merged_df = pd.merge_asof(
    kibana_df,
    sitecatalyst_df,
    left_on="@timestamp",
    right_on="hit_time_gmt",
    by="event.customer_id",
    tolerance=pd.Timedelta("1 minute"),
    direction="nearest",
)

# Correctly escape forward slashes in "page_url" and "event.api_endpoint" before saving to JSON
merged_df['page_url'] = merged_df['page_url'].astype(str).str.replace(r'\\/', '/')
merged_df['event.api_endpoint'] = merged_df['event.api_endpoint'].astype(str).str.replace(r'\\/', '/')


# Save Kibana data to CSV
kibana_df.to_csv("kibana_agent_data.csv", index=False)

# Save Kibana data to JSON
kibana_json = kibana_df.to_json(orient="records",date_format="iso", indent=4)
with open("kibana_agent_data.json", "w") as kibana_json_file:
    kibana_json_file.write(kibana_json)

# Save SiteCatalyst data to CSV
sitecatalyst_df.to_csv("sitecatalyst_agent_data.csv", index=False)

# Save SiteCatalyst data to JSON
sitecatalyst_json = sitecatalyst_df.to_json(orient="records",date_format="iso", indent=4)
with open("sitecatalyst_agent_data.json", "w") as sitecatalyst_json_file:
    sitecatalyst_json_file.write(sitecatalyst_json)

# Load JSON data from file
with open("merged_agent_data.json", "r") as merged_json_file:
    merged_data = json.load(merged_json_file)

# Clean up 'event.api_endpoint' field
for record in merged_data:
    if record.get('event.api_endpoint'):
        record['event.api_endpoint'] = record['event.api_endpoint'].replace('\\/', '/')

# Write the cleaned merged data back to the JSON file
with open("merged_agent_data.json", "w") as merged_json_file:
    json.dump(merged_data, merged_json_file, indent=4)

# Clean up 'event.api_endpoint' field in Kibana JSON data
kibana_data = json.loads(kibana_json)
for record in kibana_data:
    if 'event.api_endpoint' in record:
        record['event.api_endpoint'] = record['event.api_endpoint'].replace('\\', '')

# Write the cleaned Kibana data back to the JSON file
with open("kibana_agent_data.json", "w") as kibana_json_file:
    json.dump(kibana_data, kibana_json_file, indent=4)

# Clean up 'event.api_endpoint' field in SiteCatalyst JSON data
sitecatalyst_data = json.loads(sitecatalyst_json)
for record in sitecatalyst_data:
    if 'event.api_endpoint' in record:
        record['event.api_endpoint'] = record['event.api_endpoint'].replace('\\', '')

# Write the cleaned SiteCatalyst data back to the JSON file
with open("sitecatalyst_agent_data.json", "w") as sitecatalyst_json_file:
    json.dump(sitecatalyst_data, sitecatalyst_json_file, indent=4)

# Save merged DataFrame to CSV
merged_df.to_csv("merged_agent_data.csv", index=False)

# Save to JSON
merged_json = merged_df.to_json(orient="records", date_format="iso", indent=4)
with open("merged_agent_data.json", "w") as merged_json_file:
    merged_json_file.write(merged_json)

# Load JSON data from file
with open("merged_agent_data.json", "r") as merged_json_file:
    merged_data = json.load(merged_json_file)

# Clean up 'event.api_endpoint' field
for record in merged_data:
    record['event.api_endpoint'] = record['event.api_endpoint'].replace('\\', '')

# Write the cleaned merged data back to the JSON file
with open("merged_agent_data.json", "w") as merged_json_file:
    json.dump(merged_data, merged_json_file, indent=4)

print("Data generated, merged, and saved to CSV and JSON successfully!")

# Generate CCAI transcripts and store them in a list
ccai_data = []
for _, row in merged_df.iterrows():  # Iterate over the merged DataFrame
    agent_id = row["evar1"]           # Get agent_id and customer_id from merged data
    customer_id = row["event.customer_id"]
    timestamp_millis = int(row["@timestamp"].timestamp() * 1000) # Use Kibana timestamp

    ccai_log = generate_ccai_log(agent_id, customer_id, timestamp_millis)
    ccai_data.append(ccai_log)

    # Convert CCAI timestamps to strings with ISO format before creating DataFrame
    for log in ccai_data:
        log['call_start_time'] = str(log['call_start_time'])
        log['call_end_time'] = str(log['call_end_time'])

# Create DataFrame for CCAI transcripts and include agent and customer IDs
ccai_df = pd.DataFrame(ccai_data)

# Save CCAI data to CSV
ccai_df.to_csv("ccai_transcripts.csv", index=False)

# Save CCAI data to JSON
ccai_json = ccai_df.to_json(orient="records", date_format="iso", indent=4)
with open("ccai_transcripts.json", "w") as ccai_json_file:
    ccai_json_file.write(ccai_json)

print("CCAI transcripts generated and saved successfully!")

# Load CCAI transcripts data from CSV
ccai_df = pd.read_csv("ccai_transcripts.csv")

# Load merged agent data from CSV
merged_df = pd.read_csv("merged_agent_data.csv")

# Merge the two dataframes based on agent and customer IDs
merged_insights_df = pd.merge(
    ccai_df,
    merged_df,
    how="inner",
    left_on=["agent_id", "customer_id"],
    right_on=["evar1", "event.customer_id"]
)

# Save merged insights data to CSV
merged_insights_df.to_csv("merged_insights_data.csv", index=False)

# Save merged insights data to JSON
merged_insights_json = merged_insights_df.to_json(orient="records", date_format="iso", indent=4)
with open("merged_insights_data.json", "w") as merged_insights_json_file:
    merged_insights_json_file.write(merged_insights_json)

print("Merged agent insights generated and saved successfully!")


# Function to generate text format easily interpretable by LLM
def generate_text_record(record):
    timestamp = record["@timestamp"]
    message = record["message"]
    action = record["event.action"]
    button_name = record["event.button_name"]
    customer_id = record["event.customer_id"]
    api_endpoint = record["event.api_endpoint"]
    status = record["event.status"]
    response_time = record["event.response_time"]

    text = f"At {timestamp}, agent {message.lower()} for customer {customer_id}. "
    if status == "success":
        text += f"The {action} was successful. "
    else:
        text += f"The {action} failed. "

    if button_name:
        text += f"The action was triggered by the '{button_name}' button. "

    text += f"The API endpoint accessed was {api_endpoint}. "
    text += f"The response time was {response_time} milliseconds."

    return text

# Generate data in text format
text_data_for_llm = [generate_text_record(record) for record in merged_data]

# Save text data to a file
with open("text_data_for_llm.txt", "w") as text_file:
    text_file.write("\n".join(text_data_for_llm))

print("Data generated in text format successfully!")
