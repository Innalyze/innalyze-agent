import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import JSON5 from "json5";
import { useCallback, useState } from "react";
import { ChatContainer } from "./components/ChatContainer";
import { ChatInput } from "./components/ChatInput";
import { Header } from "./components/Header";
import { useWebSocket } from "./hooks/useWebSocket";
import { Message } from "./types/chat";
import { generateMessageId } from "./utils/idUtils";
import {
  createBotMessage,
  createThinkingMessage,
  createUserMessage,
} from "./utils/messageUtils";
import { Answer } from "./types/answer";

const queryClient = new QueryClient();

function ChatApp() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleWebSocketMessage = useCallback((data: string) => {
    try {
      // Parse the response with the correct type
      const response = JSON5.parse<Answer>(data);

      setMessages((prev) => {
        // Find the last "thinking" message
        const lastThinkingMessage = prev.find((msg) => msg.type === "thinking");

        if (lastThinkingMessage) {
          // Replace the "thinking" message with the first "bot" message
          return prev.map((msg) =>
            msg.id === lastThinkingMessage.id
              ? createBotMessage(
                  generateMessageId("bot"),
                  response.answer // Use the `answer` field from the response
                )
              : msg
          );
        }

        // If no "thinking" message is found, check if the last message is a "bot" message
        const lastMessage = prev[prev.length - 1];
        if (lastMessage && lastMessage.type === "bot") {
          // Update the existing "bot" message for streaming
          return prev.map((msg) =>
            msg.id === lastMessage.id
              ? { ...msg, content: msg.content + response.answer } // Append the `answer` to the existing content
              : msg
          );
        }

        // If no "thinking" or "bot" message is found, create a new "bot" message
        return [
          ...prev,
          createBotMessage(generateMessageId("bot"), response.answer),
        ];
      });
    } catch (error) {
      console.error("Failed to parse WebSocket message:", error);
    }
  }, []);

  const { sendMessage } = useWebSocket("/api/ask", {
    onMessage: handleWebSocketMessage,
    onError: (error) => console.error("WebSocket error:", error),
    onClose: () => setIsProcessing(false),
  });

  const handleSendMessage = async (question: string) => {
    if (isProcessing) return;

    setIsProcessing(true);
    setMessages((prev) => [
      ...prev,
      createUserMessage(question, generateMessageId("user")),
    ]);

    const thinkingId = generateMessageId("thinking");
    setMessages((prev) => [...prev, createThinkingMessage(thinkingId)]);

    try {
      // Send question through WebSocket
      sendMessage(JSON.stringify({ question }));
    } catch (error) {
      console.error("Failed to send message:", error);
      setMessages((prev) => {
        const filtered = prev.filter((msg) => msg.id !== thinkingId);
        return [
          ...filtered,
          createBotMessage(
            generateMessageId("bot"),
            "Sorry, there was an error processing your message."
          ),
        ];
      });
      setIsProcessing(false);
    }
  };

  const handleRestart = () => {
    setMessages([]);
    setIsProcessing(false);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-4xl mx-auto h-screen flex flex-col">
        <Header onRestart={handleRestart} />
        <ChatContainer
          messages={messages}
          onQuestionClick={handleSendMessage}
        />
        <ChatInput onSend={handleSendMessage} disabled={isProcessing} />
      </div>
    </div>
  );
}

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ChatApp />
    </QueryClientProvider>
  );
}
