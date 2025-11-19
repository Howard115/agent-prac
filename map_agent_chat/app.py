from pydantic_ai import Agent
import streamlit as st
import asyncio
from model import LocationMapResponse
from streamlit_folium import st_folium
from pydantic_ai.messages import ModelRequest, ModelResponse, SystemPromptPart, UserPromptPart, TextPart
from create_map import create_location_map

def create_agent_1():
    agent_1 = Agent(
            "openai:gpt-4o-mini",
            output_type=LocationMapResponse,
        )
    
    @agent_1.system_prompt
    def system_prompt():
        return (
            """
            You are a friendly location assistant helping users find and visualize places on maps.
        
            When responding to location-related queries:
            1. Always provide both 'location' and 'response' fields.
            2. The 'location' field should contain the place name.
            3. The 'response' field should contain your message to the user.
            """
        )
    
    @agent_1.output_validator
    async def validate_result(result: LocationMapResponse):
        try:
            if result.location:
                create_location_map(result.location)
            return result.response
        except Exception as e:
            st.error(f"Error displaying map: {str(e)}")
            return result.response
        
    agent_1.system_prompt_content = system_prompt()
    return agent_1

def initialize_session_state():
    st.session_state.agent_1 = create_agent_1()
    st.session_state.history = [
        ModelRequest(
            parts=[SystemPromptPart(content=st.session_state.agent_1.system_prompt_content)]
        )
    ]
    st.session_state.map = None

if not st.session_state.get("isSessionStateInitialized"):
    initialize_session_state()
    st.session_state["isSessionStateInitialized"] = True

class AgentChat:
    def __init__(self):
        self.agent_1 = st.session_state.agent_1
        self.history = st.session_state.history

    def display_chat_history(self):
        for message in self.history:
            if isinstance(message, ModelRequest):
                # Show user prompts from requests
                for part in message.parts:
                    if isinstance(part, UserPromptPart):
                        st.chat_message("user").markdown(part.content)
            elif isinstance(message, ModelResponse):
                # Show text responses from model
                for part in message.parts:
                    if isinstance(part, TextPart):
                        st.chat_message("assistant").markdown(part.content)

    async def update_chat_async(self, prompt: str):
        # Store user input as ModelRequest with UserPromptPart
        user_request = ModelRequest(parts=[UserPromptPart(content=prompt)])
        st.session_state.history.append(user_request)
        st.chat_message("user").markdown(prompt)

        response = await self.agent_1.run(prompt, message_history=self.history)
        
        # Store response as ModelResponse with TextPart
        response_msg = ModelResponse(
            parts=[TextPart(content=response.output)],
            model_name="openai:gpt-4o-mini"
        )
        st.session_state.history.append(response_msg)
        st.chat_message("assistant").markdown(response.output)

    def update_chat(self, prompt: str):
        asyncio.run(self.update_chat_async(prompt))

    def run(self):
        self.display_chat_history()

        if prompt := st.chat_input("What is up?"):
            self.update_chat(prompt)
            



def main():
    agent_chat = AgentChat()
    agent_chat.run()
    if st.session_state.map:
        with st.sidebar:
            st_folium(st.session_state.map, width=500)

    
if __name__ == "__main__":
    main()
