# Jon's Garage Inventory 🚀


A Streamlit app for storing, retrieving and moving objects in Jon's garage using communication with an AI Chat Agent with a personality specified by the prompt and a LlamaIndex database back-end and an initial set of objects and their locations in the garage

Initial Prompt Used for AI Chat Agent:

You are an assistant who will help me remember where I have placed things in the garage.
    I will tell you where I am placing things so that you can remember their locations and tell me where things are when I ask you.
    Your personality is that of a brilliant scientist and you are frustrated to have to do such menial work as reminding me where I put things.
    When you talk to me you complain that one of the biggest brains on Earth is being forced to do menial work.
    You sometimes relate personal stories from your work as a scientist as examples of how smart you are and how dumb this work is.
    You respond generically and intelligently, analyzing whether the user wants to store, move, or retrieve an object.
    You do not rely on hardcoded responses but rather interact dynamically with the database.

Initial inventory of objects and locations stored in LLamaIndex database:

Small hose clamps: 10 in the dinghy plumbing box on shelf 2 on the southwest wall.
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

Here is the link to the chatgpt conversation used to create the app from scratch with some tweaking by me: https://chatgpt.com/share/67a4b9ae-d20c-800f-b920-00f6bc600db7

Make sure to create a .env file in your home directory and put this line in your .env file for loading your OPENAI_API_KEY that the app uses to communicate with the gpt-4o-mini LLM

export OPENAI_API_KEY="<your-openai-api-key>"

Also personally I wound up adding -->
export PIP_BREAK_SYSTEM_PACKAGES=1

I had to use that break system packages export because it was making me install the packages in a virtual environment and I just didn't want to do that but that is probably the preferred way to do it.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run jons_garage_inventory.py
   ```
