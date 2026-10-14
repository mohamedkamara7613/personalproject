import { useState, useRef, useEffect } from 'react';
import { Play, Pause, SkipBack, SkipForward } from 'lucide-react';

function formatTime(seconds) {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
}

export default function AudioPlayer({ khassida }) {
  const audioRef = useRef(null);
  const [playing, setPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);

  // Si pas d'URL audio, on simule avec un timer
  const hasAudio = Boolean(khassida?.audio_url);

  useEffect(() => {
    setPlaying(false);
    setCurrentTime(0);
    setDuration(0);
  }, [khassida?.id]);

  // Simulation du player quand pas d'audio réel
  useEffect(() => {
    if (!hasAudio) {
      setDuration(240); // 4 min simulées
    }
  }, [hasAudio]);

  useEffect(() => {
    if (!hasAudio) {
      if (!playing) return;
      const interval = setInterval(() => {
        setCurrentTime(t => {
          if (t >= duration) { setPlaying(false); return 0; }
          return t + 1;
        });
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [playing, hasAudio, duration]);

  function togglePlay() {
    if (hasAudio && audioRef.current) {
      if (playing) audioRef.current.pause();
      else audioRef.current.play();
    }
    setPlaying(p => !p);
  }

  function handleSeek(e) {
    const rect = e.currentTarget.getBoundingClientRect();
    const ratio = (e.clientX - rect.left) / rect.width;
    const newTime = ratio * duration;
    setCurrentTime(newTime);
    if (hasAudio && audioRef.current) {
      audioRef.current.currentTime = newTime;
    }
  }

  const progress = duration > 0 ? (currentTime / duration) * 100 : 0;

  return (
    <div className="audio-player">
      {hasAudio && (
        <audio
          ref={audioRef}
          src={khassida.audio_url}
          onTimeUpdate={() => setCurrentTime(audioRef.current?.currentTime || 0)}
          onLoadedMetadata={() => setDuration(audioRef.current?.duration || 0)}
          onEnded={() => setPlaying(false)}
        />
      )}

      <div className="audio-player__title">
        {khassida?.titre || 'Khassida'}
        {!hasAudio && <span style={{ color: 'rgba(255,255,255,0.4)', fontSize: '10px', marginLeft: '8px' }}>
          (audio de référence — bientôt disponible)
        </span>}
      </div>

      <div className="audio-player__controls">
        <button className="icon-btn" onClick={() => setCurrentTime(0)} aria-label="Retour au début">
          <SkipBack size={18} />
        </button>

        <button className="play-btn" onClick={togglePlay} aria-label={playing ? 'Pause' : 'Lecture'}>
          {playing ? <Pause size={20} /> : <Play size={20} style={{ marginLeft: 2 }} />}
        </button>

        <button className="icon-btn" aria-label="Fin">
          <SkipForward size={18} />
        </button>

        <div className="audio-progress">
          <div className="progress-bar" onClick={handleSeek} role="slider" aria-label="Progression">
            <div className="progress-fill" style={{ width: `${progress}%` }} />
          </div>
          <div className="audio-time">
            <span>{formatTime(currentTime)}</span>
            <span>{formatTime(duration)}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
