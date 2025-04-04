import React, { useState } from 'react';
import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [pokemon, setPokemon] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchPokemon = async () => {
    if (!input) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`http://localhost:8000/pokemon/${input.toLowerCase()}`);
      if (!response.ok) {
        throw new Error('Pokemon not found');
      }
      const data = await response.json();
      setPokemon(data);
    } catch (err) {
      setError(err.message);
      setPokemon(null);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetchPokemon();
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Pokemon Finder</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter Pokemon ID or name"
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Loading...' : 'Search'}
          </button>
        </form>

        {error && <p className="error">Error: {error}</p>}

        {pokemon && (
          <div className="pokemon-card">
            <h2>{pokemon.name} (#{pokemon.id})</h2>
            {pokemon.sprite_url && (
              <img src={pokemon.sprite_url} alt={pokemon.name} />
            )}
            <div className="pokemon-details">
              <p><strong>Height:</strong> {pokemon.height / 10}m</p>
              <p><strong>Weight:</strong> {pokemon.weight / 10}kg</p>
              <p><strong>Base Experience:</strong> {pokemon.base_experience}</p>
              <p><strong>Types:</strong> {pokemon.types.join(', ')}</p>
              <p><strong>Abilities:</strong> {pokemon.abilities.join(', ')}</p>
              {/* <p><strong>Moves:</strong> {pokemon.moves.join(', ')}</p> */}
            </div>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;