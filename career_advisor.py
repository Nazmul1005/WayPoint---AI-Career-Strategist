"""
Career Advisor logic using LangChain with support for Ollama, OpenAI, and Google Gemini
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from config import AI_PROVIDER, API_KEY, MODEL_NAME, MODEL_TEMPERATURE, OLLAMA_BASE_URL
from prompts import WAYPOINT_SYSTEM_PROMPT
from utils import check_guardrails, create_out_of_scope_response


class WayPointAdvisor:
    """
    WayPoint Career Advisor powered by LangChain
    Supports Ollama (local), OpenAI, and Google Gemini
    """
    
    def __init__(self):
        """Initialize the career advisor with LLM and conversation memory"""
        
        # Initialize the appropriate LLM based on provider
        if AI_PROVIDER == "ollama":
            from langchain_ollama import ChatOllama
            try:
                self.llm = ChatOllama(
                    model=MODEL_NAME,
                    temperature=MODEL_TEMPERATURE,
                    base_url=OLLAMA_BASE_URL
                )
                self.provider_name = "Ollama (Local)"
                self.current_model = MODEL_NAME
            except Exception as e:
                raise ValueError(
                    f"❌ Could not connect to Ollama.\n\n"
                    f"Please make sure:\n"
                    f"1. Ollama is installed: https://ollama.com/download\n"
                    f"2. Ollama is running (check if you see the icon in menu bar)\n"
                    f"3. Model '{MODEL_NAME}' is downloaded: `ollama pull {MODEL_NAME}`\n\n"
                    f"Error: {str(e)}"
                )
                
        elif AI_PROVIDER == "gemini":
            if not API_KEY:
                raise ValueError("GOOGLE_API_KEY not found in .env file")
            from langchain_google_genai import ChatGoogleGenerativeAI
            self.llm = ChatGoogleGenerativeAI(
                model=MODEL_NAME,
                temperature=MODEL_TEMPERATURE,
                google_api_key=API_KEY
            )
            self.provider_name = "Google Gemini"
            self.current_model = MODEL_NAME
            
        elif AI_PROVIDER == "openai":
            if not API_KEY:
                raise ValueError("OPENAI_API_KEY not found in .env file")
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(
                model=MODEL_NAME,
                temperature=MODEL_TEMPERATURE,
                openai_api_key=API_KEY
            )
            self.provider_name = "OpenAI"
            self.current_model = MODEL_NAME
        else:
            raise ValueError(
                "No AI provider configured.\n\n"
                "Options:\n"
                "1. Use Ollama (FREE, local): Set USE_OLLAMA=true in .env\n"
                "2. Use Google Gemini (FREE): Add GOOGLE_API_KEY to .env\n"
                "3. Use OpenAI (Paid): Add OPENAI_API_KEY to .env"
            )
        
        # Initialize conversation memory (list of messages)
        self.conversation_history = []
        
        # Create the chat prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", WAYPOINT_SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        # Create the chain
        self.chain = self.prompt | self.llm
    
    def get_response(self, user_input: str, user_context: dict = None) -> str:
        """
        Get WayPoint's response to user input
        
        Args:
            user_input: The user's message
            user_context: Optional dictionary with user context (skills, experience, etc.)
            
        Returns:
            WayPoint's response
        """
        # Check guardrails first
        guardrail_check = check_guardrails(user_input)
        if guardrail_check:
            return create_out_of_scope_response(guardrail_check)
        
        # Enhance input with context if provided
        enhanced_input = user_input
        if user_context:
            context_parts = []
            if user_context.get("current_role"):
                context_parts.append(f"Current Role: {user_context['current_role']}")
            if user_context.get("experience_years"):
                context_parts.append(f"Experience: {user_context['experience_years']} years")
            if user_context.get("skills"):
                context_parts.append(f"Skills: {user_context['skills']}")
            if user_context.get("education"):
                context_parts.append(f"Education: {user_context['education']}")
            
            if context_parts:
                context_str = " | ".join(context_parts)
                enhanced_input = f"[Context: {context_str}]\n\n{user_input}"
        
        # Get response from chain
        try:
            response = self.chain.invoke({
                "history": self.conversation_history,
                "input": enhanced_input
            })
            
            # Add to conversation history
            self.conversation_history.append(HumanMessage(content=user_input))
            self.conversation_history.append(AIMessage(content=response.content))
            
            # Keep only last 20 messages (10 exchanges) to avoid context length issues
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return response.content
            
        except Exception as e:
            error_msg = str(e)
            
            # Provide helpful error messages based on error type
            if "quota" in error_msg.lower() or "429" in error_msg:
                return (
                    "⚠️ **API Quota Exceeded**\n\n"
                    "You've run out of credits. Here are your options:\n\n"
                    "1. **Use Google Gemini (FREE)**: Get a free API key at https://makersuite.google.com/app/apikey\n"
                    "   - Add to `.env`: `GOOGLE_API_KEY=your_key_here`\n\n"
                    "2. **Add OpenAI credits**: Visit https://platform.openai.com/account/billing"
                )
            elif "authentication" in error_msg.lower() or "401" in error_msg:
                return (
                    "⚠️ **Invalid API Key**\n\n"
                    "Please check your API key in the `.env` file.\n\n"
                    f"Current provider: {self.provider_name}\n"
                    "Make sure the key is valid and not expired."
                )
            else:
                return (
                    f"⚠️ **Error from {self.provider_name}**\n\n"
                    f"{error_msg}\n\n"
                    "Please check your API key and internet connection."
                )
    
    def get_conversation_history(self) -> list:
        """Get the conversation history"""
        return self.conversation_history
    
    def clear_conversation(self):
        """Clear the conversation history"""
        self.conversation_history = []
    
    def get_memory_context(self) -> str:
        """Get a summary of the conversation context"""
        if not self.conversation_history:
            return "No conversation history yet."
        
        # Return last 5 exchanges for context
        recent_messages = self.conversation_history[-10:]  # Last 5 exchanges
        context = []
        
        for msg in recent_messages:
            if isinstance(msg, HumanMessage):
                role = "User"
            elif isinstance(msg, AIMessage):
                role = "WayPoint"
            else:
                continue
                
            # Truncate long messages
            content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
            context.append(f"{role}: {content}")
        
        return "\n".join(context)
    
    def get_provider_info(self) -> str:
        """Get information about the current AI provider"""
        return f"🤖 Powered by: {self.provider_name} ({self.current_model})"
    
    def update_model(self, new_model: str):
        """
        Update the LLM model dynamically
        
        Args:
            new_model: The name of the new model to use
        """
        from config import AI_PROVIDER, MODEL_TEMPERATURE, OLLAMA_BASE_URL, API_KEY
        
        self.current_model = new_model
        
        try:
            if AI_PROVIDER == "ollama":
                from langchain_ollama import ChatOllama
                self.llm = ChatOllama(
                    model=new_model,
                    temperature=MODEL_TEMPERATURE,
                    base_url=OLLAMA_BASE_URL
                )
            elif AI_PROVIDER == "gemini":
                from langchain_google_genai import ChatGoogleGenerativeAI
                self.llm = ChatGoogleGenerativeAI(
                    model=new_model,
                    temperature=MODEL_TEMPERATURE,
                    google_api_key=API_KEY
                )
            elif AI_PROVIDER == "openai":
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    model=new_model,
                    temperature=MODEL_TEMPERATURE,
                    openai_api_key=API_KEY
                )
            
            # Recreate the chain with the new LLM
            self.chain = self.prompt | self.llm
            
        except Exception as e:
            raise ValueError(f"Failed to update model to {new_model}: {str(e)}")


