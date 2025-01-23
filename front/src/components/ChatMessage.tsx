import React from "react";
import { ResponseSection } from "./message/ResponseSection";
import { ResultSection } from "./ResultSection";

interface ChatMessageProps {
  isUser: boolean;
  message: string;
  onQuestionClick?: (question: string) => void;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({
  isUser,
  message,
  onQuestionClick,
}) => (
  <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
    <div
      className={`max-w-[80%] ${
        isUser
          ? "bg-blue-600 text-white rounded-l-lg rounded-tr-lg"
          : "bg-white text-gray-800 rounded-r-lg rounded-tl-lg"
      } p-4 shadow-md`}
    >
      <ResponseSection response={message} />
      {!isUser && onQuestionClick && (
        <ResultSection onQuestionClick={onQuestionClick} />
      )}
    </div>
  </div>
);
