

---

# Weather App

## **Présentation générale du projet**
La Weather App est une application web qui affiche les conditions météorologiques actuelles d'une ville donnée. Ce projet a été développé dans le cadre d'un apprentissage personnel pour approfondir les connaissances en développement web, notamment en JavaScript et dans l'intégration d'API.

---

## **Fonctionnalités principales**
1. **Recherche par ville** : L'utilisateur peut entrer une ville et obtenir ses informations météo actuelles.
2. **Affichage des données** : 
   - Température actuelle (°C).
   - Taux d'humidité (%).
   - Vitesse du vent (km/h).
   - Conditions météo avec une icône illustrant le temps (soleil, nuages, pluie, etc.).
3. **Gestion des erreurs** : Si la ville saisie est invalide, un message d'erreur s'affiche.

---

## **Technologies utilisées**
- **HTML** : Structure de base de la page.
- **CSS** : Pour le style et la présentation (non inclus ici, mais supposé dans `style.css`).
- **JavaScript** : Gestion de l'interactivité, récupération et traitement des données de l'API.
- **API OpenWeatherMap** : Source des données météo en temps réel.

---

## **Structure et organisation**
### Fichiers et répertoires
- **`index.html`** : Contient la structure principale de l'application.
- **`style.css`** : Fichier de style pour personnaliser l'apparence de la page.
- **Dossier `images`** : Contient les icônes météo (par exemple : nuages, pluie, etc.) et l'image du bouton de recherche.

### Organisation des éléments HTML
- Une carte contenant trois sections principales :
  1. **Barre de recherche** : Saisie du nom de la ville et bouton de recherche.
  2. **Message d'erreur** : Avertit l'utilisateur en cas de nom de ville invalide.
  3. **Affichage météo** : Informations détaillées sur les conditions météo de la ville.

---

## **Détails techniques**
### Interaction avec l'API
L'application utilise `fetch()` pour envoyer des requêtes HTTP à l'API OpenWeatherMap. La clé API est encodée en Base64 pour une sécurité minimale et décodée à l'exécution avec `atob()`.

### Fonctionnalité principale
1. **Recherche météo** :
   - La fonction `checkWeather(city)` est appelée lorsque l'utilisateur clique sur le bouton de recherche ou appuie sur la touche "Entrée".
   - Elle envoie une requête à l'API, récupère les données et les affiche dynamiquement dans les éléments HTML.

2. **Gestion des erreurs** :
   - Si la ville est invalide (code HTTP 404), un message d'erreur est affiché, et la section météo est masquée.

3. **Icônes météo dynamiques** :
   - Selon les conditions météo retournées par l'API (par exemple, "Clear", "Clouds"), une image appropriée est affichée.

### Code JavaScript principal
```javascript
async function checkWeather(city) {
    const response = await fetch(apiUrl + city + `&appid=${apiKey}`);
    var data = await response.json();

    if (response.status == 404) {
        document.querySelector(".error").style.display = "block";
        document.querySelector(".weather").style.display = "none";
    } else {
        document.querySelector(".city").innerHTML = data.name;
        document.querySelector(".temp").innerHTML = Math.round(data.main.temp) + "°C";
        document.querySelector(".humidity").innerHTML = data.main.humidity + "%";
        document.querySelector(".wind").innerHTML = data.wind.speed + "km/h";

        const weatherCondition = data.weather[0].main;
        const icons = {
            Clouds: "clouds.png",
            Clear: "clear.png",
            Drizzle: "drizzle.png",
            Mist: "mist.png",
            Rain: "rain.png",
            Snow: "snow.png",
        };
        weatherIcon.src = `images/${icons[weatherCondition] || "default.png"}`;

        document.querySelector(".weather").style.display = "block";
        document.querySelector(".error").style.display = "none";
    }
}
```

### Gestion des événements
- **Bouton de recherche** : 
  ```javascript
  searchBtn.addEventListener("click", () => {
      checkWeather(searchBox.value);
  });
  ```
- **Touche "Entrée"** : 
  ```javascript
  searchBox.addEventListener("keypress", (e) => {
      if (e.key === "Enter") checkWeather(searchBox.value);
  });
  ```

---

## **Problèmes rencontrés et solutions**
### Clé API exposée
- **Problème** : La clé API est visible dans le code source.
- **Solution temporaire** : Encodage en Base64 avec `atob()`. Pour une sécurité accrue, une configuration côté serveur est préférable dans des projets plus complexes.

### Gestion des erreurs d'entrée
- **Problème** : Nom de ville incorrect entraînant un mauvais retour.
- **Solution** : Vérification du code HTTP (404) et affichage d'un message d'erreur.

---

## **Améliorations potentielles**
- **Interface utilisateur** :
  - Design responsive pour un meilleur affichage sur mobile.
  - Amélioration visuelle des messages d'erreur.
- **Fonctionnalités** :
  - Ajouter une liste déroulante des villes récemment recherchées.
  - Inclure une carte météo interactive.
  - Afficher les prévisions pour plusieurs jours.
- **Performance** :
  - Optimisation des appels API pour réduire la latence.
  - Cacher la clé API côté serveur pour améliorer la sécurité.

---

## **Conclusion**
### Ce qui a été appris
- Manipuler une API tierce dans une application web.
- Intégrer JavaScript pour manipuler dynamiquement le DOM.
- Gérer les événements utilisateur (clics, saisie au clavier).

### Impact
Ce projet a permis de développer des compétences pratiques en développement web et d'approfondir l'utilisation de JavaScript et des API. Il constitue une excellente base pour des projets plus complexes.

---
