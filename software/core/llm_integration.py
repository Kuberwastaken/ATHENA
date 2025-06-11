"""
LLM Integration Module for ATHENA

This module handles the integration with local LLMs, including function calling
and intelligent response generation.
"""

import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger("llm_integration")

@dataclass
class LLMMessage:
    """Represents a message in the conversation."""
    role: str  # "system", "user", "assistant", "function"
    content: str
    function_call: Optional[Dict[str, Any]] = None
    name: Optional[str] = None  # For function results

class LLMIntegration:
    """
    Handles integration with local LLMs for intelligent response generation
    and function calling.
    """
    
    def __init__(self, model_path: str, function_registry):
        self.model_path = model_path
        self.function_registry = function_registry
        self.conversation_history: List[LLMMessage] = []
        self.system_prompt = self._build_system_prompt()
        
        # Initialize model (placeholder for actual model loading)
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the local LLM model."""
        try:
            # Placeholder for actual model loading
            # In real implementation, would use transformers, llama.cpp, etc.
            logger.info(f"Loading LLM model from {self.model_path}")
            # self.model = load_model(self.model_path)
            logger.info("LLM model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load LLM model: {e}")
            raise
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt with available functions."""
        functions_desc = self._get_functions_description()
        
        return f"""You are ATHENA, an intelligent voice assistant. You can help users with various tasks by calling functions when needed.

Available functions:
{functions_desc}

Guidelines:
- Be conversational and helpful
- Call functions when the user requests actions
- Provide clear, concise responses
- If you need to call a function, use the function_call format
- Always confirm actions before executing them if they could have significant effects

Remember: You are running locally on the user's device, prioritizing privacy and speed."""

    def _get_functions_description(self) -> str:
        """Get a description of available functions for the system prompt."""
        descriptions = []
        
        for category, functions in self.function_registry.categories.items():
            descriptions.append(f"\n{category.upper()} Functions:")
            for func_name in functions:
                func_def = self.function_registry.functions[func_name]
                descriptions.append(f"- {func_name}: {func_def.description}")
        
        return "\n".join(descriptions)
    
    def process_user_input(self, user_text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process user input and generate a response, potentially calling functions.
        
        Args:
            user_text: The user's spoken/typed input
            context: Additional context (location, time, user preferences, etc.)
            
        Returns:
            Dict containing response text, speech, and any function calls made
        """
        try:
            # Add user message to conversation
            user_message = LLMMessage(role="user", content=user_text)
            self.conversation_history.append(user_message)
            
            # Prepare messages for LLM
            messages = self._prepare_messages()
            
            # Get LLM response
            response = self._call_llm(messages)
            
            # Process response (handle function calls)
            result = self._process_llm_response(response)
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing user input: {e}")
            return {
                "text": "I'm sorry, I encountered an error processing your request.",
                "speech": "I'm sorry, I encountered an error processing your request.",
                "success": False
            }
    
    def _prepare_messages(self) -> List[Dict[str, Any]]:
        """Prepare messages for LLM input."""
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add conversation history (keep last N messages to avoid context limit)
        max_history = 10
        recent_history = self.conversation_history[-max_history:]
        
        for msg in recent_history:
            message = {"role": msg.role, "content": msg.content}
            if msg.function_call:
                message["function_call"] = msg.function_call
            if msg.name:
                message["name"] = msg.name
            messages.append(message)
        
        return messages
    
    def _call_llm(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Call the local LLM with the prepared messages."""
        # Placeholder for actual LLM call
        # In real implementation, would use the loaded model
        
        # Simulate LLM response based on user input
        user_input = messages[-1]["content"].lower()
        
        if "play" in user_input and ("music" in user_input or "song" in user_input):
            # Simulate function calling for music
            artist = self._extract_artist(user_input)
            service = self._extract_service(user_input)
            
            return {
                "content": None,
                "function_call": {
                    "name": "play_music",
                    "arguments": json.dumps({
                        "artist": artist,
                        "service": service
                    })
                }
            }
        
        elif "weather" in user_input:
            location = self._extract_location(user_input)
            return {
                "content": None,
                "function_call": {
                    "name": "get_weather",
                    "arguments": json.dumps({
                        "location": location
                    })
                }
            }
        
        elif "volume" in user_input:
            volume = self._extract_volume(user_input)
            return {
                "content": None,
                "function_call": {
                    "name": "set_volume",
                    "arguments": json.dumps({
                        "level": volume
                    })
                }
            }
        
        else:
            return {
                "content": f"I understand you said: '{messages[-1]['content']}'. How can I help you with that?"
            }
    
    def _process_llm_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process the LLM response and handle function calls."""
        if "function_call" in response and response["function_call"]:
            # Handle function call
            function_name = response["function_call"]["name"]
            arguments = json.loads(response["function_call"]["arguments"])
            
            # Execute function
            function_result = self.function_registry.execute_function(function_name, arguments)
            
            # Add function call and result to conversation history
            function_call_msg = LLMMessage(
                role="assistant",
                content=None,
                function_call=response["function_call"]
            )
            self.conversation_history.append(function_call_msg)
            
            function_result_msg = LLMMessage(
                role="function",
                name=function_name,
                content=json.dumps(function_result)
            )
            self.conversation_history.append(function_result_msg)
            
            # Generate final response based on function result
            final_response = self._generate_final_response(function_name, arguments, function_result)
            
        else:
            # Direct text response
            final_response = {
                "text": response["content"],
                "speech": response["content"],
                "success": True
            }
            
            # Add to conversation history
            assistant_msg = LLMMessage(role="assistant", content=response["content"])
            self.conversation_history.append(assistant_msg)
        
        return final_response
    
    def _generate_final_response(self, function_name: str, arguments: Dict[str, Any], function_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a natural language response based on function execution."""
        if not function_result.get("success", False):
            return {
                "text": f"I'm sorry, I couldn't {function_name.replace('_', ' ')}. {function_result.get('error', 'Unknown error')}",
                "speech": f"I'm sorry, I couldn't {function_name.replace('_', ' ')}.",
                "success": False
            }
        
        # Generate response based on function type
        if function_name == "play_music":
            artist = arguments.get("artist", "music")
            service = arguments.get("service", "music service")
            response_text = f"Now playing {artist} on {service}"
            
        elif function_name == "get_weather":
            weather_data = function_result["result"]
            location = weather_data["location"]
            temp = weather_data["temperature"]
            desc = weather_data["description"]
            response_text = f"The weather in {location} is {desc} with a temperature of {temp} degrees"
            
        elif function_name == "set_volume":
            level = arguments["level"]
            response_text = f"Volume set to {level}%"
            
        elif function_name == "web_search":
            query = arguments["query"]
            response_text = f"I found several results for '{query}'. Here's what I found..."
            
        else:
            response_text = f"I've executed the {function_name.replace('_', ' ')} function successfully"
        
        return {
            "text": response_text,
            "speech": response_text,
            "success": True,
            "function_result": function_result
        }
    
    # Helper methods for extracting information from user input
    def _extract_artist(self, text: str) -> str:
        """Extract artist name from user input."""
        # Simple extraction - in real implementation, use NER
        if "the weeknd" in text.lower():
            return "The Weeknd"
        elif "taylor swift" in text.lower():
            return "Taylor Swift"
        else:
            return "unknown artist"
    
    def _extract_service(self, text: str) -> str:
        """Extract music service from user input."""
        if "spotify" in text.lower():
            return "spotify"
        elif "youtube" in text.lower():
            return "youtube"
        else:
            return "spotify"  # Default
    
    def _extract_location(self, text: str) -> str:
        """Extract location from user input."""
        # Simple extraction - in real implementation, use NER
        words = text.split()
        for i, word in enumerate(words):
            if word.lower() in ["in", "for", "at"] and i + 1 < len(words):
                return words[i + 1].capitalize()
        return "current location"
    
    def _extract_volume(self, text: str) -> int:
        """Extract volume level from user input."""
        import re
        numbers = re.findall(r'\d+', text)
        if numbers:
            return min(100, max(0, int(numbers[0])))
        elif "up" in text.lower():
            return 80
        elif "down" in text.lower():
            return 20
        else:
            return 50
    
    def clear_conversation(self):
        """Clear conversation history."""
        self.conversation_history = []
        logger.info("Conversation history cleared")
