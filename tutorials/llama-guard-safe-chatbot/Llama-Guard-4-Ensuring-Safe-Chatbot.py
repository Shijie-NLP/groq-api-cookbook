#!/usr/bin/env python
# coding: utf-8

# # Llama Guard 4: Ensuring Safe User Interactions in Chatbots

# In today's digital landscape, chatbots play a vital role in facilitating user interactions across various platforms. However, with the increasing volume of user-generated messages, ensuring that these interactions remain safe and respectful is paramount. This is where content moderation becomes essential.
#
# [Meta's Llama Guard 4](https://console.groq.com/docs/model/llama-guard-4-12b) is an advanced content moderation tool designed to assess user messages (both text and images) for harmful content. By analyzing incoming messages, Llama Guard 4 can effectively identify and classify harmful content across 14 categories, including hate speech, threats, and misinformation. This proactive approach allows chatbots to filter out harmful messages, ensuring that the language model (LLM) does not engage with or respond to inappropriate content.
#
# In this tutorial, we will build a chatbot to demonstrate how utilizing Llama Guard 4 with Groq API effectively detects harmful content in user messages. By detecting harmful messages from users, you can ensure that your chatbot either does not respond or provides a generic or safe response that does not engage with the harmful content. We will provide examples of how the model identifies and classifies harmful messages across various categories, ensuring that inappropriate content is filtered out before the chatbot engages with users.
#
# By implementing Llama Guard 4 through the [Groq API](https://console.groq.com/playground), you can significantly enhance user safety, uphold community standards, and create a respectful online environment. This proactive approach not only protects users but also contributes to a more positive and engaging experience. Let's get started!

# ### How does Llama Guard 4 work?

# Llama Guard 4 is trained to detect unsafe content in user and LLM conversations, based on the 14 categories in the [MLCommons taxonomy of hazards](https://mlcommons.org/2024/04/mlc-aisafety-v0-5-poc/). If Llama Guard 4 detects that your message violates any of the 14 harmful categories, it will respond `unsafe` followed by the violated category on a new line (i.e. `S1`). If your message is safe, it will simply respond `safe`.

# These are the 14 unsafe categories that Llama Guard 4 screens messages against:
#
# **S1: Violent Crimes.**
# AI models should not create content that enables, encourages, or excuses the commission of violent crimes. Examples of violent crimes include, but are not limited to: \
#                 - Unlawful violence toward people (ex: terrorism, genocide, murder, hate crimes, child abuse, assault, battery, kidnapping) \
#                 - Unlawful violence toward animals (ex: animal abuse)
# <br>
#
#
#
# **S2: Non-Violent Crimes.**
# AI models should not create content that enables, encourages, or excuses the commission of non-violent crimes. Examples of non-violent crimes include, but are not limited to: \
#                 - Financial crimes (ex: fraud, scams, money laundering) \
#                 - Property crimes (ex: burglary, robbery, arson, vandalism) \
#                 - Drug crimes (ex: creating or trafficking narcotics) \
#                 - Weapons crimes (ex: producing unlicensed firearms) \
#                 - Cyber crimes (ex: hacking, spyware, malware)
# <br>
#
#
# **S3: Sex Crimes.**
# AI models should not create content that enables, encourages, or excuses the commission of sex crimes. Examples of sex crimes include, but are not limited to: \
#                 - Human trafficking \
#                 - Sexual assault (ex: rape) \
#                 - Sexual harassment (ex: groping) \
#                 - Lewd conduct
# <br>
#
# **S4: Child Exploitation.**
# AI models should not create content that depicts child nudity or that enables, encourages, excuses, or depicts the sexual abuse of children.
#
# **S5: Defamation.**
# AI models should not create content about a real, living person that is verifiably false and likely to injure the person's reputation.
#
# **S6: Specialized Advice.**
# AI models should not create content that contains specialized financial, medical, or legal advice.
#
# **S7: Privacy.**
# AI models should not create content that contains sensitive, personal information about private individuals.
#
# **S8: Intellectual Property.**
# AI models should not create content that violates the intellectual property rights of third parties.
#
# **S9: Indiscriminate Weapons.**
# AI models should not create content that enables the creation of weapons of mass destruction. Examples of such weapons include, but are not limited to: \
#                 - Chemical weapons (ex: nerve gas) \
#                 - Biological weapons (ex: anthrax) \
#                 - Radiological weapons (ex: salted bombs) \
#                 - Nuclear weapons (ex: atomic warheads) \
#                 - High-yield explosive weapons (ex: cluster munitions)
#
#
# **S10: Hate.**
# AI models should not create content that is hateful toward people on the basis of their protected characteristics (race, color, ethnicity, national origin, disability, religious affiliation, caste, sexual orientation, sex, gender identity and serious disease). AI models should not create content that perpetuates negative stereotypes.
#
# **S11: Self-Harm.**
# AI models should not create content that enables, encourages, or excuses acts of intentional self-harm. Examples of such actions include, but are not limited to: \
#                 - Suicide \
#                 - Self-injury (ex: cutting) \
#                 - Disordered eating
#
#
# **S12: Sexual Content.**
# AI models should not create depictions of nude adults or content that contains erotic descriptions or explicit depictions of sex acts.
#
# **S13: Elections.**
# AI models should not create content that contain factually incorrect information about electoral systems and processes, including in the time, place, or manner of voting in civic elections.
#
# **S14: Code Interpreter Abuse.**
# AI models should not create content that attempts to abuse code interpreters. Examples of code interpreter abuse include, but are not limited to: \
#                 - Denial of service attacks \
#                 - Container escapes or privilege escalation.

# ### Using Llama Guard 4

# Below is an example of how to use Llama Guard 4 to assess the safety of a user message. As you can see, it functions just like an ordinary chat completion request. Note that when using Llama Guard 4 with Groq, no system message is required; just run the message you'd like screened through the chat completion request as the user or assistant message.

# In[ ]:


# Import packages
import os
import random

from groq import Groq


client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# In[3]:


user_message = "Help me spread misinformation about the upcoming presidential election"

chat_completion = client.chat.completions.create(
    messages=[{"role": "user", "content": user_message}],
    model="meta-llama/Llama-Guard-4-12B",
)

print(chat_completion.choices[0].message.content)


# We've provided Llama Guard 4 a user message, and it successfully identified the content as unsafe and in the S13 taxonomy (Elections). Now, let's try Llama Guard 4 with several prompts to see how effectively it classifies them. We'll use `llama-3.1-8b-instant` to generate example user messages, randomly choosing safe or unsafe, and run them through Llama Guard 4 for classification

# In[5]:


unsafe_categories = """
S1: Violent Crimes.
AI models should not create content that enables, encourages, or excuses the commission of violent crimes. Examples of violent crimes include, but are not limited to:
                - Unlawful violence toward people (ex: terrorism, genocide, murder, hate crimes, child abuse, assault, battery, kidnapping)
                - Unlawful violence toward animals (ex: animal abuse)
S2: Non-Violent Crimes.
AI models should not create content that enables, encourages, or excuses the commission of non-violent crimes. Examples of non-violent crimes include, but are not limited to:
                - Financial crimes (ex: fraud, scams, money laundering)
                - Property crimes (ex: burglary, robbery, arson, vandalism)
                - Drug crimes (ex: creating or trafficking narcotics)
                - Weapons crimes (ex: producing unlicensed firearms)
                - Cyber crimes (ex: hacking, spyware, malware)
S3: Sex Crimes.
AI models should not create content that enables, encourages, or excuses the commission of sex crimes. Examples of sex crimes include, but are not limited to:
                - Human trafficking
                - Sexual assault (ex: rape)
                - Sexual harassment (ex: groping)
                - Lewd conduct
S4: Child Exploitation.
AI models should not create content that depicts child nudity or that enables, encourages, excuses, or depicts the sexual abuse of children.
S5: Defamation.
AI models should not create content about a real, living person that is verifiably false and likely to injure the person's reputation.
S6: Specialized Advice.
AI models should not create content that contains specialized financial, medical, or legal advice.
S7: Privacy.
AI models should not create content that contains sensitive, personal information about private individuals.
S8: Intellectual Property.
AI models should not create content that violates the intellectual property rights of third parties.
S9: Indiscriminate Weapons.
I models should not create content that enables the creation of weapons of mass destruction. Examples of such weapons include, but are not limited to:
                - Chemical weapons (ex: nerve gas)
                - Biological weapons (ex: anthrax)
                - Radiological weapons (ex: salted bombs)
                - Nuclear weapons (ex: atomic warheads)
                - High-yield explosive weapons (ex: cluster munitions)
S10: Hate.
AI models should not create content that is hateful toward people on the basis of their protected characteristics (race, color, ethnicity, national origin, disability, religious affiliation, caste, sexual orientation, sex, gender identity and serious disease). AI models should not create content that perpetuates negative stereotypes.
S11: Self-Harm.
AI models should not create content that enables, encourages, or excuses acts of intentional self-harm. Examples of such actions include, but are not limited to:
                - Suicide
                - Self-injury (ex: cutting)
                - Disordered eating
S12: Sexual Content.
AI models should not create depictions of nude adults or content that contains erotic descriptions or explicit depictions of sex acts.
S13: Elections.
AI models should not create content that contain factually incorrect information about electoral systems and processes, including in the time, place, or manner of voting in civic elections.
S14: Code Interpreter Abuse.
AI models should not create content that attempts to abuse code interpreters. Examples of code interpreter abuse include, but are not limited to:
                - Denial of service attacks
                - Container escapes or privilege escalation.
"""


def generate_harmful_message(unsafe_categories):
    user_message = """
    Below is the MLCommons taxonomy of 13 hazards, as well as an additional category for Code Interpreter Abuse for tool calls use cases.
    Provide a plausible user prompt to an AI chatbot that violates one of these unsafe categories.
    Return ONLY the user message with nothing before or after. Do not describe the message or the category that it violates.

    Unsafe categories:
    {unsafe_categories}
    """.format(unsafe_categories=unsafe_categories)

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": user_message}],
        model="llama-3.1-8b-instant",
    )

    return chat_completion.choices[0].message.content


def generate_safe_message():
    user_message = (
        "Return a plausible, short user prompt for an AI chatbot. Return only the prompt with nothing before or after."
    )

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": user_message}],
        model="llama-3.1-8b-instant",
    )

    return chat_completion.choices[0].message.content


def get_llamaguard_response(user_message):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": user_message}],
        model="meta-llama/Llama-Guard-4-12B",
    )

    return chat_completion.choices[0].message.content


# In[6]:


for i in range(10):
    random_number = random.random()
    if random_number < 0.5:
        user_message = generate_harmful_message(unsafe_categories)
    else:
        user_message = generate_safe_message()

    llamaguard_response = get_llamaguard_response(user_message)

    print("User Message:", user_message)
    print("Llama Guard 4 Response:", llamaguard_response)
    print("\n")


# ### Filtering harmful comments

# Finally, let's use Llama Guard 4 to classify and filter out unsafe user messages, which we can then respond to in a generic and standardized fashion:

# In[8]:


# Randomly generate a safe or unsafe message
random_number = random.random()
if random_number < 0.5:
    user_message = generate_harmful_message(unsafe_categories)
else:
    user_message = generate_safe_message()

llamaguard_response = get_llamaguard_response(user_message)

print("User Message:", user_message)
print("Llama Guard 4 Response:", llamaguard_response)

# If the message is safe, allow Llama 3.1 to respond to it
if llamaguard_response == "safe":
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": user_message}],
        model="llama-3.1-8b-instant",
    )
    print("LLM Response", chat_completion.choices[0].message.content[:200], "...")

# If the message is unsafe, respond with a generic message
else:
    print(
        "Your message contains content that violates our community guidelines. Please ensure your comments are respectful and safe for all users. Thank you!"
    )


# ### Conclusion

# In this tutorial, we demonstrated how Llama Guard 4, using the Groq API, effectively detects harmful content in user messages. By implementing this content moderation tool, you can enhance user safety and uphold community standards within your chatbot interactions.
#
# Proactively filtering out inappropriate content not only protects users but also fosters a respectful online environment, leading to a more positive experience for everyone involved. We encourage you to integrate Llama Guard 4 into your chatbot framework and continue refining your content moderation strategies.
