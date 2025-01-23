import React from "react";
import { getRandomQuestions } from "../utils/questionUtils";

interface ResultSectionProps {
  onQuestionClick: (question: string) => void;
}

export const ResultSection: React.FC<ResultSectionProps> = ({
  onQuestionClick,
}) => {
  const questions = React.useMemo(() => getRandomQuestions(3), []);

  return (
    <div className="mt-6 border-t border-gray-200 pt-4">
      <p className="text-sm text-gray-600 mb-3">Autres questions possibles :</p>
      <div className="space-y-2">
        {questions.map((question, idx) => (
          <button
            key={idx}
            onClick={() => onQuestionClick(question.question_principale)}
            className="w-full text-left px-3 py-2 text-sm rounded-md 
                     bg-gray-50 hover:bg-blue-50 text-gray-600 
                     hover:text-blue-600 transition-colors duration-200"
          >
            {question.question_principale}
          </button>
        ))}
      </div>
    </div>
  );
};
