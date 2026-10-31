// Retourne l'action la plus urgente pour une personne dans une cohorte
export interface ProchainPas {
  label: string;
  href: string;
  urgent: boolean;
}

export function prochainPas(context: {
  seanceOuverte?: string;  // code de la séance en cours
  devoirEcheance?: string; // AAAA-MM-JJ
  devoirRendu: boolean;
  quizNonPasse?: string;   // code quiz
}): ProchainPas {
  const { seanceOuverte, devoirEcheance, devoirRendu, quizNonPasse } = context;
  const maintenant = new Date();

  if (devoirEcheance && !devoirRendu) {
    const echeance = new Date(devoirEcheance + 'T23:59:59+01:00');
    const heuresRestantes = (echeance.getTime() - maintenant.getTime()) / 3600000;
    if (heuresRestantes < 24) {
      return { label: 'Déposer votre rendu (urgent)', href: `/seance/${seanceOuverte}/rendu`, urgent: true };
    }
    return { label: 'Déposer votre rendu', href: `/seance/${seanceOuverte}/rendu`, urgent: false };
  }
  if (quizNonPasse) {
    return { label: 'Passer le quiz', href: `/quiz/${quizNonPasse}`, urgent: false };
  }
  if (seanceOuverte) {
    return { label: 'Continuer la séance', href: `/seance/${seanceOuverte}`, urgent: false };
  }
  return { label: 'Voir mon parcours', href: '/parcours', urgent: false };
}
