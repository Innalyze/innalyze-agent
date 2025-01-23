export type MessageType = "user" | "bot" | "thinking";

export interface Message {
  id: string;
  type: MessageType;
  content: string;
  timestamp: number;
}
