---
title: "ATHENA: Open-Source AI Smart Voice Assistant"
author: "Kuber Mehta"
description: "An Open Source, Customizable Smart Speaker that Actually Respects you"
created_at: "2025-05-24"
---

# May 22nd, 2025: Project Kickoff

Today marks the beginning of Project ATHENA, my ambitious attempt to build a smarter, more capable voice assistant than what's currently available commercially. I've been frustrated with the limitations of my Echo Dot - it works for simple commands but falls short on anything complex. With recent advances in AI, I believe we can do much better with open hardware.

I began by researching existing open-source voice assistant projects to understand their architectures and limitations. I looked at:
- Mycroft AI's hardware and software stack
- Various ReSpeaker implementations
- Custom Raspberry Pi voice assistant builds

Main observations:
- Wake word detection is a significant challenge for reliability
- Microphone array quality dramatically affects voice recognition accuracy
- Audio output quality is often overlooked but crucial for user experience
- Local AI processing requires careful optimization for the hardware

Next, I drafted a preliminary BOM and started sketching some initial designs for the hardware layout. I'm particularly excited about incorporating a 6-mic array for superior voice detection and designing a custom case with proper acoustic properties.

a lot of it was setting up this fancy repo

**Total time spent: 3h**

# June 09th, 2025: Welp, Got time to pick it up again

Been a while since I *officially* jounaled here so guess it's a good time to. Been stuck with exams but it'll be much better after this week so I'll get some real time to work on this

Past few days I've been researching more deeper into existing-ish implementations that exist, even played a lot more with Alexa 

Some things I find that we can do different:
- Screen: It... would be a challenge for sure, but I've seen some implementations and they're extremely cool, I want to do it too
- customised wake words: Found a repository to create pipelines for home assistant wakewords, it's.. not easy but we'll try at least 3 wake words and good documentation if the user wants to make their own 
- Model choice: Something decent enough to be fully local but run fast, which is hard, ideally it'll be quantized and may use APIs to connect to other models (probably HF models!?) but that's an extra cost, so not exactly sure
- Mic Arrays: They suck in all Open Source projects or aren't integrated well, usually it's just a cheap mic, using multiple will be very very benificial 

Features that I really want:
- Integration with music apps - I like spotify connect on Alexa, youtube music has a feature like that too but they don't support it, we can do that here, also found a library for apple casting so that would be fun
- custom commands - ideally without making the prompt too long? Gonna be interesting to see how this fits with LLMs

**Total time spent: 6h**

# June 10th, 2025: Actually picking up specifics

Played around with a few models today that can actually run on the hardware as an LLM
As a rule of thumb, we AT LEAST need:
- Whisper Base+ (tiny is really bad) [at least 73M parameters]
- Any sub 1B model for the actual processing [Llama 3.2 1.5B or Qwen 0.6B]
- TTS Model (Kokoro v1.0, about 82M parameters)

So optimistically we can get everything running under at or about under 2B parameters, which is huge 
if it runs well enough, I'd like to experiment with bigger models, but yes, the prompting would have to be greatly worked upon

Here's a very basic idea in my head of how it would work for something like "What is the weather like today?":

**Speech → Text**: Whisper converts speech to "What is the weather like today?"

**Text → Function Call**: LLM analyzes text and outputs:
```json
{"function": "weather", "parameters": {"location": "New Delhi"}}
```

**Function Execution**: Our function registry looks up `weather` and uses a weather API

**Response Generation**: LLM gets the function result and generates a natural response: "The weather in New Delhi is 46 degrees, hope you don't boil to death"

**Text → Speech**: Kokoro TTS converts response to speech with one of the voices we choose

another thing that a lot of open source assistants struggle with at the moment is understanding intent, if you say 
"Turn on the kitchen lights" it would turn it on
"Turn the lights inside the kitchen" might not - which honestly sucks because we don't always say all the sentences exactly same 

Using an LLM completely solves that, which is pretty cool

# June 11th, 2025: Function and Tool Calling

Been thinking more about how to actually make the LLM *do* things, I mean, getting the prompt to mention all the things it can do and functions it can call is obvious but connecting it to things is the actual challenge

What I learnt about **function calling** - when I say "play The Weeknd on Spotify", the LLM needs to:

1. Understand the intent (play music)
2. Extract entities (artist: "The Weeknd", service: "Spotify") 
3. Call the appropriate function: `play_music(artist="The Weeknd", service="spotify")`

Probably only gonna focus on spotify now because free API I think youtube music is free too but with more limitations on the API requests but it isn't documented well so welp.

As I said yesterday, using an LLM for this is WAY better because I can say anything like these and it'll pick it up
- "Put on some Weeknd"
- "I want to hear The Weeknd" 
- "Play music by The Weeknd"
- "Start playing The Weeknd on Spotify"

All map to the same function call.

For implementation (at least for now):
- **Function Registry**: Centralized catalog of available functions
- **Music Integration**: Spotify/YouTube Music APIs with proper auth
- **Web Search**: DuckDuckGo integration for general queries
- **Smart Home**: Eventually IoT device control - maybe integrating with home assistant but that's another beast that I'll touch way later
- **System Functions**: Volume, time, weather, etc.
