import { useState } from 'react';
import { Search, LayoutGrid, List } from 'lucide-react';
import { KhassidaCard, KhassidaGridCard } from '../components/KhassidaCard';
import { KHASSIDAS } from '../data/khassidas';

const SOUS_ONGLETS = ['Khassida', 'Khassida PDF'];

export default function Kaggu() {
  const [sousOnglet, setSousOnglet] = useState('Khassida');
  const [viewMode, setViewMode] = useState('list'); // 'list' | 'grid'
  const [query, setQuery] = useState('');

  const filtered = KHASSIDAS.filter(k =>
    k.titre.toLowerCase().includes(query.toLowerCase()) ||
    k.titre_arabe.includes(query)
  );

  return (
    <div className="kaggu-page">
      {/* Header */}
      <header className="app-header">
        <span className="app-header__title">Kàggu</span>
        <div style={{ display: 'flex', gap: 6 }}>
          <button
            className={`view-btn${viewMode === 'list' ? ' active' : ''}`}
            onClick={() => setViewMode('list')}
            aria-label="Vue liste"
            id="kaggu-view-list"
          >
            <List size={17} />
          </button>
          <button
            className={`view-btn${viewMode === 'grid' ? ' active' : ''}`}
            onClick={() => setViewMode('grid')}
            aria-label="Vue grille"
            id="kaggu-view-grid"
          >
            <LayoutGrid size={17} />
          </button>
        </div>
      </header>

      <div className="page-content">
        {/* Sous-onglets */}
        <div className="tab-bar">
          {SOUS_ONGLETS.map(o => (
            <button
              key={o}
              className={`tab-pill${sousOnglet === o ? ' active' : ''}`}
              onClick={() => setSousOnglet(o)}
              id={`kaggu-tab-${o.replace(' ', '-').toLowerCase()}`}
            >
              {o}
            </button>
          ))}
        </div>

        {/* Barre de recherche */}
        <div style={{ padding: '0 16px 12px' }}>
          <div className="search-bar">
            <Search size={16} color="rgba(255,255,255,0.5)" />
            <input
              type="text"
              placeholder={`Rechercher un ${sousOnglet}…`}
              value={query}
              onChange={e => setQuery(e.target.value)}
              id="kaggu-search-input"
            />
          </div>
        </div>

        {/* Contenu */}
        {sousOnglet === 'Khassida' && (
          viewMode === 'list'
            ? (
              <div className="kaggu-list">
                {filtered.length === 0
                  ? <EmptyState query={query} />
                  : filtered.map(k => <KhassidaCard key={k.id} khassida={k} />)
                }
              </div>
            )
            : (
              <div className="khassida-grid" style={{ paddingBottom: 16 }}>
                {filtered.map(k => <KhassidaGridCard key={k.id} khassida={k} />)}
              </div>
            )
        )}

        {sousOnglet === 'Khassida PDF' && (
          <div>
            <p style={{ padding: '8px 16px', fontSize: '12px', color: 'rgba(255,255,255,0.5)' }}>
              Appuyez pour télécharger le PDF
            </p>
            <div className="khassida-grid" style={{ paddingBottom: 16 }}>
              {filtered.map(k => (
                <PDFCard key={k.id} khassida={k} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function PDFCard({ khassida }) {
  function handleClick() {
    if (khassida.pdf_url) {
      window.open(khassida.pdf_url, '_blank');
    } else {
      alert(`PDF de "${khassida.titre}" — bientôt disponible`);
    }
  }

  return (
    <div className="khassida-grid-card" onClick={handleClick} role="button" tabIndex={0}>
      <div className="khassida-grid-card__img" style={{ fontSize: '32px' }}>
        📄
      </div>
      <div className="khassida-grid-card__title">{khassida.titre}</div>
    </div>
  );
}

function EmptyState({ query }) {
  return (
    <div className="empty-state">
      <div className="empty-state__icon">🔍</div>
      <div className="empty-state__title">Aucun résultat</div>
      <div className="empty-state__sub">Aucun Khassida trouvé pour « {query} »</div>
    </div>
  );
}
