import { Home, BookOpen } from 'lucide-react';
import useStore from '../store/useStore';

export default function BottomNav() {
  const page = useStore(s => s.page);
  const navigate = useStore(s => s.navigate);

  const tabs = [
    { id: 'home',  label: 'Accueil', Icon: Home },
    { id: 'kaggu', label: 'Kàggu',   Icon: BookOpen },
  ];

  return (
    <nav className="bottom-nav">
      {tabs.map(({ id, label, Icon }) => (
        <button
          key={id}
          className={`nav-tab${page === id || (page === 'reader' && id === 'kaggu') ? ' active' : ''}`}
          onClick={() => navigate(id)}
          aria-label={label}
        >
          <span className="nav-tab__icon">
            <Icon size={22} strokeWidth={page === id ? 2.5 : 1.8} />
          </span>
          <span className="nav-tab__label">{label}</span>
        </button>
      ))}
    </nav>
  );
}
