function calculateIV() {
    // Obtendo os valores dos campos de entrada
    const hp = parseInt(document.getElementById('hp').value);
    const attack = parseInt(document.getElementById('attack').value);
    const defense = parseInt(document.getElementById('defense').value);
    const spAttack = parseInt(document.getElementById('sp-attack').value);
    const spDefense = parseInt(document.getElementById('sp-defense').value);
    const speed = parseInt(document.getElementById('speed').value);
  
    // Definindo o valor máximo de um IV (31, que é o valor máximo possível nos jogos Pokémon)
    const maxIV = 31;
  
    // Calculando o total dos IVs
    const totalIV = hp + attack + defense + spAttack + spDefense + speed;
  
    // Calculando a porcentagem dos IVs em relação ao total máximo possível (186)
    const ivPercentage = (totalIV / (maxIV * 6)) * 100;
  
    // Exibindo o resultado
    const resultElement = document.getElementById('result');
    resultElement.innerHTML = `<br>Porcentagem dos IVs: ${ivPercentage.toFixed(2)}%`;
  }
  