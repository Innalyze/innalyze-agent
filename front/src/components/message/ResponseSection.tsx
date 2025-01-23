import React from 'react';
import { MessageCircle } from 'lucide-react';

interface ResponseSectionProps {
  response: string;
}

export const ResponseSection: React.FC<ResponseSectionProps> = ({ response }) => (
  <div className="flex items-start gap-2">
    <MessageCircle className="w-5 h-5 mt-1 flex-shrink-0" />
    <p className="text-sm">{response}</p>
  </div>
);