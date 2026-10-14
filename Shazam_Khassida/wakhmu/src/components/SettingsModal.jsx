import { X } from 'lucide-react';
import useStore from '../store/useStore';

const TABS = ['Affichage', 'Texte', 'Audio'];
const THEMES = [
  { id: 'modern', label: 'Modern',  bg: '#3D1400', color: '#fff' },
  { id: 'paper',  label: 'Paper',   bg: '#FAF6F0', color: '#1A1208' },
  { id: 'sombre', label: 'Sombre',  bg: '#000000', color: '#fff' },
];

export default function SettingsModal() {
  const { closeSettings, theme, setTheme, showTranslation, toggleTranslation, fontSize, setFontSize } = useStore();
  const [activeTab, setActiveTab] = useState('Affichage');

  return (
    <div className="modal-overlay" onClick={(e) => e.target === e.currentTarget && closeSettings()}>
      <div className="modal-sheet">
        <div className="modal-handle" />
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
          <h2 className="modal-title" style={{ margin: 0 }}>Paramètres</h2>
          <button className="icon-btn" style={{ color: '#6B5B42', background: '#E8DDD0' }} onClick={closeSettings}>
            <X size={18} />
          </button>
        </div>

        <div className="modal-tabs">
          {TABS.map(tab => (
            <button key={tab} className={`modal-tab${activeTab === tab ? ' active' : ''}`}
              onClick={() => setActiveTab(tab)}>
              {tab}
            </button>
          ))}
        </div>

        {activeTab === 'Affichage' && (
          <div>
            <p className="settings-label">Thème</p>
            <div className="theme-options">
              {THEMES.map(t => (
                <button key={t.id}
                  className={`theme-option${theme === t.id ? ' active' : ''}`}
                  style={{ background: t.bg, color: t.color }}
                  onClick={() => setTheme(t.id)}>
                  <span className="theme-option-preview">بِسْمِ</span>
                  {t.label}
                </button>
              ))}
            </div>

            <p className="settings-label" style={{ marginTop: '16px' }}>Taille du texte arabe</p>
            <input
              type="range" min={18} max={36} step={2}
              value={fontSize}
              onChange={e => setFontSize(Number(e.target.value))}
              className="font-size-slider"
              aria-label="Taille du texte"
            />
            <div style={{ textAlign: 'center', fontFamily: "'Amiri', serif", fontSize: `${fontSize}px`, color: '#1A1208', padding: '8px 0' }}>
              بِسْمِ اللَّهِ
            </div>
          </div>
        )}

        {activeTab === 'Texte' && (
          <div>
            <p className="settings-label">Police arabe</p>
            <div style={{ background: '#F5EFE6', borderRadius: '10px', padding: '14px', textAlign: 'center', marginBottom: '16px' }}>
              <span style={{ fontFamily: "'Amiri', serif", fontSize: '22px', color: '#1A1208' }}>
                بِسْمِ اللَّهِ الرَّحْمَنِ
              </span>
              <p style={{ fontSize: '11px', color: '#9B8B7A', marginTop: '6px' }}>Amiri — Police complète avec diacritiques</p>
            </div>

            <div className="toggle-row">
              <span className="toggle-row__label">Afficher la translittération</span>
              <button className="toggle on" aria-label="toggle translitération" />
            </div>
            <div className="toggle-row">
              <span className="toggle-row__label">Afficher la traduction française</span>
              <button
                className={`toggle${showTranslation ? ' on' : ''}`}
                onClick={toggleTranslation}
                aria-label="Toggle traduction"
              />
            </div>
          </div>
        )}

        {activeTab === 'Audio' && (
          <div>
            <p className="settings-label">Audio de référence</p>
            <div style={{ background: '#F5EFE6', borderRadius: '10px', padding: '16px', color: '#6B5B42', fontSize: '14px', lineHeight: '1.6' }}>
              <p>Les fichiers audio de référence pour chaque Khassida seront ajoutés prochainement.</p>
              <p style={{ marginTop: '8px', fontSize: '12px' }}>
                Le lecteur audio est déjà fonctionnel et prêt à recevoir les fichiers.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// Nécessaire car useState est utilisé dans ce composant
import { useState } from 'react';
