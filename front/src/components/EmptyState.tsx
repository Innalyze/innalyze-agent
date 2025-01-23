import React from 'react';
import { useLanguage } from '../context/LanguageContext';
import { getRandomQuestions } from '../utils/questionUtils';

interface EmptyStateProps {
  onQuestionClick: (question: string) => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({ onQuestionClick }) => {
  const { t } = useLanguage();
  const initialQuestions = React.useMemo(() => getRandomQuestions(3), []);

  return (
    <div className="text-center p-8">
      <h2 className="text-xl font-semibold text-gray-700 mb-4">{t('welcome')}</h2>
      <p className="text-gray-600 mb-6">{t('getStarted')}</p>
      
      <div className="space-y-3">
        {initialQuestions.map((question, idx) => (
          <button
            key={idx}
            onClick={() => onQuestionClick(question.question_principale)}
            className="w-full text-left px-4 py-3 rounded-lg bg-white 
                     border border-gray-200 hover:border-blue-300 
                     text-gray-700 hover:text-blue-600 hover:bg-blue-50 
                     transition-colors duration-200"
          >
            {question.question_principale}
          </button>
        ))}
      </div>
    </div>
  );
};