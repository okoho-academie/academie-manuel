export type Appareil = 'smartphone' | 'laptop-recommande' | 'laptop-obligatoire';

export interface SeanceRef {
  code: string;
  titre: string;
  appareil?: Appareil;
  livrable?: string;
  outil?: string;
}
export interface Module {
  code: string;
  titre: string;
  seances: SeanceRef[];
}
export interface Partie {
  num: 'I' | 'II' | 'III' | 'IV' | 'V' | string;
  titre: string;
  modules: Module[];
}
