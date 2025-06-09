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