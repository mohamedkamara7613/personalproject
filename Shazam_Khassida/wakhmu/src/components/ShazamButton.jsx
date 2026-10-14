import { Mic, MicOff } from 'lucide-react';
import { useState } from 'react';
import useStore from '../store/useStore';
import { mockRecognize } from '../engine/mockAI';
import { addHistorique } from '../db/db';

export default function ShazamButton() {
  const { status, setStatus, setResult, setError, addToHistory } = useStore();
  const [held, setHeld] = useState(false);

  const isListening = status === 'listening' || status === 'processing';

  async function handleTap() {
    if (isListening) return;
    if (status === 'found' || status === 'error') {
      useStore.getState().resetRecognition();
      return;
    }

    try {
      setStatus('listening');
      const khassida = await mockRecognize(3000);
      setResult(khassida);
      addToHistory(khassida);
      await addHistorique(khassida);
    } catch (e) {
      setError(e.message);
    }
  }

  const statusText = {
    idle:       'Appuyez pour identifier',
    listening:  'Écoute en cours…',
    processing: 'Analyse en cours…',
    found:      'Khassida reconnu !',
    error:      'Non reconnu — Réessayer',
  }[status];

  return (
    <div className="shazam-zone">
      <span className="shazam-tagline">WakhMu</span>

      <div className={`shazam-btn-wrapper${isListening ? ' listening' : ''}`}>
        <div className="wave-ring" />
        <div className="wave-ring" />
        <div className="wave-ring" />
        <div className="wave-ring" />
        <button
          className={`shazam-btn${isListening ? ' listening' : ''}`}
          onClick={handleTap}
          aria-label="Identifier le Khassida"
          disabled={isListening}
        >
          {isListening
            ? <MicOff size={38} strokeWidth={2} />
            : <Mic size={38} strokeWidth={2} />
          }
        </button>
      </div>

      <p className={`shazam-status ${status}`}>{statusText}</p>
    </div>
  );
}
