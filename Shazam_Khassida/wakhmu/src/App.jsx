import './index.css';
import useStore from './store/useStore';
import BottomNav from './components/BottomNav';
import SettingsModal from './components/SettingsModal';
import Home from './pages/Home';
import Kaggu from './pages/Kaggu';
import Reader from './pages/Reader';

export default function App() {
  const { page, settingsOpen } = useStore();

  return (
    <div className="app-shell">
      {/* Pages */}
      {page === 'reader'
        ? <div className="page-content" style={{ paddingBottom: 0 }}><Reader /></div>
        : (
          <>
            {page === 'home'  && <Home />}
            {page === 'kaggu' && <Kaggu />}
            <BottomNav />
          </>
        )
      }

      {/* Modal Paramètres */}
      {settingsOpen && <SettingsModal />}
    </div>
  );
}
