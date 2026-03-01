def buscar_series_por_genero(genre_id):
    url = f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_KEY}&with_genres={genre_id}&language=pt-BR&sort_by=popularity.desc"
    
    response = requests.get(url)

    if response.status_code != 200:
        return "Erro ao conectar com a API 😢"

    data = response.json()
    series = data.get("results", [])[:3]

    if not series:
        return "Não encontrei séries 😢"

    resultado = ""

    for s in series:
        serie_id = s["id"]
        nome = s["name"]

        # 🔥 Segunda requisição para pegar episódios
        detalhes_url = f"https://api.themoviedb.org/3/tv/{serie_id}?api_key={TMDB_KEY}&language=pt-BR"
        detalhes_resp = requests.get(detalhes_url)

        if detalhes_resp.status_code == 200:
            detalhes = detalhes_resp.json()
            temporadas = detalhes.get("number_of_seasons", "?")
            episodios = detalhes.get("number_of_episodes", "?")

            resultado += (
                f"📺 {nome}\n"
                f"📀 {temporadas} temporadas\n"
                f"🎬 {episodios} episódios\n\n"
            )
        else:
            resultado += f"📺 {nome}\n\n"

    return resultado
