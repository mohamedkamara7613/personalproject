import { ChevronRight, FileText } from 'lucide-react';
import useStore from '../store/useStore';
import { getKhassidaById } from '../data/khassidas';

export function KhassidaCard({ khassida, showMeta = true }) {
  const openReader = useStore(s => s.openReader);

  function handleClick() {
    const full = getKhassidaById(khassida.id) || khassida;
    openReader(full);
  }

  return (
    <div className="khassida-card" onClick={handleClick} role="button" tabIndex={0}
      onKeyDown={e => e.key === 'Enter' && handleClick()}>
      <div className="khassida-card__img">
        <FileText size={24} />
      </div>
      <div className="khassida-card__body">
        <div className="khassida-card__title">{khassida.titre}</div>
        <div className="khassida-card__arabic">{khassida.titre_arabe}</div>
        {showMeta && khassida.auteur && (
          <div className="khassida-card__meta">{khassida.auteur}</div>
        )}
      </div>
      <ChevronRight size={18} className="khassida-card__arrow" />
    </div>
  );
}

export function KhassidaGridCard({ khassida }) {
  const openReader = useStore(s => s.openReader);

  function handleClick() {
    const full = getKhassidaById(khassida.id) || khassida;
    openReader(full);
  }

  return (
    <div className="khassida-grid-card" onClick={handleClick} role="button" tabIndex={0}
      onKeyDown={e => e.key === 'Enter' && handleClick()}>
      <div className="khassida-grid-card__img">
        <FileText size={28} />
      </div>
      <div className="khassida-grid-card__title">{khassida.titre}</div>
    </div>
  );
}
