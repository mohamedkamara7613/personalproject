import { KHASSIDAS } from '../data/khassidas';

// Simule un appel au modèle de reconnaissance IA
// Sera remplacé par le vrai modèle sans toucher à l'interface
export async function mockRecognize(durationMs = 3000) {
  await new Promise(r => setTimeout(r, durationMs));

  // 10% de chance d'échec pour tester le cas d'erreur
  if (Math.random() < 0.10) {
    throw new Error('Khassida non reconnu. Essayez à nouveau.');
  }

  // Retourne un Khassida aléatoire
  const idx = Math.floor(Math.random() * KHASSIDAS.length);
  return KHASSIDAS[idx];
}
