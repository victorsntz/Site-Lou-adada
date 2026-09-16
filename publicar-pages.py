#!/usr/bin/env python3
"""Publica o site no GitHub Pages, no endereço provisório.

Por que existe: o site de verdade usa caminho a partir da raiz (/assets/...),
que é o que o playbook manda e o que funciona no domínio próprio. O GitHub
Pages serve o repositório dentro de uma subpasta (/Site-Lou-adada/), onde a
barra inicial apontaria para o lugar errado.

Então este script monta uma cópia com caminho relativo, marca tudo como
noindex (para o Google nunca indexar o endereço de teste e concorrer com o
domínio final) e joga essa cópia na branch gh-pages. O site original não é
tocado em momento nenhum.

    python3 publicar-pages.py

Quando o domínio próprio entrar, rode ./trocar-dominio.sh e apague a branch
gh-pages: ela deixa de ter função.
"""
import os, re, shutil, subprocess, sys, tempfile

RAIZ = os.path.dirname(os.path.abspath(__file__))
BRANCH = 'gh-pages'
BASE = '/Site-Lou-adada/'          # subpasta em que o Pages publica

FORA = {'.git', 'docs', '.github', 'node_modules'}
ARQ_FORA = {'.htaccess', 'robots.txt', 'sitemap.xml',
            'trocar-dominio.sh', 'publicar-pages.py', '.gitignore'}

NOINDEX = ('<meta name="robots" content="noindex, nofollow" />\n'
           '<!-- Endereço provisório de teste. O noindex existe para o Google não\n'
           '     indexar esta cópia e concorrer com o domínio final. Some quando\n'
           '     o site for para o domínio de verdade. -->\n')

def arruma(html, pre, absoluto=False):
    """absoluto=True prefixa com a subpasta em vez de ../, para o 404, que o
       Pages serve a partir de qualquer profundidade de URL."""
    def troca(m):
        atr, caminho = m.group(1), m.group(2)
        raiz = BASE if absoluto else pre
        if caminho == '/':
            return '%s="%sindex.html"' % (atr, raiz)
        if caminho.startswith('//'):          # protocolo relativo: é externo
            return m.group(0)
        novo = caminho.lstrip('/')
        if novo.endswith('/'):                # pasta vira o index dela
            novo += 'index.html'
        return '%s="%s%s"' % (atr, raiz, novo)
    html = re.sub(r'\b(href|src|content)="(/[^"]*)"', troca, html)
    return html.replace('<meta charset="utf-8" />',
                        '<meta charset="utf-8" />\n' + NOINDEX, 1)

def montar(destino):
    total = 0
    for raiz, dirs, arqs in os.walk(RAIZ):
        dirs[:] = [d for d in dirs if d not in FORA]
        for a in arqs:
            if a in ARQ_FORA or a.endswith(('.bak', '.py', '.sh')):
                continue
            origem = os.path.join(raiz, a)
            rel = os.path.relpath(origem, RAIZ)
            alvo = os.path.join(destino, rel)
            os.makedirs(os.path.dirname(alvo) or destino, exist_ok=True)
            if a.endswith('.html'):
                with open(origem, encoding='utf-8') as f:
                    html = f.read()
                with open(alvo, 'w', encoding='utf-8') as f:
                    f.write(arruma(html, '../' * rel.count('/'),
                                   absoluto=(rel == '404.html')))
            else:
                shutil.copy2(origem, alvo)
            total += 1

    # sem isto o Pages ignora pasta que começa com _
    open(os.path.join(destino, '.nojekyll'), 'w').close()
    with open(os.path.join(destino, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write('# Endereço provisório de teste. Nada aqui deve ser indexado:\n'
                '# o site de verdade vai morar no domínio próprio.\n'
                'User-agent: *\nDisallow: /\n')
    return total

def conferir(destino):
    """Nenhuma barra inicial pode ter escapado: no Pages ela cai fora do site."""
    sobrou = []
    for raiz, _, arqs in os.walk(destino):
        for a in arqs:
            if not a.endswith('.html'):
                continue
            p = os.path.join(raiz, a)
            with open(p, encoding='utf-8') as f:
                for n, linha in enumerate(f, 1):
                    for m in re.finditer(r'\b(href|src)="(/[^"/][^"]*)"', linha):
                        if not m.group(2).startswith(BASE):
                            sobrou.append('%s:%d %s' %
                                          (os.path.relpath(p, destino), n, m.group(2)))
    return sobrou

def git(*args, cwd):
    return subprocess.run(('git',) + args, cwd=cwd, check=True,
                          capture_output=True, text=True).stdout.strip()

def main():
    remoto = git('remote', 'get-url', 'origin', cwd=RAIZ)
    temp = tempfile.mkdtemp(prefix='pages-')
    try:
        total = montar(temp)
        sobrou = conferir(temp)
        print('%d arquivos montados' % total)
        if sobrou:
            print('PAROU: sobrou caminho absoluto, ia quebrar no Pages:')
            print('\n'.join(sobrou[:10]))
            return 1
        print('caminhos conferidos: nenhum absoluto sobrou')

        # a branch não guarda história: ela é o site montado, e só
        git('init', '-q', '-b', BRANCH, cwd=temp)
        git('remote', 'add', 'origin', remoto, cwd=temp)
        git('add', '-A', cwd=temp)
        git('-c', 'user.name=Fortunato Estudio',
            '-c', 'user.email=loucadadapresentes@yahoo.com.br',
            'commit', '-q', '-m',
            'Louçadada no endereço provisório do GitHub Pages', cwd=temp)
        git('push', '-f', 'origin', BRANCH, cwd=temp)
        print('\npublicado em https://victorsntz.github.io%s' % BASE)
        print('Se for a primeira vez, ligue em Settings > Pages:')
        print('  Source: Deploy from a branch · Branch: %s · pasta / (root)' % BRANCH)
        return 0
    finally:
        shutil.rmtree(temp, ignore_errors=True)

sys.exit(main())
