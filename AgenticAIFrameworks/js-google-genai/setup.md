# Quick Setup Guide - Raw Google Gen AI Implementation

## 1. Create your .env file

Create a file named `.env` in this directory:

```bash
GOOGLE_GENERATIVE_AI_API_KEY="your-api-key-here"
```

Get your API key from: https://aistudio.google.com/app/apikey

## 2. Install dependencies

```bash
npm install
```

## 3. Run the agent

For production (no auto-reload):
```bash
npm start
```

For development (with auto-reload on code changes, ignoring todos folder):
```bash
npm run dev
```

**Note**: The dev script automatically ignores changes in the `todos/` folder to prevent the app from reloading while you're typing.

## Example Prompts to Try

### Creating and Managing Lists
- "Create a shopping list" (automatically creates shopping-list.md)
- "Create a todo list called work-tasks"
- "List all my todo files"

### Adding Tasks (Smart Formatting)
- "Add buy milk" → becomes "- [ ] Buy milk"
- "Add task do the homework" → becomes "- [ ] Do the homework"
- "Add finish report to work-tasks"

### Completing Tasks
- "Complete task buy milk"
- "Mark homework as done"
- "Complete the report task"

### Deleting Tasks
- "Delete task buy milk"
- "Remove homework from the list"

### Reading and Viewing
- "Show me my shopping list"
- "What's in my work-tasks?"
- "Read my todos"

### Other Operations
- "Delete the shopping list file"

**Note**: This is a raw implementation using Google's Gen AI SDK directly. Compare it with the `ai-sdk` folder to see how frameworks simplify agent development!

## What Makes This "Raw"?

Unlike the AI SDK version, this implementation:
- ✅ Manually implements the agent loop
- ✅ Directly manages function calling
- ✅ Custom tool execution logic
- ✅ Manual conversation history handling
- ✅ Explicit step counting and control flow

This gives you full control and understanding of how agents work under the hood!

