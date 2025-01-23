import React from 'react';
import { MessageCircle } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

interface FollowUpQuestionsProps {
  questions: string[];
  onQuestionClick: (question: string) => void;
}

export const FollowUpQuestions: React.FC<FollowUpQuestionsProps> = ({
  questions,
  onQuestionClick
}) => {
  const { t } = useLanguage();

  if (questions.length === 0) return null;

  return (
    <div className="mt-4 pt-3 border-t border-gray-200">
      <div className="flex items-center gap-2 mb-2">
        <MessageCircle className="w-4 h-4" />
        <p className="text-sm font-medium text-gray-700">{t('followUpQuestions')}</p>
      </div>
      <div className="space-y-2">
        {questions.map((question, index) => (
          <button
            key={index}
            onClick={() => onQuestionClick(question)}
            className="w-full text-left px-3 py-2 text-sm rounded-md 
                     bg-gray-50 hover:bg-blue-50 text-gray-600 hover:text-blue-600
                     transition-colors duration-200"
          >
            {question}
          </button>
        ))}
      </div>
    </div>
  );
};