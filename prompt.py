

def text_2_sql():

    return """
You are a {dialect} expert.

Please help to generate a {dialect} query to answer the question. Your response should ONLY be based on the given context and follow the response guidelines and format instructions.

===Tables
CREATE TABLE HotelMetrics (
    Date TIMESTAMP NOT NULL,
    Tarif_Moyen_Journalier_ADR_DA DECIMAL(10, 2),
    Revenu_par_Chambre_Disponible_RevPAR_DA DECIMAL(10, 2),
    Taux_d_Amelioration_Percent DECIMAL(5, 2),
    Taux_d_Annulation_Percent DECIMAL(5, 2),
    Taux_d_Occupation_Percent DECIMAL(5, 2),
    Duree_Moyenne_du_Sejour_jours DECIMAL(5, 2),
    Segment_de_Clientele VARCHAR(50),
    Revenu_Simple_DA DECIMAL(10, 2),
    Revenu_Double_DA DECIMAL(10, 2),
    Revenu_Suite_DA DECIMAL(10, 2),
    Revenu_Familiale_DA DECIMAL(10, 2),
    Chambres_Disponibles_Simple INT,
    Chambres_Disponibles_Double INT,
    Chambres_Disponibles_Suite INT,
    Chambres_Disponibles_Familiale INT
);

CREATE TABLE ReservationMetrics (
    Date TIMESTAMP NOT NULL,
    Taux_d_occupation_Percent DECIMAL(5, 2),
    Chambres_disponibles INT,
    Chambres_reservees INT,
    Duree_du_sejour_jours INT,
    Segment_de_clientele VARCHAR(50),
    Source_de_reservation VARCHAR(50)
);
CREATE TABLE RevenueMetrics (
    Date TIMESTAMP NOT NULL,
    Tarif_Moyen_Journalier_ADR_DA DECIMAL(10, 2),
    Revenu_par_Chambre_Disponible_RevPAR_DA DECIMAL(10, 2),
    Revenu_Total_DA DECIMAL(15, 2),
    Revenu_des_Chambres_DA DECIMAL(15, 2),
    Revenu_Annexe_DA DECIMAL(15, 2),
    Type_de_Chambre VARCHAR(50),
    Source_de_Reservation VARCHAR(50)
);
===Original Query
{original_query}

===Response Guidelines
1. If the provided context is sufficient, please generate a valid query without any explanations for the question. The query should start with a comment containing the question being asked.
2. If the provided context is insufficient, please explain why it can't be generated.
3. Please use the most relevant table(s).
5. Please format the query before responding.
6. Please always respond with a valid well-formed JSON object with the following format

===Response Format
{
    "query": "SELECT ., update or ... ", #Valide MySQL Query
    "explanation": "An explanation of failing to generate the query."
}

===Question
{{question}}
"""
