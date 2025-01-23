import { Message } from "../types/chat";

export const createUserMessage = (content: string, id: string): Message => ({
  id,
  type: "user",
  content,
  timestamp: Date.now(),
});

export const createThinkingMessage = (id: string): Message => ({
  id,
  type: "thinking",
  content: "",
  timestamp: Date.now(),
});

export const createBotMessage = (id: string, content: string): Message => ({
  id,
  type: "bot",
  content,
  timestamp: Date.now(),
});
