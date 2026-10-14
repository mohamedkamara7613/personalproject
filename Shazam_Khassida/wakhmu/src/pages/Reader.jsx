import { ArrowLeft, Bookmark, Settings, Search } from 'lucide-react';
import useStore from '../store/useStore';
import AudioPlayer from '../components/AudioPlayer';

export default function Reader() {
  const { currentKhassida, closeReader, openSettings, showTranslation, fontSize, theme } = useStore();

  if (!currentKhassida) return null;

  const paperStyle = {
    background: theme === 'sombre' ? '#0A0A0A' : theme === 'paper' ? '#FAF6F0' : '#3D1400',
    color: theme === 'sombre' ? '#E0D8D0' : theme === 'paper' ? '#1A1208' : '#F0E8D8',
    minHeight: '100%',
  };

  const arabicColor = theme === 'sombre' ? '#F0E8D8' : theme === 'paper' ? '#1A1208' : '#F0E8D8';
  const mutedColor  = theme === 'sombre' ? '#9B9080' : theme === 'paper' ? '#6B5B42' : '#C8B89A';

  return (
    <div className="reader-page" style={paperStyle}>
      {/* Header */}
      <header className="reader-header">
        <button className="reader-header__back" onClick={closeReader} aria-label="Retour" id="reader-back-btn">
          <ArrowLeft size={20} color="white" />
        </button>
        <span className="reader-header__title">{currentKhassida.titre}</span>
        <div style={{ display: 'flex', gap: 6 }}>
          <button className="icon-btn" aria-label="Favori" id="reader-bookmark-btn">
            <Bookmark size={18} />
          </button>
          <button className="icon-btn" onClick={openSettings} aria-label="Paramètres" id="reader-settings-btn">
            <Settings size={18} />
          </button>
        </div>
      </header>

      {/* Titre en arabe */}
      <div style={{ padding: '24px 20px 16px', textAlign: 'center', borderBottom: `1px solid ${theme === 'paper' ? '#D4C4A8' : 'rgba(255,255,255,0.1)'}` }}>
        <div style={{ fontFamily: "'Amiri', serif", fontSize: '28px', color: arabicColor, lineHeight: 1.6, direction: 'rtl' }}>
          {currentKhassida.titre_arabe}
        </div>
        <div style={{ fontSize: '13px', fontStyle: 'italic', color: mutedColor, marginTop: 4 }}>
          {currentKhassida.translit_intro}
        </div>
        <div style={{ fontSize: '12px', color: mutedColor, marginTop: 4 }}>
          {currentKhassida.auteur}
        </div>
      </div>

      {/* Versets */}
      <div className="reader-content" style={{ paddingBottom: 140 }}>
        {currentKhassida.versets && currentKhassida.versets.length > 0
          ? currentKhassida.versets.map(v => (
            <div key={v.num} className="verse">
              <div className="verse__number" style={{ color: '#C8832A' }}>— {v.num} —</div>
              <div
                className="verse__arabic"
                style={{ fontSize: `${fontSize}px`, color: arabicColor, whiteSpace: 'pre-line' }}
              >
                {v.arabe}
              </div>
              <div className="verse__translit" style={{ color: mutedColor, whiteSpace: 'pre-line' }}>
                {v.translit}
              </div>
              {showTranslation && v.traduction && (
                <div className="verse__translation" style={{ color: mutedColor }}>
                  {v.traduction}
                </div>
              )}
            </div>
          ))
          : (
            <div className="empty-state" style={{ color: mutedColor }}>
              <div className="empty-state__icon">📖</div>
              <div className="empty-state__title">Texte bientôt disponible</div>
              <div className="empty-state__sub">Le contenu de ce Khassida sera ajouté prochainement.</div>
            </div>
          )
        }
      </div>

      {/* Audio Player */}
      <AudioPlayer khassida={currentKhassida} />
    </div>
  );
}
