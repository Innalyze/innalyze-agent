import React from 'react';
import { MessageCircle } from 'lucide-react';

interface MessageContentProps {
  message: string;
}

export const MessageContent: React.FC<MessageContentProps> = ({ message }) => (
  <div className="flex items-start gap-2">
    <MessageCircle className="w-5 h-5 mt-1 flex-shrink-0" />
    <p className="text-sm">{message}</p>
  </div>
);