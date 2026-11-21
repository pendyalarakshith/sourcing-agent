import json
from agent.llm import client, MODEL
from agent.tools_registry import TOOLS, TOOL_FUNCTIONS

SYSTEM_PROMPT = """You help recruiters find US healthcare providers.
Use the search_npi tool to find providers. Use official NPPES taxonomy names
(e.g. 'Cardiovascular Disease' for cardiologists) and two-letter state codes.
If a search returns nothing, try a related taxonomy or nearby city once.
Summarize results as a short list with NPI, name, credential and city.
State any assumptions you made."""


def run_tool(name, args):
    fn = TOOL_FUNCTIONS.get(name)
    if not fn:
        return {"error": f"Unknown tool: {name}"}
    try:
        return fn(**args)
    except Exception as e:
        return {"error": str(e)}


def run_agent(query, max_steps=6):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query},
    ]
    for _ in range(max_steps):
        resp = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS, temperature=0.3
        )
        msg = resp.choices[0].message

        if msg.tool_calls:
            messages.append(msg.model_dump(exclude_none=True))
            for call in msg.tool_calls:
                args = json.loads(call.function.arguments or "{}")
                print(f"  -> {call.function.name}({args})")
                result = run_tool(call.function.name, args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result),
                })
            continue

        if msg.content and "<tool_call>" in msg.content:
            messages.append({"role": "user",
                             "content": "You wrote the tool call as text. Call the tool properly instead."})
            continue

        return msg.content
    return "Stopped after too many steps."


if __name__ == "__main__":
    print(run_agent("Find heart doctors in Austin, Texas"))