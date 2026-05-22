const GROQ_API_KEY = process.env.GROQ_API_KEY;
import { Agent, Browser, ChatGroq } from "browser-use";
// import { Agent } from "browser-use-sdk";

// import { ChatGroq } from "browser-use/llm/groq";
// import { ChatGroq } from "@langchain/groq";

async function runBrowserAgent() {
  // 1. Initialize the Groq LLM
  const llm = new ChatGroq({
    apiKey: GROQ_API_KEY,
    model: "llama-3.3-70b-versatile", // Use a supported Groq model
  });

  // const browser = Browser();
  // const llm = new ChatOpenAI({
  //   apiKey: GROQ_API_KEY,
  //   model: "gpt-oss-20b", // Use a supported Groq model
  // });
  // 2. Create the Agent with a task
  const agent = new Agent({
    task: 'Go to google.com and search for "latest AI news"',
    llm: llm,
    use_vision: false,
  });

  // 3. Run the agent
  const result = await agent.run();
  console.log("Task Result:", result);
}

runBrowserAgent();

// import { Agent } from "browser-use-sdk";

// const client = new BrowserUse({
//   apiKey: "",
// });

// async function runBrowserAgent() {
//   const result = await client.run(
//     "List the top 20 posts on Hacker News today with their points",
//   );
//   console.log(result.output);
// }

// runBrowserAgent();
