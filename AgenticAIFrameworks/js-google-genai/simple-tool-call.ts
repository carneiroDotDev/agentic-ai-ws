import {
  FunctionDeclaration,
  GoogleGenerativeAI,
  SchemaType,
} from "@google/generative-ai";

// Step 0 - Initialize the Google Generative AI client
if (!process.env.GOOGLE_GENERATIVE_AI_API_KEY) {
  console.error(
    "❌ Error: GOOGLE_GENERATIVE_AI_API_KEY not found in .env file",
  );
  process.exit(1);
}

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_GENERATIVE_AI_API_KEY);

// Step 1 - Define a simple greeting tool
const tools: FunctionDeclaration[] = [
  {
    name: "respondWhereAmI",
    description: 'Responds to a question "Where am I?" with "DevFest Armenia"',
    parameters: {
      type: SchemaType.OBJECT,
      properties: {},
    },
  },
];

// Step 2 - Execute the tool function
function executeTool(toolName: string): any {
  if (toolName === "respondWhereAmI") {
    return {
      success: true,
      message: "DevFest Armenia",
    };
  }
  return { error: "Unknown tool" };
}

// Step 3 - Send the query and the tools to the model
async function simpleToolCall() {
  const model = genAI.getGenerativeModel({
    model: "gemini-2.0-flash-exp",
    tools: [{ functionDeclarations: tools }],
  });

  const chat = model.startChat({ history: [] });

  const userMessage = "Where am I?";
  const systemPrompt =
    'You are a friendly assistant. When someone says "Hey!", you must use the respondWhereAmI tool to respond.';

  console.log("📤 REQUEST OBJECT:");
  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
  console.log({
    model: "gemini-2.0-flash-exp",
    userMessage,
    systemPrompt,
    tools: tools.map((tool) => ({
      name: tool.name,
      description: tool.description,
    })),
    timestamp: new Date().toISOString(),
  });
  console.log("\n");

  // Step 4 - Send message
  let result = await chat.sendMessage([systemPrompt, userMessage].join("\n\n"));

  // Step 5 - Check for function calls
  const functionCalls = result.response.functionCalls();

  if (functionCalls && functionCalls.length > 0) {
    console.log("📥 RESPONSE OBJECT (Tool Call):");
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    console.log({
      functionCalls: functionCalls.map((call) => ({
        name: call.name,
        args: call.args,
      })),
      candidates: result.response.candidates?.map((candidate) => ({
        finishReason: candidate.finishReason,
      })),
    });
    console.log("\n");

    // Step 6 - Execute the tool
    const functionResponses = functionCalls.map((call) => {
      const toolResult = executeTool(call.name);

      console.log("🔧 TOOL EXECUTION:");
      console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
      console.log({
        toolName: call.name,
        result: toolResult,
      });
      console.log("\n");

      return {
        functionResponse: {
          name: call.name,
          response: toolResult,
        },
      };
    });

    // Step 7 - Send tool results back!!!!!
    result = await chat.sendMessage(functionResponses);

    console.log("📥 FINAL RESPONSE OBJECT:");
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    console.log({
      text: result.response.text(),
      usageMetadata: result.response.usageMetadata,
    });
  } else {
    console.log("No tool calls were made.");
  }
}

// Step 8 - Run the tool call example
simpleToolCall().catch((error) => {
  console.error("❌ Error:", error);
  process.exit(1);
});
