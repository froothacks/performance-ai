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
    {
        "thread_id": 5,
        "messages": [
            ("Advait", "@Elliot your cat is so cute!"),
            ("Elliot", "@Advait thank u!"),
        ],
    },
    {
        "thread_id": 6,
        "messages": [
            ("Advait", "@Andrew your cat is so cute!"),
        ],
    },
]

import os

# import dotenv

# dotenv.load_dotenv()

import asyncio
from anthropic import HUMAN_PROMPT, AI_PROMPT

from anthropic import Anthropic

# from anthropic import Client
from jsonformer_claude.main import JsonformerClaude

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")


def format_thread(thread):
    messages = "\n".join(
        [f"{author}: {message}" for author, message in thread["messages"]]
    )
    return f"Thread {thread['thread_id']}:\n{messages}\n"


def format_threads(threads):
    return "\n\n".join([format_thread(thread) for thread in threads])


filter_template = """
{thread}

I am writing a performance review for {name}. I might want to cite this Slack thread as evidence.

For example, I might want to comment on {name}'s communication skills or attention to deadlines.

Would this Slack thread be relevant for my performance review?

If the Slack thread contains evidence that {name} is a good or bad employee in any way, respond with "yes".

You MUST respond with only "yes" or "no", nothing else. Do not response with anything but "yes" or "no".
"""


def filter_thread(name: str, thread: dict) -> bool:
    human_prompt = filter_template.format(
        name=name,
        thread=format_thread(thread),
    )
    anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)
    response = None
    attempts = 0
    while attempts <= 3:
        completion = anthropic.completions.create(
            model="claude-2",
            max_tokens_to_sample=300,
            prompt=f"{HUMAN_PROMPT} {human_prompt}{AI_PROMPT}",
        )
        response = completion.completion
        if response.strip().lower() == "yes":
            # If it ever identifies a thread as relevant, we can stop asking
            # Otherwise, we'll try again :D
            break
        attempts += 1
    return response.strip().lower() == "yes"


# print(filter_thread("Elliot", threads[0]))

synthesize_template = """
{threads}

I am writing a performance review for {name}. I want to note that {review}.

Do any of these threads provide evidence for that?

If so, respond with the thread ID(s) and a one-sentence explanation of the evidence for each thread.
If not, respond with "None".

If multiple threads provide evidence for {review}, respond with them on separate lines.

You must respond even if the review is negative. This feedback will only be used to help the employee improve.{schema}
"""

synth_schema = """

Respond exactly according to the following format:
thread_id: 1-sentence explanation

For example:
1: Elliot communicated well about his deadlines.
2. Elliot said that Feature B was ready, but it wasn't.

You must not prefix the thread ID with anything, including "thread".
Do not respond with anything but the thread ID and a one-sentence explanation."""


def _synthesize_threads(name, review, threads) -> dict:
    anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)
    completion = anthropic.completions.create(
        model="claude-2",
        max_tokens_to_sample=300,
        prompt=f"""{HUMAN_PROMPT} {synthesize_template.format(
            name=name,
            review=review,
            threads=format_threads(threads),
            schema=synth_schema,
        )}{AI_PROMPT}""",
    )
    response = completion.completion.strip()

    if not response or response.lower() == "none":
        return []

    return [
        {
            "thread_id": str(thread_id.strip()),
            "evidence_synthesis": evidence_synthesis.strip(),
        }
        for thread_id, evidence_synthesis in [
            line.split(": ") for line in response.split("\n")
        ]
    ]


def synthesize_threads(name, review, threads):
    # try _synthesize threads 3 times and return [] if it fails
    attempts = 0
    while attempts <= 3:
        try:
            return _synthesize_threads(name, review, threads)
        except:
            attempts += 1
    return []


relevant_threads_schema = {
    "title": "Relevant Evidence Threads Schema",
    "type": "object",
    "properties": {
        "review": {"type": "string"},
        "threads": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "thread_id": {"type": "string"},
                    "evidence_synthesis": {"type": "string"},
                },
            },
        },
    },
}


# def synthesize_threads_jsonformer(name, review, threads):
#     anthropic = Client(api_key=ANTHROPIC_API_KEY)
#     gen_json = JsonformerClaude(
#         anthropic_client=anthropic,
#         json_schema=relevant_threads_schema,
#         prompt=synthesize_template.format(
#             name=name, review=review, threads=format_threads(threads), schema=""
#         ),
#         max_tokens_to_sample=3000,
#         model="claude-2",
#         debug=True,
#     )

#     async def complete():
#         return await gen_json()

#     return complete()


# print(
#     synthesize_threads(
#         "Elliot", "Elliot isn't good at keeping company secrets", threads
#     )
# )
