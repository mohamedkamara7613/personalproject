import { Settings, Search } from 'lucide-react';
import ShazamButton from '../components/ShazamButton';
import { KhassidaCard } from '../components/KhassidaCard';
import useStore from '../store/useStore';
import { KHASSIDAS, POPULAIRES } from '../data/khassidas';

export default function Home() {
  const { result, status, history, openSettings } = useStore();
  const populaires = POPULAIRES.map(id => KHASSIDAS.find(k => k.id === id)).filter(Boolean);
  const recents = history.slice(0, 5);

  return (
    <div className="home-page">
      {/* Header */}
      <header className="app-header">
        <span className="app-header__logo">WakhMu</span>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="icon-btn" onClick={openSettings} aria-label="Paramètres" id="home-settings-btn">
            <Settings size={20} />
          </button>
        </div>
      </header>

      <div className="page-content">
        {/* Barre de recherche */}
        <div style={{ padding: '16px 16px 0' }}>
          <div className="search-bar">
            <Search size={16} color="rgba(255,255,255,0.5)" />
            <input
              type="text"
              placeholder="Rechercher un Khassida…"
              id="home-search-input"
              readOnly
            />
          </div>
        </div>

        {/* Bouton Shazam */}
        <ShazamButton />

        {/* Résultat de la reconnaissance */}
        {result && (
          <div className="results-section">
            <p className="results-section__title">✨ Résultat</p>
            <KhassidaCard khassida={result} />
          </div>
        )}

        {/* Khassidas récemment reconnus */}
        {recents.length > 0 && (
          <div className="recent-section">
            <div className="section-header">
              <span className="section-title">Récents</span>
            </div>
            {recents.map(k => (
              <KhassidaCard key={k.id} khassida={k} showMeta={false} />
            ))}
          </div>
        )}

        {/* Khassidas populaires */}
        <div className="recent-section">
          <div className="section-header">
            <span className="section-title">Populaires</span>
          </div>
          {populaires.map(k => (
            <KhassidaCard key={k.id} khassida={k} />
          ))}
        </div>
      </div>
    </div>
  );
}
