# Agentic AI: Raw Gemini API X AI SDK Implementation

A raw implementation of an agentic AI using Google's native Generative AI SDK. This project demonstrates how to build an agent loop from scratch without high-level abstractions.

## 🎯 Overview

- **Manual Agent Loop**: Full control over the agent execution flow
- **Google Gemini 2.0 Flash**: Latest Gemini model with function calling
- **Tool Execution**: Custom tool execution logic
- **Multi-step Reasoning**: Handle multiple sequential tool calls

## 📁 Files

- `main.ts` - Todo agent with full agent loop implementation
- `request-response.ts` - Simple query showing request/response objects
- `simple-tool-call.ts` - Basic tool calling example
- `file-system-tools.ts` - File system utilities

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ installed
- A Google AI API key from [aistudio.google.com](https://aistudio.google.com/app/apikey)

### Installation

1. Install dependencies:

```bash
npm install
```

2. Create a `.env` file (check the .env.example):

```bash
GOOGLE_GENERATIVE_AI_API_KEY="your-api-key-here"
```

### Running Examples

Run the todo agent:

```bash
npm start
```

Run the simple request/response example:

```bash
npm run example:request-response
```

Run the simple tool call example:

```bash
npm run example:tool-call
```

## 📊 Comparison: Raw Google AI SDK vs Vercel AI SDK

| Feature | Raw Google AI SDK | Vercel AI SDK |
|---------|------------------|---------------|
| Agent Loop | Manual implementation | Built-in with `generateText` |
| Tool Definition | JSON schema | Zod schemas with `tool()` |
| Tool Execution | Manual switch statement | Automatic via `execute` |
| Multi-step Handling | Custom while loop | Automatic with `maxSteps` |
| Type Safety | Manual typing | Full TypeScript inference |
| Code Complexity | ~200 lines | ~100 lines |

## 📄 License

MIT

