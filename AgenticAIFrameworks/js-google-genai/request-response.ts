import { GoogleGenerativeAI } from '@google/generative-ai';

// Initialize the Google Generative AI client
if (!process.env.GOOGLE_GENERATIVE_AI_API_KEY) {
  console.error('❌ Error: GOOGLE_GENERATIVE_AI_API_KEY not found in .env file');
  process.exit(1);
}

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_GENERATIVE_AI_API_KEY);

async function simpleQuery() {
  const model = genAI.getGenerativeModel({
    model: 'gemini-2.0-flash-exp',
  });

  const query = 'What is the capital of France?';

  console.log('📤 REQUEST OBJECT:');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  console.log({
    model: 'gemini-2.0-flash-exp',
    prompt: query,
    timestamp: new Date().toISOString(),
  });
  console.log('\n');

  const result = await model.generateContent(query);
  const response = result.response;

  console.log('📥 RESPONSE OBJECT:');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  console.log({
    text: response.text(),
    candidates: response.candidates?.map((candidate) => ({
      content: candidate.content,
      finishReason: candidate.finishReason,
      safetyRatings: candidate.safetyRatings,
    })),
    usageMetadata: response.usageMetadata,
  });
}

// Run the query
simpleQuery().catch((error) => {
  console.error('❌ Error:', error);
  process.exit(1);
});

