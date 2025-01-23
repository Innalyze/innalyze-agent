import { Question, questions } from "../data/questions";

export const getRandomQuestions = (count: number = 3): Question[] => {
  const shuffled = [...questions].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, count);
};
