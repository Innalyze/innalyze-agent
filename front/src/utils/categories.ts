export const CATEGORIES = {
  RESERVATIONS: "reservations",
  CHAMBRES: "chambres",
  REVENUE: "revenue",
  OCCUPATION: "occupation",
} as const;

export const categoryKeywords = {
  [CATEGORIES.RESERVATIONS]: ["réservation", "source", "canal"],
  [CATEGORIES.CHAMBRES]: ["chambre", "type", "suite"],
  [CATEGORIES.REVENUE]: ["revenu", "adr", "tarif"],
  [CATEGORIES.OCCUPATION]: ["occupation", "remplissage", "disponible"],
};
