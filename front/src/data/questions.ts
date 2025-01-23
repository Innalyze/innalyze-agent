export interface Question {
  question_set: number;
  question_principale: string;
  reponse: string;
}

export const questions: Question[] = [
  {
    question_set: 1,
    question_principale:
      "Quel pourcentage des chambres réservées provenaient de chaque source de réservation en octobre ?",
    reponse:
      "En octobre, le pourcentage des chambres réservées par source était : Site web : 35 %, Application : 40 %, Agent de voyage : 15 %, Direct : 10 %.",
  },
  {
    question_set: 2,
    question_principale: "Quel était le revenu total généré en octobre ?",
    reponse: "Le revenu total généré en octobre était de 1 500 000 DA.",
  },
  {
    question_set: 3,
    question_principale:
      "Quel était le taux d'annulation moyen pour chaque segment de clientèle en octobre ?",
    reponse:
      "Le taux d'annulation moyen en octobre était : Loisirs : 4 %, Couples : 6 %, Affaires : 2 %.",
  },
  {
    question_set: 4,
    question_principale:
      "Quel était le pourcentage de types de chambres réservées en octobre ?",
    reponse:
      "La répartition des types de chambres réservées en octobre était : Chambres simples : 20 %, Chambres doubles : 50 %, Suites : 20 %, Chambres familiales : 10 %.",
  },
  {
    question_set: 5,
    question_principale:
      "Quelle était la durée moyenne des séjours pour chaque segment de clientèle en octobre ?",
    reponse:
      "La durée moyenne des séjours en octobre était : Loisirs : 3 jours, Couples : 2 jours, Affaires : 5 jours.",
  },
  {
    question_set: 6,
    question_principale:
      "Quel segment de clientèle avait le taux d'occupation le plus élevé en octobre ?",
    reponse:
      "Le segment Affaires avait le taux d'occupation le plus élevé, suivi des Loisirs.",
  },
];
