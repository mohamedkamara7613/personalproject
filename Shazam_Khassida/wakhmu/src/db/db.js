import Dexie from 'dexie';

const db = new Dexie('WakhMuDB');

db.version(1).stores({
  historique: '++id, khassidaId, titre, timestamp',
  favoris:    '++id, khassidaId, titre, timestamp',
});

export async function addHistorique(khassida) {
  await db.historique.add({
    khassidaId: khassida.id,
    titre: khassida.titre,
    titre_arabe: khassida.titre_arabe,
    timestamp: Date.now(),
  });
}

export async function getHistorique(limit = 20) {
  return db.historique.orderBy('timestamp').reverse().limit(limit).toArray();
}

export async function clearHistorique() {
  return db.historique.clear();
}

export default db;
