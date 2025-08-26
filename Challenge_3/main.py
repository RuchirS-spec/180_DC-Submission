import streamlit as st
import requests

# App Title
st.title("⚖️ Courtroom Clash - AI Debate Simulator")

# User input
case_query = st.text_input("Enter the case you want the lawyers to debate on:")

# Button
if st.button("Start Debate") and case_query.strip():
    with st.spinner("Summoning the court..."):
        try:
            FLOW_ID = "fbbe6810-3d83-4b36-bc5c-3718e01db863"
            WORKSPACE_ID = "b62bf019-5a79-469c-a4fe-8efd0feb50fb"
            BASE_URL = "https://api.langflow.astra.datastax.com"
            LANGFLOW_API_KEY = "AstraCS:qROmAHpJqqRETLccqwZcDywc:9133db37f37dfcb351ef237903c3cab3791888b35b0fbd6dc9b4ed55f6431e12"

            url = f"{BASE_URL}/lf/{WORKSPACE_ID}/api/v1/run/{FLOW_ID}"

            headers = {
                "Authorization": f"Bearer {LANGFLOW_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "input_value": case_query,
                "output_type": "chat",
                "input_type": "chat"
            }

            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                data = response.json()

                st.subheader("👨‍⚖️ Court Proceedings")

                # Extract debate transcript
                try:
                    messages = data["outputs"][0]["outputs"][0]["results"]["message"]["text"].split("\n")
                except Exception:
                    st.error("Could not parse Langflow response.")
                    st.json(data)
                    st.stop()

                # Format round by round
                for msg in messages:
                    msg = msg.strip()
                    if not msg:
                        continue

                    if msg.lower().startswith("prosecutor"):
                        st.markdown(f"🟥 **Prosecutor:** {msg.split(':',1)[1].strip()}")
                    elif msg.lower().startswith("defense"):
                        st.markdown(f"🟦 **Defense:** {msg.split(':',1)[1].strip()}")
                    elif msg.lower().startswith("judge"):
                        st.markdown(f"⚖️ **Judge:** {msg.split(':',1)[1].strip()}")
                    else:
                        st.write(msg)

            else:
                st.error(f"Langflow API error: {response.status_code} → {response.text}")

        except Exception as e:
            st.error(f"Error: {str(e)}")
