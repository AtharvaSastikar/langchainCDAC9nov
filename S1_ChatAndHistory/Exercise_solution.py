import os
import configparser
from langchain_groq import ChatGroq
from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage, SystemMessage
config = configparser.ConfigParser()
from langchain_core.output_parsers import StrOutputParser
config.read('/workspaces/langchainCDAC9nov/config.ini')
groq = config['groq']
cohere = config['cohere']

os.environ['GROQ_API_KEY'] = groq.get('GROQ_API_KEY')
os.environ['COHERE_API_KEY'] = cohere.get('COHERE_API_KEY')

def actor_picker():
    import random
    number=random.randint(1,5)
    messages =[
    SystemMessage(content= 'I am a random actor picker service. Please provide a number between 1 and 5, and I will always return a random Bollywood male actors full name only in two words. '), 
    HumanMessage(content= f"{number}")
]
    model = ChatCohere(model="command-r-plus")
    parser = StrOutputParser()
    chain = model | parser
    response = chain.invoke(messages)

    print(response)
    return response

def location_picker():
    import random
    number=random.randint(1,5)
    messages =[
    SystemMessage(content= 'I am a random location picker service. Please provide a number between 1 and 5, and I will give always you a random name of a beautiful location and its country around the world in one or two words. '), 
    HumanMessage(content= f"{number}")
]
    model = ChatCohere(model="command-r-plus")
    parser = StrOutputParser()
    chain = model | parser
    response = chain.invoke(messages)

    print(response)
    return response
def theme_picker():
    import random
    number=random.randint(1,5)
    messages =[
    SystemMessage(content= 'I am a random movie theme picker service. Please provide a number between 1 and 5, and I will always return you the random theme of movie in a single word. '), 
    HumanMessage(content= f"{number}")
]
    model = ChatCohere(model="command-r-plus")
    parser = StrOutputParser()
    chain = model | parser
    response = chain.invoke(messages)

    print(response)
    return response
    
actor=actor_picker()
location=location_picker()
theme=theme_picker()


from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

system_template = "Return an output in string form as a story reading the output for the input three functions. Please provide a {{size}} related response."

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        ("user", 'Create a story for a movie in which the actor is {actor}, the location is {location} and the theme for the movie is {theme}.Tell the genre, location and starring for the movie and then display story.')  # Use string representation of my_list here
    ]
)
def story_generator():
    model_groq = ChatGroq(model="llama3-8b-8192")
    chain = prompt_template | model_groq | parser

    final_story_output = chain.invoke({"actor":actor,"location":location,"theme":theme})

    print(final_story_output)
    return final_story_output

def story_generator2():
    model = ChatCohere(model="command-r-plus")
    chain = prompt_template | model | parser

    final_story_output = chain.invoke({"actor":actor,"location":location,"theme":theme})

    print(final_story_output)
story=story_generator()
# story_generator()
# story_generator2()

from langchain_core.chat_history import(BaseChatMessageHistory,InMemoryChatMessageHistory,)
from langchain_core.runnables.history import RunnableWithMessageHistory
# store = {}
model = ChatGroq(model="llama3-8b-8192")
# parser = StrOutputParser()
# chain = model | parser
# def get_session_history(session_id: str) -> BaseChatMessageHistory:
#     if session_id not in store:  # If a new session then create a new memory store.
#         store[session_id] = InMemoryChatMessageHistory()
#     return store[session_id]
# config = {'configurable': {"session_id": "Sesssion-1"}}
# newHistory = RunnableWithMessageHistory(model, get_session_history)
# withHistory = RunnableWithMessageHistory(model, get_session_history)
# response = newHistory.invoke([HumanMessage(f'{story}')], config=config)

# print(response.content) # all good so far

# # we dont need to explicitly store the response from the model in history

# response = withHistory.invoke(
#     [HumanMessage(content=input('Tell if you want to make changes to your story? Tell if any: '))], config=config
# )

# print(response.content)



from langchain_core.chat_history import(BaseChatMessageHistory,InMemoryChatMessageHistory,)
import asyncio
store=InMemoryChatMessageHistory()

async def func1():
    store.add_message(HumanMessage(content=f'{story}'))
    messages = await store.aget_messages()
    response = model.invoke(messages)
    print(response.content)
    store.add_message(SystemMessage(content=response.content))
async def func2():
    await asyncio.sleep(2)  # Simulate delay or allow other processes
    # Add a system message for context
    system_message_content = "Please ensure the story aligns with the requested changes and return the output in paragraphs."
    store.add_message(SystemMessage(content=system_message_content))
    
    # Add a human message based on user input
    user_input = input("Tell if you want to make changes to your story: ")
    store.add_message(HumanMessage(content=user_input))

    # Retrieve the updated message history
    messages = await store.aget_messages()
    print("Messages so far:", messages)

    # Invoke the model with the updated history
    response = model.invoke(messages)
    print("Model Response:", response.content)

    # Add the model's response to the chat history
    store.add_message(SystemMessage(content=response.content))

async def main():
    await func1()
    await func2()

# Run the async workflow
story = story_generator()
asyncio.run(main())
                                                                                                     
