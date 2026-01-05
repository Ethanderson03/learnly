# Learnly Prototype

This prototype demonstrates a lightweight, browser-only React experience for branching LLM-style conversations.

## Features
- Highlight portions of responses and fork side chats that inherit the parent context.
- Movable, minimizable modal chat windows for every forked branch.
- Sidebar tree showing every conversation layer and allowing quick activation.
- Closing a modal merges its notes back into the main chat thread.

## Running locally
Because everything is loaded from CDNs, you only need a simple static server:

```bash
python -m http.server 4173
```

Then open http://localhost:4173 in your browser.
