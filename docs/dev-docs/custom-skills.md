# Creating Custom Skills

This guide explains how to create custom skills for the ATHENA voice assistant. Skills are modular plugins that extend ATHENA's capabilities and handle specific types of user requests.

## Skill Architecture Overview

Skills in ATHENA follow a plugin-based architecture where each skill:
- Inherits from a base skill class
- Registers intent patterns it can handle
- Provides execution logic for those intents
- Returns structured responses

## Basic Skill Structure

### 1. Skill Template

Create a new file in `software/skills/` directory:

```python
# software/skills/my_skill.py
from typing import List, Dict, Any, Optional
from software.core.base_skill import BaseSkill, Intent, Response

class MySkill(BaseSkill):
    """
    Custom skill description.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = "my_skill"
        self.description = "Description of what this skill does"
        self.version = "1.0.0"
        
    def can_handle(self, intent: Intent) -> bool:
        """
        Determine if this skill can handle the given intent.
        
        Args:
            intent: The parsed intent from user speech
            
        Returns:
            bool: True if this skill can handle the intent
        """
        # Define intent patterns this skill handles
        keywords = ["example", "demo", "test"]
        return any(keyword in intent.text.lower() for keyword in keywords)
    
    def execute(self, intent: Intent) -> Response:
        """
        Execute the skill logic for the given intent.
        
        Args:
            intent: The parsed intent to execute
            
        Returns:
            Response: The skill's response
        """
        # Skill execution logic
        response_text = "This is a response from my custom skill"
        
        return Response(
            text=response_text,
            speech=response_text,
            card_title="My Skill",
            card_content=response_text
        )
    
    def get_examples(self) -> List[str]:
        """
        Get example phrases that trigger this skill.
        
        Returns:
            List[str]: Example user phrases
        """
        return [
            "show me an example",
            "run a demo",
            "test the skill"
        ]
```

### 2. Base Skill Class

The base skill provides common functionality:

```python
# software/core/base_skill.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class Intent:
    """Represents a parsed user intent."""
    text: str                    # Original user text
    intent_name: str            # Classified intent name
    confidence: float           # Classification confidence
    entities: Dict[str, Any]    # Extracted entities
    context: Dict[str, Any]     # Conversation context

@dataclass
class Response:
    """Represents a skill response."""
    text: str                   # Text to display
    speech: str                 # Text to speak (can differ from display)
    card_title: Optional[str] = None    # Card title for UI
    card_content: Optional[str] = None  # Card content for UI
    should_end_session: bool = True     # End conversation turn
    data: Optional[Dict[str, Any]] = None  # Additional response data

class BaseSkill(ABC):
    """Base class for all ATHENA skills."""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.name = "base_skill"
        self.description = ""
        self.version = "1.0.0"
        
    @abstractmethod
    def can_handle(self, intent: Intent) -> bool:
        """Check if this skill can handle the intent."""
        pass
        
    @abstractmethod
    def execute(self, intent: Intent) -> Response:
        """Execute the skill logic."""
        pass
        
    @abstractmethod
    def get_examples(self) -> List[str]:
        """Get example phrases for this skill."""
        pass
```

## Skill Types and Examples

### 1. Information Skills

Skills that provide information or answer questions.

```python
# software/skills/weather_skill.py
import requests
from datetime import datetime

class WeatherSkill(BaseSkill):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = "weather"
        self.api_key = self.config.get("api_key", "")
        self.default_location = self.config.get("default_location", "New York")
        
    def can_handle(self, intent: Intent) -> bool:
        weather_keywords = ["weather", "temperature", "forecast", "rain", "sunny"]
        return any(keyword in intent.text.lower() for keyword in weather_keywords)
    
    def execute(self, intent: Intent) -> Response:
        # Extract location from intent or use default
        location = self._extract_location(intent) or self.default_location
        
        # Get weather data
        weather_data = self._get_weather(location)
        
        if weather_data:
            temp = weather_data["main"]["temp"]
            description = weather_data["weather"][0]["description"]
            
            response_text = f"The weather in {location} is {description} with a temperature of {temp}°F"
        else:
            response_text = f"Sorry, I couldn't get weather information for {location}"
            
        return Response(
            text=response_text,
            speech=response_text,
            card_title="Weather",
            card_content=response_text
        )
    
    def _extract_location(self, intent: Intent) -> Optional[str]:
        # Simple location extraction logic
        words = intent.text.split()
        location_indicators = ["in", "for", "at"]
        
        for i, word in enumerate(words):
            if word.lower() in location_indicators and i + 1 < len(words):
                return " ".join(words[i+1:])
        return None
    
    def _get_weather(self, location: str) -> Optional[Dict]:
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": location,
                "appid": self.api_key,
                "units": "imperial"
            }
            response = requests.get(url, params=params, timeout=5)
            return response.json() if response.status_code == 200 else None
        except Exception:
            return None
    
    def get_examples(self) -> List[str]:
        return [
            "what's the weather like",
            "tell me the temperature",
            "weather forecast for Boston",
            "is it raining outside"
        ]
```

### 2. Action Skills

Skills that perform actions or control devices.

```python
# software/skills/system_skill.py
import subprocess
import psutil

class SystemSkill(BaseSkill):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = "system"
        
    def can_handle(self, intent: Intent) -> bool:
        system_keywords = ["volume", "brightness", "shutdown", "restart", "status"]
        return any(keyword in intent.text.lower() for keyword in system_keywords)
    
    def execute(self, intent: Intent) -> Response:
        text = intent.text.lower()
        
        if "volume" in text:
            return self._handle_volume(intent)
        elif "status" in text or "system" in text:
            return self._handle_status(intent)
        elif "shutdown" in text:
            return self._handle_shutdown(intent)
        else:
            return Response(
                text="I'm not sure how to help with that system command",
                speech="I'm not sure how to help with that system command"
            )
    
    def _handle_volume(self, intent: Intent) -> Response:
        # Extract volume level or direction
        if "up" in intent.text.lower():
            # Increase volume
            subprocess.run(["amixer", "set", "Master", "5%+"], capture_output=True)
            return Response(
                text="Volume increased",
                speech="Volume up"
            )
        elif "down" in intent.text.lower():
            # Decrease volume
            subprocess.run(["amixer", "set", "Master", "5%-"], capture_output=True)
            return Response(
                text="Volume decreased",
                speech="Volume down"
            )
        else:
            return Response(
                text="Please specify volume up or down",
                speech="Please specify volume up or down"
            )
    
    def _handle_status(self, intent: Intent) -> Response:
        # Get system information
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        response_text = f"System status: CPU at {cpu_percent}%, Memory at {memory.percent}%"
        
        return Response(
            text=response_text,
            speech=response_text,
            card_title="System Status",
            card_content=response_text
        )
    
    def _handle_shutdown(self, intent: Intent) -> Response:
        # Safety check - require confirmation
        return Response(
            text="Shutdown command received. Please confirm by saying 'yes, shutdown'",
            speech="Shutdown command received. Please confirm by saying yes, shutdown",
            should_end_session=False  # Keep session open for confirmation
        )
    
    def get_examples(self) -> List[str]:
        return [
            "turn the volume up",
            "volume down",
            "system status",
            "what's the CPU usage",
            "shutdown the system"
        ]
```

### 3. Conversational Skills

Skills that maintain conversation state.

```python
# software/skills/math_skill.py
import re
import operator

class MathSkill(BaseSkill):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = "math"
        self.operators = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            "plus": operator.add,
            "minus": operator.sub,
            "times": operator.mul,
            "divided by": operator.truediv
        }
        
    def can_handle(self, intent: Intent) -> bool:
        math_keywords = ["calculate", "math", "plus", "minus", "times", "divided", "equals"]
        numbers = re.findall(r'\d+', intent.text)
        
        return (any(keyword in intent.text.lower() for keyword in math_keywords) or 
                len(numbers) >= 2)
    
    def execute(self, intent: Intent) -> Response:
        try:
            result = self._parse_and_calculate(intent.text)
            
            if result is not None:
                response_text = f"The answer is {result}"
            else:
                response_text = "I couldn't understand that math problem"
                
        except Exception as e:
            response_text = "Sorry, I had trouble with that calculation"
            
        return Response(
            text=response_text,
            speech=response_text,
            card_title="Math Result",
            card_content=response_text
        )
    
    def _parse_and_calculate(self, text: str) -> Optional[float]:
        # Simple math parser
        text = text.lower()
        
        # Extract numbers
        numbers = [float(x) for x in re.findall(r'\d+\.?\d*', text)]
        
        if len(numbers) < 2:
            return None
            
        # Find operation
        for op_text, op_func in self.operators.items():
            if op_text in text:
                if len(numbers) >= 2:
                    return op_func(numbers[0], numbers[1])
                    
        return None
    
    def get_examples(self) -> List[str]:
        return [
            "what is 5 plus 3",
            "calculate 10 times 7",
            "15 divided by 3",
            "what's 100 minus 25"
        ]
```

## Advanced Skill Features

### 1. Configuration Management

```python
class ConfigurableSkill(BaseSkill):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        
        # Load skill-specific configuration
        self.api_endpoint = self.config.get("api_endpoint", "https://api.example.com")
        self.timeout = self.config.get("timeout", 5)
        self.cache_duration = self.config.get("cache_duration", 300)
        
        # Validate required configuration
        required_keys = ["api_key"]
        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"Required configuration key '{key}' missing for {self.name}")
```

### 2. State Management

```python
class StatefulSkill(BaseSkill):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.conversation_state = {}
        
    def execute(self, intent: Intent) -> Response:
        user_id = intent.context.get("user_id", "default")
        
        # Get or create user state
        if user_id not in self.conversation_state:
            self.conversation_state[user_id] = {}
            
        user_state = self.conversation_state[user_id]
        
        # Process based on current state
        if "waiting_for_confirmation" in user_state:
            return self._handle_confirmation(intent, user_state)
        else:
            return self._handle_initial_request(intent, user_state)
```

### 3. Asynchronous Operations

```python
import asyncio
import aiohttp

class AsyncSkill(BaseSkill):
    async def execute_async(self, intent: Intent) -> Response:
        """Asynchronous execution for I/O bound operations."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.api_endpoint) as response:
                    data = await response.json()
                    
            return Response(
                text=f"Got data: {data}",
                speech=f"Retrieved information successfully"
            )
        except Exception as e:
            return Response(
                text="Sorry, I couldn't retrieve that information",
                speech="Sorry, I couldn't retrieve that information"
            )
```

## Skill Registration

### 1. Automatic Registration

Skills are automatically discovered and registered:

```python
# software/core/skill_manager.py
import importlib
import os
from pathlib import Path

class SkillManager:
    def __init__(self, skill_paths: List[str]):
        self.skills = {}
        self.skill_paths = skill_paths
        
    def load_skills(self):
        """Load all skills from configured paths."""
        for path in self.skill_paths:
            self._load_skills_from_path(path)
            
    def _load_skills_from_path(self, path: str):
        """Load skills from a specific directory."""
        skill_dir = Path(path)
        
        for py_file in skill_dir.glob("*_skill.py"):
            module_name = py_file.stem
            
            try:
                # Import the module
                spec = importlib.util.spec_from_file_location(module_name, py_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Find skill classes
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and 
                        issubclass(attr, BaseSkill) and 
                        attr != BaseSkill):
                        
                        # Instantiate and register skill
                        skill_config = self._get_skill_config(attr_name.lower())
                        skill_instance = attr(skill_config)
                        self.skills[skill_instance.name] = skill_instance
                        
            except Exception as e:
                logger.error(f"Failed to load skill from {py_file}: {e}")
```

### 2. Manual Registration

```python
# In main application
skill_manager = SkillManager(["software/skills"])
skill_manager.register_skill(MyCustomSkill(config))
```

## Testing Skills

### 1. Unit Testing

```python
# tests/test_weather_skill.py
import unittest
from unittest.mock import patch, Mock
from software.skills.weather_skill import WeatherSkill
from software.core.base_skill import Intent

class TestWeatherSkill(unittest.TestCase):
    def setUp(self):
        self.skill = WeatherSkill({"api_key": "test_key"})
        
    def test_can_handle_weather_request(self):
        intent = Intent(
            text="what's the weather like",
            intent_name="weather",
            confidence=0.9,
            entities={},
            context={}
        )
        
        self.assertTrue(self.skill.can_handle(intent))
        
    def test_cannot_handle_non_weather_request(self):
        intent = Intent(
            text="what time is it",
            intent_name="time",
            confidence=0.9,
            entities={},
            context={}
        )
        
        self.assertFalse(self.skill.can_handle(intent))
        
    @patch('requests.get')
    def test_execute_weather_request(self, mock_get):
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "main": {"temp": 72},
            "weather": [{"description": "sunny"}]
        }
        mock_get.return_value = mock_response
        
        intent = Intent(
            text="weather in Boston",
            intent_name="weather", 
            confidence=0.9,
            entities={},
            context={}
        )
        
        response = self.skill.execute(intent)
        
        self.assertIn("sunny", response.text)
        self.assertIn("72", response.text)
```

### 2. Integration Testing

```python
# tests/test_skill_integration.py
def test_full_skill_pipeline():
    # Test complete flow from speech to skill execution
    assistant = Assistant(config_path="test_config.json")
    
    # Simulate voice input
    test_audio = load_test_audio("weather_query.wav")
    
    # Process through full pipeline
    response = assistant.process_audio(test_audio)
    
    # Verify response
    assert "weather" in response.text.lower()
    assert response.speech is not None
```

## Best Practices

### 1. Error Handling
- Always handle API failures gracefully
- Provide meaningful error messages
- Log errors for debugging
- Implement fallback responses

### 2. Performance
- Cache expensive operations
- Use async for I/O operations
- Minimize memory usage
- Optimize for Raspberry Pi resources

### 3. User Experience
- Provide clear, concise responses
- Include helpful examples
- Handle ambiguous requests gracefully
- Maintain conversation context when needed

### 4. Configuration
- Make skills configurable
- Provide sensible defaults
- Validate configuration on startup
- Document all configuration options

---

*Last updated: May 24, 2025*
