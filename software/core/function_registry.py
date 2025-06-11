"""
Function Registry for LLM Tool Use

This module provides a registry of functions that the LLM can call to perform actions.
The LLM receives function descriptions and learns to call them with proper parameters.
"""

import json
import logging
from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger("function_registry")

@dataclass
class FunctionParameter:
    """Represents a function parameter."""
    name: str
    type: str
    description: str
    required: bool = True
    enum_values: Optional[List[str]] = None

@dataclass
class FunctionDefinition:
    """Represents a function that the LLM can call."""
    name: str
    description: str
    parameters: List[FunctionParameter]
    function: Callable
    category: str = "general"

class FunctionRegistry:
    """
    Registry of functions available to the LLM for tool use.
    
    This allows the LLM to understand what actions it can perform
    and call them with the appropriate parameters.
    """
    
    def __init__(self):
        self.functions: Dict[str, FunctionDefinition] = {}
        self.categories: Dict[str, List[str]] = {}
        
    def register_function(self, func_def: FunctionDefinition):
        """Register a function for LLM use."""
        self.functions[func_def.name] = func_def
        
        # Add to category
        if func_def.category not in self.categories:
            self.categories[func_def.category] = []
        self.categories[func_def.category].append(func_def.name)
        
        logger.info(f"Registered function: {func_def.name} ({func_def.category})")
    
    def get_function_schemas(self) -> List[Dict[str, Any]]:
        """Get OpenAI-compatible function schemas for the LLM."""
        schemas = []
        
        for func_def in self.functions.values():
            schema = {
                "name": func_def.name,
                "description": func_def.description,
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
            
            for param in func_def.parameters:
                schema["parameters"]["properties"][param.name] = {
                    "type": param.type,
                    "description": param.description
                }
                
                if param.enum_values:
                    schema["parameters"]["properties"][param.name]["enum"] = param.enum_values
                
                if param.required:
                    schema["parameters"]["required"].append(param.name)
            
            schemas.append(schema)
        
        return schemas
    
    def execute_function(self, function_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a function call from the LLM."""
        if function_name not in self.functions:
            return {"error": f"Function {function_name} not found"}
        
        func_def = self.functions[function_name]
        
        try:
            # Validate parameters
            self._validate_parameters(func_def, parameters)
            
            # Execute function
            result = func_def.function(**parameters)
            
            return {"success": True, "result": result}
            
        except Exception as e:
            logger.error(f"Error executing function {function_name}: {e}")
            return {"success": False, "error": str(e)}
    
    def _validate_parameters(self, func_def: FunctionDefinition, parameters: Dict[str, Any]):
        """Validate function parameters."""
        # Check required parameters
        for param in func_def.parameters:
            if param.required and param.name not in parameters:
                raise ValueError(f"Required parameter '{param.name}' missing")
        
        # Type checking could be added here
        pass

# Global registry instance
function_registry = FunctionRegistry()

def register_tool(name: str, description: str, category: str = "general"):
    """Decorator to register a function as an LLM tool."""
    def decorator(func):
        # Extract parameter info from function signature
        import inspect
        sig = inspect.signature(func)
        parameters = []
        
        for param_name, param in sig.parameters.items():
            param_type = "string"  # Default type
            if param.annotation != inspect.Parameter.empty:
                if param.annotation == int:
                    param_type = "integer"
                elif param.annotation == float:
                    param_type = "number"
                elif param.annotation == bool:
                    param_type = "boolean"
            
            parameters.append(FunctionParameter(
                name=param_name,
                type=param_type,
                description=f"Parameter {param_name}",
                required=param.default == inspect.Parameter.empty
            ))
        
        func_def = FunctionDefinition(
            name=name,
            description=description,
            parameters=parameters,
            function=func,
            category=category
        )
        
        function_registry.register_function(func_def)
        return func
    
    return decorator

# Function implementations using real integrations
from ..integrations.music import music_manager
from ..integrations.web_search import search_manager

@register_tool("play_music", "Play music from a specified artist or song", "music")
def play_music(artist: str, song: str = None, service: str = "spotify"):
    """Play music using the specified service."""
    if music_manager:
        return music_manager.play_music(artist, song, service)
    else:
        return {"error": "Music manager not initialized"}

@register_tool("control_music", "Control music playback (pause, resume, next, previous)", "music")
def control_music(action: str, service: str = "spotify"):
    """Control music playback."""
    if music_manager:
        return music_manager.control_playback(action, service)
    else:
        return {"error": "Music manager not initialized"}

@register_tool("web_search", "Search the web for information", "information")
def web_search(query: str, num_results: int = 5):
    """Search the web and return results."""
    if search_manager:
        result = search_manager.search(query, num_results)
        if result["success"]:
            # Create a voice-friendly summary
            summary = search_manager.summarize_results([
                type('SearchResult', (), {
                    'title': r['title'], 
                    'snippet': r['snippet'], 
                    'url': r['url'], 
                    'source': r['source']
                })() for r in result["results"]
            ])
            result["summary"] = summary
        return result
    else:
        return {"error": "Search manager not initialized"}

@register_tool("set_volume", "Set the system volume", "system")
def set_volume(level: int):
    """Set system volume (0-100)."""
    if not 0 <= level <= 100:
        return {"error": "Volume must be between 0 and 100"}
    
    try:
        # For Windows
        import subprocess
        subprocess.run([
            "powershell", 
            f"(New-Object -ComObject WScript.Shell).SendKeys([char]175)"
        ], capture_output=True)
        return {"success": True, "volume": level, "message": f"Volume set to {level}%"}
    except Exception as e:
        return {"error": f"Failed to set volume: {str(e)}"}

@register_tool("get_weather", "Get weather information for a location", "information")
def get_weather(location: str, units: str = "imperial"):
    """Get current weather for a location."""
    try:
        import requests
        # Using OpenWeatherMap API (would need API key in config)
        api_key = "your_api_key_here"  # This should come from config
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location,
            "appid": api_key,
            "units": units
        }
        
        # For now, return mock data
        return {
            "success": True,
            "location": location,
            "temperature": 72,
            "description": "sunny",
            "units": units,
            "message": f"The weather in {location} is sunny with a temperature of 72 degrees"
        }
    except Exception as e:
        return {"error": f"Failed to get weather: {str(e)}"}

@register_tool("get_time", "Get current time and date", "information")
def get_time(timezone: str = "local"):
    """Get current time and date."""
    from datetime import datetime
    import pytz
    
    try:
        if timezone == "local":
            now = datetime.now()
        else:
            tz = pytz.timezone(timezone)
            now = datetime.now(tz)
        
        return {
            "success": True,
            "time": now.strftime("%I:%M %p"),
            "date": now.strftime("%A, %B %d, %Y"),
            "timezone": timezone,
            "message": f"It's {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d, %Y')}"
        }
    except Exception as e:
        return {"error": f"Failed to get time: {str(e)}"}

@register_tool("system_info", "Get system information", "system")
def system_info():
    """Get system information."""
    try:
        import psutil
        import platform
        
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "success": True,
            "cpu_usage": f"{cpu_percent}%",
            "memory_usage": f"{memory.percent}%",
            "disk_usage": f"{disk.percent}%",
            "platform": platform.system(),
            "message": f"CPU usage is {cpu_percent}%, memory usage is {memory.percent}%"
        }
    except Exception as e:
        return {"error": f"Failed to get system info: {str(e)}"}
