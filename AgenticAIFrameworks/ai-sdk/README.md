# Todo Agent - AI-Powered Todo List Manager

A simple agentic AI application built with the Vercel AI SDK that demonstrates the agent loop pattern. This CLI-based todo manager uses AI models (Google Gemini, Anthropic Claude, or OpenAI GPT) to help you manage your todo lists through natural language.

## 🌟 Features

- **Natural Language Interface**: Talk to your todo list in plain English
- **Multiple AI Providers**: Supports Google Gemini, Anthropic Claude, and OpenAI GPT
- **Smart File Handling**: Automatically adds `.md` extension - just say "shopping-list"
- **Auto Task Formatting**: "add do homework" → "- [ ] Do homework" 
- **Task Operations**: Complete, delete, or update tasks with simple commands
- **Verbose Tool Logging**: See detailed information about every tool call including call number, tool name, and full response
- **Real-time Action Indicators**: Visual feedback with emoji indicators (📝 📖 🗑️ ✅ ❌)
- **File-based Storage**: All todos stored in markdown files in a sandboxed `todos` folder
- **Agent Loop**: Demonstrates how AI agents can use tools to accomplish tasks
- **Multiple Tool Calls**: Agent can chain multiple operations to complete complex requests
- **Safety First**: All file operations are sandboxed to the `todos` folder only

## 🏗️ Architecture

This project demonstrates key agentic AI concepts:

1. **Tool Definition**: Functions that the AI can call to interact with the file system
2. **Agent Loop**: The AI can make multiple tool calls in sequence to complete a task
3. **Step Limiting**: Maximum 10 steps to prevent infinite loops
4. **Sandboxing**: All file operations restricted to a specific directory

### Tools Available to the Agent

- `writeFile` - Create or update todo files
- `readFile` - Read existing todo files
- `deleteFile` - Delete todo files
- `listTodos` - List all todo files in the directory

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ installed
- At least one API key from:
  - **Google Gemini** - Get one at [aistudio.google.com](https://aistudio.google.com/app/apikey)
  - **Anthropic Claude** - Get one at [console.anthropic.com](https://console.anthropic.com/)
  - **OpenAI GPT** - Get one at [platform.openai.com](https://platform.openai.com/api-keys)

### Installation

1. Clone or navigate to this directory:

```bash
cd AgenticAIFrameworks/ai-sdk
```

2. Install dependencies:

```bash
npm install
```

3. Create a `.env` file in the project root with at least one API key:

```bash
# Choose one or more providers:

# For Google Gemini:
GOOGLE_GENERATIVE_AI_API_KEY="your-gemini-key-here"

# For Anthropic Claude:
ANTHROPIC_API_KEY="your-anthropic-key-here"

# For OpenAI GPT:
OPENAI_API_KEY="your-openai-key-here"
```

The agent will automatically use the first available API key in this priority order: Gemini → Claude → GPT.

### Running the Agent

Start the agent:

```bash
npm start
```

Or use watch mode for development:

```bash
npm run dev
```

## 💬 Example Usage

Once the agent is running, you can interact with it naturally. The agent is smart and understands context:

```
💬 You: Create a file called GDG-Cloud-Munich. Add a todo called Event on the 19th November.

🤔 Agent is thinking...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 Tool Call #1
📌 Tool Name: writeFile
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Writing to file: GDG-Cloud-Munich.md
✅ Successfully wrote to GDG-Cloud-Munich.md
📊 Tool Response:
{
  "success": true,
  "message": "File written successfully: GDG-Cloud-Munich.md",
  "path": "GDG-Cloud-Munich.md"
}

🤖 Agent: I've created a file called GDG-Cloud-Munich.md and added the task "Event on the 19th November" to it.

💬 You: Add task prepare presentation

🤔 Agent is thinking...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 Tool Call #1
📌 Tool Name: readFile
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 Reading file: GDG-Cloud-Munich.md
✅ Successfully read GDG-Cloud-Munich.md
📊 Tool Response:
{
  "success": true,
  "content": "# GDG-Cloud-Munich\n\n- [ ] Event on the 19th November",
  "message": "File read successfully: GDG-Cloud-Munich.md",
  "path": "GDG-Cloud-Munich.md"
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 Tool Call #2
📌 Tool Name: writeFile
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Writing to file: GDG-Cloud-Munich.md
✅ Successfully wrote to GDG-Cloud-Munich.md
📊 Tool Response:
{
  "success": true,
  "message": "File written successfully: GDG-Cloud-Munich.md",
  "path": "GDG-Cloud-Munich.md"
}

🤖 Agent: I've added "Prepare presentation" to your GDG-Cloud-Munich list!

💬 You: exit
👋 Goodbye!
```

### Smart Features

The agent understands natural language and context:

- **Auto .md extension**: Just say "work-tasks" instead of "work-tasks.md"
- **Task formatting**: "add do homework" → automatically formats as "- [ ] Do homework"
- **Complete tasks**: "complete homework" → finds and marks the task as done
- **Delete tasks**: "delete homework" → removes the task from the file
- **Tool logging**: See every action the agent takes in real-time with emojis

## 🔧 How It Works

### 1. Tool Definition

Each file system function is wrapped as an AI tool using the AI SDK's `tool()` function:

```typescript
const tools = {
  writeFile: tool({
    description: 'Write content to a todo file...',
    parameters: z.object({
      filePath: z.string().describe('The path to the file'),
      content: z.string().describe('The content to write'),
    }),
    execute: async ({ filePath, content }) => {
      return fsTools.writeFile(filePath, content);
    },
  }),
  // ... more tools
};
```

### 2. Agent Loop

The agent uses `generateText` with tools enabled and automatically selects the model based on available API keys:

```typescript
function getModel(): LanguageModelV1 {
  if (process.env.GOOGLE_GENERATIVE_AI_API_KEY) {
    return google('gemini-2.0-flash-exp');
  } else if (process.env.ANTHROPIC_API_KEY) {
    return anthropic('claude-3-5-sonnet-20241022');
  } else if (process.env.OPENAI_API_KEY) {
    return openai('gpt-4o');
  }
}

const result = await generateText({
  model: getModel(),
  system: systemPrompt,
  prompt: userInput,
  tools,
  maxSteps: 10, // Limit steps to prevent infinite loops
});
```

### 3. File System Sandboxing

All file operations are validated and restricted to the `todos` folder:

```typescript
function validatePath(filePath: string): string {
  const fullPath = path.resolve(BASE_DIR, filePath);
  if (!fullPath.startsWith(BASE_DIR)) {
    throw new Error('Access denied: Path is outside allowed directory');
  }
  return fullPath;
}
```

## 📁 Project Structure

```
ai-sdk/
├── main.ts                  # CLI interface and agent loop
├── file-system-tools.ts     # Simplified file system operations
├── package.json             # Dependencies and scripts
├── README.md               # This file
├── .env                    # API keys (create this)
└── todos/                  # Where todo files are stored (created automatically)
```

## 🎓 Learning Outcomes

This project demonstrates:

- **Tool Calling**: How LLMs can use external functions
- **Agent Loops**: Multiple sequential tool calls to complete complex tasks
- **Agentic AI Patterns**: Planning, execution, and response generation
- **Safety Mechanisms**: Path validation and step limiting
- **Real-world Application**: Practical file system operations

## 🔐 Security

- All file operations are sandboxed to the `todos` folder
- Path traversal attacks are prevented through validation
- Maximum step limit prevents infinite loops
- API key should be kept in `.env` (never commit this file)

## 🛠️ Customization

### Change the AI Model

The agent automatically selects a model based on available API keys (priority: Gemini → Claude → GPT). To use a specific provider, only set that provider's API key in your `.env` file.

To change the specific model version, edit the `getModel()` function in `main.ts`:

```typescript
function getModel(): LanguageModelV1 {
  if (process.env.GOOGLE_GENERATIVE_AI_API_KEY) {
    return google('gemini-1.5-pro'); // Different Gemini model
  } else if (process.env.ANTHROPIC_API_KEY) {
    return anthropic('claude-3-opus-20240229'); // Use Opus instead
  } else if (process.env.OPENAI_API_KEY) {
    return openai('gpt-4-turbo'); // Different OpenAI model
  }
}
```

### Supported Models

- **Google Gemini**: `gemini-2.0-flash-exp`, `gemini-1.5-pro`, `gemini-1.5-flash`
- **Anthropic Claude**: `claude-3-5-sonnet-20241022`, `claude-3-opus-20240229`, `claude-3-haiku-20240307`
- **OpenAI GPT**: `gpt-4o`, `gpt-4-turbo`, `gpt-3.5-turbo`

### Adjust Step Limit

Change `maxSteps` in the `generateText` call:

```typescript
maxSteps: 15, // Allow more tool calls
```

### Modify System Prompt

Edit the `systemPrompt` constant in `main.ts` to change the agent's behavior.

## 📝 Notes

- The agent will create the `todos` folder automatically on first use
- All files are stored in markdown format by default for readability
- You don't need to type `.md` extensions - the agent adds them automatically
- Tasks are automatically formatted with markdown checkboxes: `- [ ]` and `- [x]`
- The agent can handle multiple operations in a single request
- Every tool call is logged verbosely with detailed information:
  - 🔧 Tool call number and name
  - 📊 Full JSON response from each tool
  - 📝 Writing to file indicator
  - 📖 Reading file indicator
  - 🗑️ Deleting file indicator
  - 📋 Listing files indicator
  - ✅ Success confirmation
  - ❌ Error details

## 🤝 Contributing

This is a learning project. Feel free to experiment and extend it!

## 📄 License

MIT

