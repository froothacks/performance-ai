threads = [
    {
        "thread_id": 1,
        "messages": [
            ("Advait", "@Elliot when's Feature A available?"),
            ("Elliot", "@Advait soon sry"),
            ("Advait", "WDYM soon?"),
            ("Elliot", "EOD"),
            ("Advait", "but you said EOD yesterday"),
            ("Elliot", "yes but it's actually EOD today"),
        ],
    },
    {
        "thread_id": 2,
        "messages": [
            ("Advait", "@Elliot when's Feature B available?"),
            ("Elliot", "@Advait it's ready now!"),
            ("Advait", "great, I'll test it out"),
            ("Elliot", "sounds good"),
            ("Advait", "I tested it out, it's not working"),
            ("Elliot", "oh, I'll take a look"),
            ("Advait", "thanks"),
            ("Elliot", "I fixed it, it should work now"),
            ("Advait", "thanks, it works now"),
            ("Elliot", "great"),
            ("Advait", "I have another question"),
            ("Elliot", "sry just a sec"),
            ("Advait", "no worries"),
            ("Elliot", "what's up?"),
            ("Advait", "I'm having trouble with Feature C"),
            ("Elliot", "sry IDK"),
        ],
    },
    {
        "thread_id": 3,
        "messages": [
            ("Advait", "@Elliot good work on Feature D"),
            ("Elliot", "@Advait thanks"),
            ("Advait", "you completed it right on time"),
        ],
    },
    {
        "thread_id": 4,
        "messages": [
            ("Advait", "@Elliot who was that person you were talking to?"),
            ("Elliot", "@Advait what person?"),
            ("Advait", "the person you were talking to about Feature E"),
            ("Elliot", "oh, that was my friend"),
            ("Advait", "why were you talking to your friend about Feature E?"),
            ("Elliot", "I was just asking for advice"),
            ("Advait", "what kind of advice?"),
            ("Elliot", "I was asking for advice on how to implement Feature E"),
            ("Advait", "Feature E is a secret"),
        ],
    },
]


def format_thread(thread):
    messages = "\n".join(
        [f"{author}: {message}" for author, message in thread["messages"]]
    )
    return f"Thread {thread['thread_id']}:\n{messages}\n"


import os

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

import asyncio
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import anthropic

filter_template = """
{thread}

I am writing a performance review for {name}. I want to note that {review}.

Does this thread provide any evidence for that?

You MUST respond with only "yes" or "no", nothing else. Do not response with anything but "yes" or "no".
"""

human_prompt = filter_template.format(
    name="Elliot",
    review="Elliot is inconsistent with deadlines",
    thread=format_thread(threads[0]),
)

# anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)
# completion = anthropic.completions.create(
#     model="claude-2",
#     max_tokens_to_sample=300,
#     prompt=f"{HUMAN_PROMPT} {human_prompt}{AI_PROMPT}",
# )
# print(completion.completion)


def format_threads(threads):
    return "\n\n".join([format_thread(thread) for thread in threads])


synthesize_template = """
{threads}

I am writing a performance review for {name}. I want to note that {review}.

Do any of these threads provide evidence for that?

If so, respond with the thread ID and a one-sentence explanation of the evidence.
If not, respond with "None".

Respond exactly according to the following format.
{schema}

For example:
1: Elliot initially said that Feature A would be ready EOD yesterday, but it was actually ready EOD today.

You must not prefix the thread ID with anything, including "thread".
Do not respond with anything but the thread ID and a one-sentence explanation.
"""


from jsonformer_claude.main import JsonformerClaude

anthropic = anthropic.Client(api_key=ANTHROPIC_API_KEY)

relevant_threads_schema = {
    "title": "Relevant Evidence Threads Schema",
    "type": "object",
    "properties": {
        "threads": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "thread_id": {"type": "number"},
                    "evidence_synthesis": {"type": "string"},
                },
            },
        },
    },
}

# gen_json = JsonformerClaude(
#     anthropic_client=anthropic,
#     json_schema=relevant_threads_schema,
#     prompt=synthesize_template.format(
#         name="Elliot",
#         review="Elliot is inconsistent with deadlines",
#         threads=format_threads(threads),
#     ),
#     debug=True,
# )


# async def complete():
#     res = await gen_json()
#     print(res)


# # Run the event loop
# asyncio.run(complete())


anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)
completion = anthropic.completions.create(
    model="claude-2",
    max_tokens_to_sample=300,
    prompt=f"""{HUMAN_PROMPT} {synthesize_template.format(
        name="Elliot",
        review="Elliot is acting as a corporate spy for a competitor",
        threads=format_threads(threads),
        schema="thread_id: 1-sentence explanation",
    )}{AI_PROMPT}""",
)
print(completion.completion)
