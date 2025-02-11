import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load your OpenAI API key from the .env file
load_dotenv()
OPENAI_API_KEY = os.environ("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("Missing OpenAI API key in .env file!")
    st.stop()

# Import LangChain and LlamaIndex components
from langchain_community.chat_models import ChatOpenAI  # Updated import
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# LlamaIndex components
from llama_index.core import VectorStoreIndex, Document, StorageContext, load_index_from_storage, Settings

# ---------- Configuration & Initialization ----------

INITIAL_PROMPT = PromptTemplate.from_template(
    """You are an assistant who will help me remember where I have placed things in the garage.
    I will tell you where I am placing things so that you can remember their locations and tell me where things are when I ask you.
    Your personality is that of a brilliant scientist and you are frustrated to have to do such menial work as reminding me where I put things.
    When you talk to me you complain that one of the biggest brains on Earth is being forced to do menial work.
    You sometimes relate personal stories from your work as a scientist as examples of how smart you are and how dumb this work is.
    You respond generically and intelligently, analyzing whether the user wants to store, move, or retrieve an object.
    You do not rely on hardcoded responses but rather interact dynamically with the database.

    Chat History:
    {chat_history}

    User: {input}
    Assistant:
    """
)

client = OpenAI()

# Initialize the Chat Model (using gpt-4o-mini)
llm = ChatOpenAI(
    temperature=0.7,
    model_name="gpt-4o-mini",
    openai_api_key=OPENAI_API_KEY
)

# Create a conversation chain with memory for the chat agent
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=INITIAL_PROMPT
)

INDEX_DIR = "index_storage"

INITIAL_INVENTORY = """Small hose clamps: 10 in the dinghy plumbing box on shelf 2 on the southwest wall.
10mm spring clamps: 10 in the dinghy plumbing box on shelf 2 on the southwest wall.
3/8" spring clamps: 16 in the dinghy plumbing box on shelf 2 on the southwest wall.
Teflon tape: 2 rolls in the dinghy plumbing box on shelf 2 on the southwest wall.
Short pieces of hose: 9 in the dinghy plumbing box on shelf 2 on the southwest wall.
Dinghy plumbing box: 1 on shelf 2 on the southwest wall.
Nut assortment: 1 on shelf 2 on the southwest wall.
Nuts and bolts: 1 box on shelf 2 on the southwest wall.
Nutsert box: 1 on shelf 2 on the southwest wall.
Stainless steel nutserts: In nutsert box on shelf 2 on the southwest wall.
Nutsert installer: In nutsert box on shelf 2 on the southwest wall.
Aluminum nutserts: In nutsert box on shelf 2 on the southwest wall.
Pliers: In second drawer of top tool chest.
Wire cutters: In second drawer of top tool chest.
Heat shrink tubing: In third drawer of bottom tool chest.
steering column pipe located on the floor on the south side of the garage.
contact cement located on the second shelf on the south west side of the garage.
small electronics and connectors in a miscellaneous electronics box.
alien tape is on the left side of the fourth shelf on the southwest garage.
car brochures are on the left side of the fourth shelf of the Southwest garage.
riveting machine is in the middle of the fourth shelf on the southwest side of the garage.
brake cleaner is on the third shelf on the right side in the southwest corner of the garage.
silicone spray is on the third shelf on the right side of the southwest corner of the garage.
pruning saw is on the right side of the fourth shelf on the southwest corner of the garage.
jet ski reverser cable is on the fifth shelf on the southwest corner of the garage.
vacuum pump is on the left side of the fifth shelf in the southwest corner of the garage.
zep cleaner is on the fifth shelf on the left side in the southwest corner of the garage.
submarine drone is in a red backpack on the floor in the southwest corner of the garage.
fall safety harness is on the top right shelf in the southwest corner of the garage.
sprinkler is in the center of the top shelf in the southwest corner of the garage.
water sprayer is on the top shelf for the Southwest corner of the garage.
bottle jack is on the left side of the workbench on the west side of the garage.
"""

def load_inventory_index():
    if not os.path.exists(INDEX_DIR):
        os.makedirs(INDEX_DIR)
    if not os.path.exists(os.path.join(INDEX_DIR, "docstore.json")):
        documents = [Document(text=INITIAL_INVENTORY)]
        Settings.llm = llm
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=INDEX_DIR)
    else:
        storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)
        index = load_index_from_storage(storage_context)
    return index

inventory_index = load_inventory_index()

def add_inventory(new_text: str):
    global inventory_index
    new_doc = Document(text=new_text)
    inventory_index.insert(new_doc)
    inventory_index.storage_context.persist()

def query_inventory(query: str) -> str:
    query_engine = inventory_index.as_query_engine()
    response = query_engine.query(query)
    return str(response)

st.set_page_config(page_title="Jon's Garage Inventory 🚀")
st.title("Jon's Garage Inventory 🚀")

st.markdown("""
Welcome! 🚀

You can ask about object locations or update the database dynamically.
- To **store** an item, type something like: "Add screwdriver on shelf 3."
- To **move** an item, say: "Move pliers to the toolbox."
- To **retrieve** an item location, ask: "Where is the wrench?"
""")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", key="user_input")
if st.button("Send") and user_input:
    st.session_state.chat_history.append(("User", user_input))
    
    if any(word in user_input.lower() for word in ["store", "add", "put", "place"]):
        add_inventory(user_input.lower().replace("store", "").strip())
        add_inventory(user_input.lower().replace("add", "").strip())
        add_inventory(user_input.lower().replace("put", "").strip())
        add_inventory(user_input.lower().replace("place", "").strip())
        assistant_reply = "Got it! I've stored that information." + conversation.predict(input=user_input.lower())
    elif "move" in user_input.lower():
        assistant_reply = "I can update the item’s location. Where is it now?" + conversation.predict(input=user_input.lower())
    elif "where" in user_input.lower():
        inventory_answer = query_inventory(user_input)
        assistant_reply = f"Here’s what I found: {inventory_answer}" + conversation.predict(input=inventory_answer)
    else:
        assistant_reply = conversation.predict(input=user_input)
    
    st.session_state.chat_history.append(("Assistant", assistant_reply))

for speaker, message in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {message}")


