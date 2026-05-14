const audio = document.getElementById('audio');
const playBtn = document.getElementById('playBtn');
const playIcon = document.getElementById('playIcon');
const progress = document.getElementById('progress');
const volume = document.getElementById('volume');
const cur = document.getElementById('cur');
const dur = document.getElementById('dur');

function fmt(s) {
    const m = Math.floor(s / 60);
    const sec = Math.floor(s % 60);
    return m + ':' + (sec < 10 ? '0' : '') + sec;
}

playBtn.addEventListener('click', () => {
    if (audio.paused) {
        audio.play();
        playIcon.className = 'ti ti-player-pause';
    } else {
        audio.pause();
        playIcon.className = 'ti ti-player-play';
    }
});

audio.addEventListener('timeupdate', () => {
    const pct = (audio.currentTime / audio.duration) * 100;
    progress.value = pct || 0;
    cur.textContent = fmt(audio.currentTime);
});

audio.addEventListener('loadedmetadata', () => {
    dur.textContent = fmt(audio.duration);
});

if(audio.readyState>=1){
    dur.textContent = fmt(audio.duration);
}

progress.addEventListener('input', () => {
    audio.currentTime = (progress.value / 100) * audio.duration;
});

volume.addEventListener('input', () => {
    audio.volume = volume.value / 100;
});

audio.volume = 0.7;