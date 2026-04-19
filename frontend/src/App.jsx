import { useState } from 'react'
import './MusicCard'
import './App.css'
import MusicCard from './MusicCard';


function App() {
  const [songRequest, setSongRequest] = useState("");
  const [songs, setSongs] = useState([]);

  const handleSubmit = async () => {
    if (!songRequest) return;

    try {

      const res = await fetch("http://localhost:8000/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: songRequest, num_songs: 5 })
      });

      const data = await res.json();

      const songs = data.songs;

      // process the data and set songs
      setSongs(songs);

      setSongRequest("");

    } catch (error) {

    }
  };

  return <div>
    <div className="app-container">
      <input
      type="text"
      placeholder="Enter a song request"
      value={songRequest}
      onChange={(e) => setSongRequest(e.target.value)}
      onKeyDown={(e) => {
        if (e.key === "Enter") {
          handleSubmit();
        }
      }}
    />
    <button type="button" onClick={handleSubmit}> Find De Vibe </button>
    <div className="song-result-container">
      { songs.map( (song) => {
        return <MusicCard key={song.id} song={song}/>
      })}
    </div>
    </div>
  </div>
}

export default App;
