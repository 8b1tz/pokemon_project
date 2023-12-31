async function getPokemonData(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erro ao obter dados do Pokémon:', error);
    }
}

async function fetchPokemon() {
    const pokeListElement = document.getElementById('pokeList');

    try {
        const response = await fetch('https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0');
        const data = await response.json();

        for (const pokemon of data.results) {
            const pokemonData = await getPokemonData(pokemon.url);
            const { name, types, sprites } = pokemonData;
            const pokemonTypes = types.map(type => type.type.name).join(', ');

            const div = document.createElement('div');
            div.className = `pokemons`;
            div.innerHTML = `
                <img src="${sprites.front_default}" alt="${name}">
                <p><strong>Name:</strong> ${name}</p>
                <p><strong>Type:</strong> ${pokemonTypes}</p>
            `;
            pokeListElement.appendChild(div);
        }
    } catch (error) {
        console.error('Erro ao buscar a lista de Pokémon:', error);
    }
}

function searchPokemon() {
    const input = document.getElementById('searchInput').value.trim().toLowerCase();
    const pokemonCards = document.querySelectorAll('.pokemons');

    pokemonCards.forEach(card => {
        const name = card.querySelector('p').textContent.trim().toLowerCase();
        if (name.includes(input)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

fetchPokemon();
