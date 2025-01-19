from pydantic_ai import Agent
import streamlit as st
import asyncio
from pydantic_ai.messages import SystemPrompt, UserPrompt, ModelTextResponse


def create_agent_1():
    agent_1 = Agent(
        "openai:gpt-4o-mini",
    )

    @agent_1.system_prompt
    def system_prompt():
        return "You are a helpful assistant."

    agent_1.system_prompt_content = system_prompt()
    return agent_1


def initialize_session_state():
    st.session_state.agent_1 = create_agent_1()
    st.session_state.history = [
        SystemPrompt(content=st.session_state.agent_1.system_prompt_content)
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
            if message.role == "user":
                st.chat_message("user").markdown(message.content)
            elif message.role == "model-text-response":
                st.chat_message("assistant").markdown(message.content)

    async def update_chat_async(self, prompt: str):
        st.chat_message("user").markdown(prompt)
        response = await self.agent_1.run(prompt, message_history=self.history)
        st.chat_message("assistant").markdown(response.data)

        user_message = UserPrompt(content=prompt)
        ai_message = ModelTextResponse(content=f"{response.data}")
        st.session_state.history += [user_message, ai_message]

    def update_chat(self, prompt: str):
        asyncio.run(self.update_chat_async(prompt))

    def run(self):
        self.display_chat_history()

        if prompt := st.chat_input("What is up?"):
            self.update_chat(prompt)


def main():
    agent_chat = AgentChat()
    agent_chat.run()


if __name__ == "__main__":
    main()
