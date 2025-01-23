import React, { useEffect, useRef } from "react";
import { Message } from "../types/chat";
import { ChatMessage } from "./ChatMessage";
import { EmptyState } from "./EmptyState";
import { ThinkingIndicator } from "./ThinkingIndicator";
import { scrollToElement } from "../utils/scrollUtils";

interface ChatContainerProps {
  messages: Message[];
  onQuestionClick: (question: string) => void;
}

export const ChatContainer: React.FC<ChatContainerProps> = ({
  messages,
  onQuestionClick,
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollToElement(messagesEndRef.current);
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-4">
      {messages.length === 0 ? (
        <EmptyState onQuestionClick={onQuestionClick} />
      ) : (
        <>
          {messages.map((message) =>
            message.type === "thinking" ? (
              <ThinkingIndicator key={message.id} />
            ) : (
              <ChatMessage
                key={message.id}
                isUser={message.type === "user"}
                message={message.content}
                onQuestionClick={
                  message.type !== "user" ? onQuestionClick : undefined
                }
              />
            )
          )}
          <div ref={messagesEndRef} />
        </>
      )}
    </div>
  );
};
