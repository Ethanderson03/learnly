# Fork

An AI-powered learning tool that uses branching conversations to help you explore topics deeply. Fork off into subtopics, mark concepts as understood, and let the AI tutor adapt to your expertise level.

## Features

### Branching Conversations
- **Fork discussions** - Highlight any text or click suggested topics to branch into focused subtopics
- **Visual tree** - Sidebar shows your full exploration tree with depth indicators
- **Context inheritance** - Each branch carries forward the parent conversation context

### Intelligent AI Tutor
- **Socratic teaching** - The AI uses questions and progressive disclosure to deepen understanding
- **Expertise levels** - Select your level (novice to expert) and responses adapt accordingly
- **Foundation marking** - Mark messages as "understood" to signal concepts you've grasped

### Interactive Learning Tools
The AI can generate rich interactive content:

- **Mermaid Diagrams** - Visual flowcharts, architecture diagrams, and concept maps with expandable lightbox view
- **Charts (Chart.js)** - Bar, line, pie, and radar charts for data visualization
- **Comparison Tables** - Side-by-side feature comparisons with sortable columns
- **Flashcards** - Interactive flip cards for reviewing key concepts

### Terminal-Inspired UI
- Dark theme with monospace typography
- Depth meter showing how deep you've explored
- Collapsible sidebar for focused reading

## Getting Started

### Prerequisites
- Python 3.x
- An [Anthropic API key](https://console.anthropic.com/)

### Running Locally

1. Clone the repository:
```bash
git clone https://github.com/Ethanderson03/fork.git
cd fork
```

2. Start the server:
```bash
python server.py
```

3. Open http://localhost:4173 in your browser

4. Click the settings icon (gear) in the sidebar and add your Anthropic API key

### How It Works

The Python server (`server.py`) serves static files and proxies requests to the Anthropic API with streaming support. Your API key is stored in localStorage and never sent to any server except Anthropic directly.

## Usage Tips

- **Start broad** - Ask about a topic you want to learn
- **Fork often** - When the AI mentions something interesting, highlight it and fork
- **Mark foundations** - Click the star on messages when you understand a concept
- **Use the tree** - The sidebar shows your exploration path; click branches to revisit

## Tech Stack

- **Frontend**: React 18 (via CDN with Babel transform)
- **Charts**: Chart.js
- **Diagrams**: Mermaid.js
- **Backend**: Python stdlib (http.server)
- **AI**: Claude API (Anthropic)

## License

MIT
