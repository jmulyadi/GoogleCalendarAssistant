import { Message } from "@/types";

// Define the structure of the response you expect from your backend
type ApiResponse = {
  action: string;
  response: string;
};

export const config = {
  runtime: "edge",
};

const handler = async (req: Request): Promise<Response> => {
  try {
    // Extract the messages array from the request body
    const { messages } = (await req.json()) as { messages: Message[] };
    //console.log(messages);
    // Concatenate the content of all messages into a single string (or choose logic to determine which to send)
    const text = messages.map((message) => message.content).join(" ");
    //console.log(text);
    // Send the text to your FastAPI endpoint
    const apiUrl = "http://localhost:8000/process"; // Change to your FastAPI URL
    const apiResponse = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: text }), // Serialize the object into a JSON string
    });

    // Check if the API responded with an error
    if (!apiResponse.ok) {
      throw new Error(`API Error: ${apiResponse.statusText}`);
    }

    // Parse the API response
    const responseData: ApiResponse = await apiResponse.json();

    // Now, handle the action based on the response (add event, delete event, or summarize)
    // Return the result as a response
    return new Response(responseData.response, { status: 200 });
  } catch (error) {
    console.error(error);
    return new Response("Error processing request", { status: 500 });
  }
};

export default handler;
