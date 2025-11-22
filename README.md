# Agentic AI Workshop
## From the Agent Loop to Multi-Agents

A comprehensive workshop exploring AI agent development using Google's Agent Development Kit (ADK), covering everything from basic agents to complex multi-agent systems and production deployment.

## Workshop Structure

This repository contains three main sections:

### 🎓 [DevFest25-WS](./DevFest25-WS/) - Main Workshop (Python + ADK)
Complete 9-part progressive workshop covering:
- **P1**: Basic agents with built-in tools
- **P2**: Custom tools and API integration
- **P3**: Multi-agent teams and delegation
- **P4**: Sessions and conversational memory
- **P5**: Router patterns for intelligent delegation
- **P6**: Sequential workflows with SequentialAgent
- **P7**: Iterative refinement with LoopAgent
- **P8**: Parallel execution with ParallelAgent
- **P9**: Production deployment to Cloud Run

Each part includes:
- Complete working code
- Dockerfiles for containerization
- Comprehensive README with examples
- Progressive difficulty

### 🔧 [AgenticAIFrameworks](./AgenticAIFrameworks/) - Alternative Frameworks
Examples using different agentic AI frameworks:
- **js-google-genai**: TypeScript examples with Google's Generative AI SDK
- **ai-sdk**: Examples using Vercel's AI SDK

### 📝 [Prompts](./Prompts/) - Prompt Templates
Collection of system prompts and templates.

## Prerequisites

- **Python 3.13+** (for DevFest25-WS)
- **Node.js 18+** (for AgenticAIFrameworks)
- **Docker** (optional, for containerization)
- **Google API Key** for Gemini ([Get one here](https://codelabs.developers.google.com/onramp/instructions#1))

## Quick Start

### DevFest25-WS (Recommended)

```bash
cd DevFest25-WS

# Set up environment
cp env.example .env
# Edit .env and add your GOOGLE_API_KEY

# Start with Part 1
cd P1-ToolCalling
uv venv && source .venv/bin/activate && uv sync
adk web --port 8000
```

Visit http://localhost:8000 to start chatting with your first agent!

### Alternative Frameworks

```bash
# Google Generative AI SDK (TypeScript)
cd AgenticAIFrameworks/js-google-genai
pnpm install
# Follow setup.md for configuration

# Vercel AI SDK
cd AgenticAIFrameworks/ai-sdk
pnpm install
# Follow setup.md for configuration
```

## Learning Path

**Recommended progression** through DevFest25-WS:

1. **Fundamentals** (P1-P2): Learn agent basics and custom tools
2. **Multi-Agent** (P3-P5): Build agent teams and routing systems
3. **Advanced Patterns** (P6-P8): Master sequential, iterative, and parallel workflows
4. **Production** (P9): Deploy to Google Cloud Run

Each part builds on previous concepts, creating a complete learning journey.

## Key Concepts Covered

### Agent Fundamentals
- Agent definition and configuration
- Built-in tools (google_search)
- Custom tool development
- Environment setup

### Multi-Agent Systems
- Agent-as-a-Tool pattern
- Delegation and specialization
- Router patterns
- Hierarchical agent structures

### Advanced Workflows
- **Sequential**: Chain agents for multi-step tasks
- **Loop**: Iterative refinement with critique-refine cycles
- **Parallel**: Concurrent execution for speed

### Production Readiness
- Docker containerization
- Cloud Run deployment
- Secret management
- Monitoring and logging

## Repository Structure

```
agentic-ai-ws/
├── DevFest25-WS/           # Main workshop (9 parts)
│   ├── P1-ToolCalling/     # Basic agent
│   ├── P2-CustomTools/     # Custom tools
│   ├── P3-AgentTeams/      # Multi-agent
│   ├── P4-Memory/          # Sessions
│   ├── P5-RouterAgent/     # Routing
│   ├── P6-SequentialAgents/# Sequential
│   ├── P7-LoopAgents/      # Iterative
│   ├── P8-ParallelAgents/  # Parallel
│   ├── P9-Deployment/      # Cloud Run
│   └── source/             # Original notebooks
├── AgenticAIFrameworks/    # Alternative frameworks
│   ├── js-google-genai/    # TypeScript/Google
│   └── ai-sdk/             # Vercel AI SDK
└── Prompts/                # Prompt templates
```

## Resources

### Workshop Materials
- Original notebooks in `DevFest25-WS/source/`
- Complete working examples in each part
- Dockerfiles for all parts

## Features

✅ **Progressive Learning** - Build from basics to advanced patterns  
✅ **Production-Ready** - Complete with Docker and deployment guides  
✅ **Hands-On** - Every part is runnable code with examples  
✅ **Well-Documented** - Comprehensive READMEs with ASCII diagrams  
✅ **Multiple Frameworks** - Explore different agentic AI approaches  

## Contributing

This workshop was developed for educational purposes. Feel free to:
- Use the code in your own projects
- Adapt examples for your use cases
- Share feedback and improvements

## Workshop Credits

Inspired by Google's ADK learning notebooks and adapted for hands-on workshop format with production deployment focus.

## License

See [LICENSE](./LICENSE) file for details.

## Getting Help

Each workshop part includes:
- Detailed README with setup instructions
- Example prompts to try
- Troubleshooting tips
- Links to next steps

Start with [DevFest25-WS README](./DevFest25-WS/README.md) for the complete learning path!

---

**Ready to build amazing AI agents?** Start with [Part 1: Tool Calling](./DevFest25-WS/P1-ToolCalling/) 🚀
