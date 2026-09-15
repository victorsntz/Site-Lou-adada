# Playbook — Estrutura & SEO para o site novo
### Baseado em tudo que foi construído e validado no fortunatoestudio.com (jun–jul/2026)

> **Como usar:** vocês estão na fase de design — perfeito, termina o design primeiro.
> Quando começar a construir, siga este documento na ordem. Ele também foi escrito
> pra ser entregue direto ao **Claude Code do projeto novo** (salve como `docs/PLAYBOOK-SEO.md`
> no repositório, ou cole o conteúdo no `CLAUDE.md`): ele sabe executar cada item daqui.
> Onde tiver **[ADAPTAR]**, troque pelo contexto do produto da sua esposa.

---

## 1. Fundações técnicas (fazer ANTES de qualquer página)

- **Domínio próprio** com HTTPS desde o dia 1. Decidir o domínio definitivo antes de indexar
  qualquer coisa (migrar domínio depois joga autoridade fora).
- **URLs limpas, padrão pasta**: cada página vive em `pasta/index.html` e a URL pública é
  `/sobre/`, `/contato/` — minúsculas, sem `.html`, com barra final. Links internos sempre
  **root-relative** (`/sobre/`, `/assets/foto.jpg`), nunca relativos à pasta.
- **`.htaccess` na raiz** (se Apache) com:
  - `ErrorDocument 404 /404.html` e uma **página 404 caprichada** (com links de volta);
  - **301 de toda URL antiga → nova** sempre que qualquer URL mudar (regra de ouro: URL
    nunca morre, ela redireciona);
  - bloqueio de arquivos de desenvolvimento (`docs/`, `.github/`, `package.json` → 404);
  - **cache de assets**: imagens/vídeo/fontes 1 ano (`immutable`), CSS/JS 1 mês.
- **CSS com versão**: linkar como `/site.css?v=1`. **REGRA CRÍTICA:** toda vez que o CSS
  mudar, subir o número (`?v=2`, `?v=3`...) em TODAS as páginas — senão o visitante que
  já veio antes fica com o CSS velho em cache por 30 dias e vê o site quebrado.
  (Isso aconteceu no Fortunato: imagens esticadas pra quem tinha cache antigo.)
- **`robots.txt`** simples: `User-agent: * / Allow: /` + linha `Sitemap: https://.../sitemap.xml`.
- **`sitemap.xml`** com TODAS as páginas indexáveis: `<loc>` + `<lastmod>` (atualizar a data
  quando a página mudar de verdade) + `<priority>` (home 1.0, páginas-chave 0.8, resto 0.6).
  Atualizar o sitemap **sempre** que criar/remover página.
- **Git como fonte da verdade** desde o início (nunca editar direto no servidor), e conhecer
  o comportamento do deploy (no Fortunato o deploy **não apaga** arquivos removidos — por
  isso remoção de página exige 301 no `.htaccess`, não só deletar o arquivo).

## 2. As páginas obrigatórias (a "casa" completa)

O Google premia site que parece **negócio de verdade**. Estrutura mínima:

| Página | Papel | Pontos críticos |
|---|---|---|
| `/` Home | Proposta de valor + H1 com a linguagem do cliente | 1 H1 só; seções claras; CTA visível |
| `/sobre/` | E-E-A-T: quem está por trás | História real, foto de verdade, FAQ |
| `/contato/` | Conversão + confiança do Google | **Endereço completo, telefone, mapa** + formulário |
| `/obrigado/` | Destino pós-formulário | É aqui que se mede a conversão (evento no GTM) |
| `/termos/` | Página de segurança | Confiança (o Google olha isso) |
| `/privacidade/` | Página de segurança + LGPD | Idem |
| `404.html` | Erro amigável | Links de volta pro conteúdo |
| **[ADAPTAR]** página do produto | A oferta | Preço claro, FAQ, prova social, schema Product |
| **[ADAPTAR]** provas/portfólio/depoimentos | Autoridade | Fotos reais com legenda, nunca banco de imagem |

**Lição do consultor (Gu):** contato completo (endereço + telefone + mapa) e páginas de
Termos/Privacidade não são burocracia — são sinal de confiança que pesa no ranqueamento.

## 3. SEO on-page (em CADA página)

- `<title>` único, ≤ 60 caracteres, keyword no começo: `Produto X — benefício | Marca`.
- `<meta name="description">` única, ~150–155 caracteres, com a keyword e um motivo pra clicar.
- `<link rel="canonical">` apontando pra própria URL limpa.
- **Open Graph completo** (og:title, og:description, og:image 1200×630, og:url, og:locale
  pt_BR) + `twitter:card summary_large_image` — é o cartão de visita no WhatsApp.
- **Favicons**: 32px, 180px (Apple), 512px.
- **Headings em ordem**: um único `<h1>`, depois `<h2>` → `<h3>` sem pular nível
  (o Fortunato tinha ordem quebrada e foi apontado em auditoria).
- **A linguagem do público, não a sua**: o cliente não busca o jargão da sua área — busca
  o problema dele. No Fortunato: ranquear "posicionamento/autoridade", não "branding".
  **[ADAPTAR]:** descubra as palavras que a cliente do produto realmente digita no Google
  (Google Trends + autocomplete ajudam) e escreva títulos/H1 com ELAS.

## 4. Imagens e mídia (performance + SEO)

- **Toda `<img>` com `width` e `height`** (evita layout shift, métrica do Google) **E**
  no CSS base: `img{max-width:100%;height:auto}` — sem o `height:auto`, os atributos
  esticam a imagem. (Bug real que tivemos.)
- Otimizar antes de subir: **máx. 1600px de largura, JPEG qualidade ~84, progressivo**.
  Nada de PNG de 7MB direto da pasta do designer.
- `alt` descritivo em tudo (acessibilidade + SEO de imagem).
- **Capa/LCP**: `fetchpriority="high"` na imagem principal da dobra; todo o resto
  `loading="lazy" decoding="async"`.
- Fontes do Google com carregamento assíncrono (`media="print" onload="this.media='all'"`).
- Vídeo: `preload="none"` + poster, nunca autoplay pesado na dobra.
- **Fotos reais com legenda** (produto, bastidores, pessoas) — legenda com `<figcaption>`.
  Não usar banco de imagem genérico; não usar foto de imprensa/agência (direito autoral).

## 5. Schema.org (JSON-LD) — o Google entendendo quem vocês são

Blocos que usamos no Fortunato, adaptados pro site de produto:

- **`WebSite`** — nome do site + URL.
- **`Organization` ou `LocalBusiness`** — com **NAP completo** (nome, endereço com CEP,
  telefone) idêntico ao do Google Business Profile, + `sameAs` listando TODAS as presenças
  (Instagram, YouTube, perfil no Google, etc.). Consistência de entidade é o que ensina o
  Google a não confundir a marca com outra parecida.
- **`Person`** — a fundadora, com `sameAs` das redes dela. **[ADAPTAR]**
- **`Product` + `Offer`** — nome do produto, imagem, descrição, `price` + `priceCurrency`
  (manter o preço do schema SEMPRE igual ao da página e ao do checkout!).
- **`FAQPage`** — nas páginas com FAQ (aparece direto no Google).
- **`BreadcrumbList`** — em páginas internas.
- **Regra de entidade:** o nome da marca grafado EXATAMENTE igual em todo lugar (site,
  GBP, Instagram, YouTube). No Fortunato, o Google confundia "estúdio" com um concorrente
  "studio" — consistência de grafia + schema resolve com o tempo.

## 6. Confiança e autoridade (E-E-A-T)

- **Google Business Profile** da marca desde o lançamento + pedir avaliações de verdade
  (o do Victor: 5.0 com 15 avaliações — pesa muito pra busca local e pra entidade).
- Autor(a) visível no conteúdo: foto + bio curta.
- **Acessibilidade** = SEO: contraste suficiente, sem atributos aria inválidos, sem
  elementos que PARECEM clicáveis mas não são (geram bounce, e bounce derruba ranking).
- **3 pilares da autoridade** (framework do consultor): técnica (on-page), conteúdo
  (blog/artigos), off-site (backlinks/imprensa). O site resolve o 1º; os outros dois são
  trabalho contínuo.

## 7. Analytics e conversão

- **Google Tag Manager** em todas as páginas (script no head + noscript no body).
- **Evento de conversão** no envio do formulário (ex.: `lead_form`) — medir na página
  `/obrigado/`, não no clique do botão.
- Formulário sem back-end: **Web3Forms** funciona bem (usamos no Fortunato).

## 8. Blog (quando chegar a hora — não precisa ser no lançamento)

- Estrutura **pilar + satélites**: 1 guia definitivo pra keyword principal + artigos
  menores pra variações, todos linkando entre si e pro pilar.
- **Pautas evergreen de fundo de funil** — temas que a cliente busca quando está perto de
  comprar. **Evitar tema datado/noticioso**: dá pico e vira página morta (lição do Gu).
- Anatomia do artigo que funcionou: breadcrumb, data de publicação E de atualização,
  tempo de leitura, resumo rápido (bullets), índice/TOC, imagens reais com legenda,
  FAQ no final (com schema), caixa de autor, **CTA pelo estágio do funil** (topo → produto
  de entrada; fundo → formulário/compra), links internos cruzados.
- Cada artigo entra no sitemap no dia da publicação + "Solicitar indexação" no GSC.

## 9. Google Search Console — ritual do dia 1

1. Criar propriedade de **DOMÍNIO** (não "prefixo de URL") — verificação por registro TXT
   no DNS. Cobre www, sem-www, http, https e qualquer subdomínio futuro de uma vez.
2. Enviar o `sitemap.xml`.
3. "Solicitar indexação" nas páginas-chave (home, produto, sobre) uma a uma.
4. Acompanhar **Desempenho** (cliques/impressões) semanalmente e **Indexação de páginas**
   sem pânico: URLs antigas dando 404 e "rastreada, não indexada" de resto de site antigo
   são normais e somem sozinhas. O número que importa é o de páginas **indexadas** e a curva
   de cliques.
5. Dar acesso ao consultor/parceiro (Configurações → Usuários e permissões).

## 10. Rotina de manutenção (o que manteve o Fortunato saudável)

- Commit + push a cada bloco de trabalho; verificar o site AO VIVO depois de cada deploy
  (com cache-bust: `?_=123` na URL).
- Mudou CSS? **Bump do `?v=`** em todas as páginas, sem exceção.
- Mudou/removeu URL? **301 no `.htaccess`**, sem exceção.
- Preço mudou? Mudar **nos 3 lugares**: página, schema JSON-LD e checkout — no mesmo dia.
- Página nova? Card/link interno apontando pra ela + sitemap + solicitar indexação.
- Nunca force-push; nunca editar direto no servidor.

---

## ✅ Checklist de pré-lançamento (imprimir e riscar)

**Técnico**
- [ ] HTTPS ok, domínio definitivo
- [ ] URLs limpas (`/pagina/`), links root-relative
- [ ] `.htaccess`: 404 custom, cache de assets, bloqueio de arquivos dev
- [ ] `robots.txt` + `sitemap.xml` completos
- [ ] CSS versionado `?v=1`
- [ ] 404.html com navegação

**Páginas**
- [ ] Home com H1 na linguagem da cliente
- [ ] Sobre com história + foto real
- [ ] Contato com endereço + telefone + mapa + formulário
- [ ] Obrigado (com evento de conversão)
- [ ] Termos + Privacidade
- [ ] Página do produto com preço + FAQ

**On-page (cada página)**
- [ ] title único ≤60 · description ~155 · canonical
- [ ] OG completo + imagem 1200×630
- [ ] 1 H1, headings em ordem
- [ ] imgs com width/height + `height:auto` no CSS + alt + lazy (menos a LCP: fetchpriority)

**Schema**
- [ ] WebSite + Organization/LocalBusiness (NAP + sameAs)
- [ ] Person (fundadora)
- [ ] Product + Offer (preço = página = checkout)
- [ ] FAQPage onde tiver FAQ

**Confiança**
- [ ] Google Business Profile criado + primeiras avaliações
- [ ] GTM + evento lead
- [ ] Contraste/acessibilidade ok, nada "clicável fake"

**Search Console**
- [ ] Propriedade de DOMÍNIO verificada (TXT no DNS)
- [ ] Sitemap enviado
- [ ] Indexação solicitada nas páginas-chave

---

*Gerado a partir do projeto fortunatoestudio.com — estrutura validada na prática: 42 páginas
indexadas e curva de cliques crescendo em ~2 semanas de trabalho (jul/2026).*
