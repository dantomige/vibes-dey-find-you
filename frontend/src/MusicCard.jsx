function MusicCard({ song }) {
  return (
    <div className="card">
      <h3 className="title">{song.title}</h3>

      <p className="artist">
        {song.artists?.join(", ")}
      </p>

      <p className="score">
        Score: {song.score.toFixed(3)}
      </p>
    </div>
  );
}

export default MusicCard;