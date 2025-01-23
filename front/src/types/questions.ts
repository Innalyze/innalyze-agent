export interface FollowUpQuestion {
  question: string;
  reponse: string | null;
}

export interface QuestionSet {
  jeu_de_questions: number;
  question_principale: string;
  reponse: string;
  questions_de_suivi: FollowUpQuestion[];
}
