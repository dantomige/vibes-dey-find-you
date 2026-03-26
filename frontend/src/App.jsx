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
      // const res = await fetch(""); // backend server request

      // const data = await res.json();

      // process the data and set songs
      setSongs([]);

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
