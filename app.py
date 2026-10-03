
import streamlit as st
from langchain_groq import ChatGroq
import json

st.set_page_config(
    page_title="Smart City Dispatch",
    layout="centered"
)

st.title("🚑 Smart City Dynamic Dispatch Grid")


# API Key
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input(
        "Groq API Key",
        type="password"
    )


# Mock 911 calls
calls = st.text_area(
    "🚨 Emergency Calls",
    height=250,
    value="""
There is a huge fire near Andheri Station.
People are trapped inside the building.

Fire at Andheri Station.
Many people need help.

Someone is injured near Bandra.
Please send an ambulance.
"""
)


# Resource Database
resources = {
    "Fire Truck 1": {
        "type": "Fire Truck",
        "status": "Available"
    },

    "Fire Truck 2": {
        "type": "Fire Truck",
        "status": "Busy"
    },

    "Ambulance 1": {
        "type": "Ambulance",
        "status": "Available"
    },

    "Ambulance 2": {
        "type": "Ambulance",
        "status": "Available"
    }
}


# Mock Travel Times
travel_times = {
    "Fire Truck 1": {
        "Andheri Station": 5,
        "Bandra": 12
    },

    "Fire Truck 2": {
        "Andheri Station": 10,
        "Bandra": 15
    },

    "Ambulance 1": {
        "Andheri Station": 8,
        "Bandra": 4
    },

    "Ambulance 2": {
        "Andheri Station": 14,
        "Bandra": 7
    }
}


if st.button("🚨 Analyze & Dispatch"):

    if not api_key:

        st.error("Please enter Groq API Key.")

    else:

        llm = ChatGroq(
            model="openai/gpt-oss-20b",
            temperature=0,
            api_key=api_key
        )


        # =========================
        # 1. TRIAGE AGENT
        # =========================

        triage_prompt = f"""
You are an Emergency Triage Agent.

Analyze these emergency calls:

{calls}

For every unique incident identify:

- Location
- Emergency type
- Severity: LOW, MEDIUM or HIGH
- Number of people affected
- Required resource

Important:
Multiple calls may describe the same incident.
Identify duplicate calls and combine them.

Return a clear structured summary.
"""

        triage_response = llm.invoke(
            triage_prompt
        )

        incident_data = triage_response.content


        st.subheader("🚨 Triage Agent")

        st.write(incident_data)


        # =========================
        # 2. DISPATCH AGENT
        # =========================

        dispatch_prompt = f"""
You are an Emergency Dispatch Agent.

Here are the incidents identified by
the Triage Agent:

{incident_data}


Available resources:

{json.dumps(resources, indent=2)}


Mock travel times:

{json.dumps(travel_times, indent=2)}


Dispatch rules:

1. HIGH priority incidents first.
2. Only use AVAILABLE resources.
3. Match resource type with emergency.
4. Prefer the resource with the shortest travel time.
5. Do not assign one resource to two incidents.
6. Explain why each resource was selected.

Create a dispatch plan.

For each incident provide:

Incident:
Resource:
Travel Time:
Reason:
"""

        dispatch_response = llm.invoke(
            dispatch_prompt
        )


        st.subheader("🚒 Dispatch Agent")

        st.success(
            dispatch_response.content
        )
