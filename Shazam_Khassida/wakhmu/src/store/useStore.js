import { create } from 'zustand';

const useStore = create((set, get) => ({
  // ---- Navigation ----
  page: 'home', // 'home' | 'kaggu' | 'reader'
  navigate: (page) => set({ page }),

  // ---- Reader ----
  currentKhassida: null,
  openReader: (khassida) => set({ currentKhassida: khassida, page: 'reader' }),
  closeReader: () => set({ page: get().previousPage || 'home', currentKhassida: null }),

  // ---- Reconnaissance ----
  status: 'idle', // 'idle' | 'listening' | 'processing' | 'found' | 'error'
  result: null,
  errorMsg: '',
  setStatus: (status) => set({ status }),
  setResult: (result) => set({ result, status: 'found' }),
  setError: (msg) => set({ status: 'error', errorMsg: msg }),
  resetRecognition: () => set({ status: 'idle', result: null, errorMsg: '' }),

  // ---- Historique (en mémoire, complété par Dexie) ----
  history: [],
  addToHistory: (khassida) => set((s) => ({
    history: [khassida, ...s.history.filter(k => k.id !== khassida.id)].slice(0, 20),
  })),

  // ---- Paramètres ----
  settingsOpen: false,
  openSettings: () => set({ settingsOpen: true }),
  closeSettings: () => set({ settingsOpen: false }),
  theme: 'paper',  // 'modern' | 'paper' | 'sombre'
  setTheme: (theme) => set({ theme }),
  showTranslation: true,
  toggleTranslation: () => set((s) => ({ showTranslation: !s.showTranslation })),
  fontSize: 26,
  setFontSize: (fontSize) => set({ fontSize }),
  audioEnabled: true,
  toggleAudio: () => set((s) => ({ audioEnabled: !s.audioEnabled })),
}));

export default useStore;
