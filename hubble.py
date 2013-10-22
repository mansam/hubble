#!/usr/bin/env python

import requests

def find_repositories(query, language, name_only):

    host = "https://api.github.com/search/repositories"
    headers = {
        "Accept": "application/vnd.github.preview"
    }
    params = {
        "q": query,
        "sort": "stars",
        "per_page": 10
    }
    if language:
        params['q'] += " language:%s" % language.strip()
    if name_only:
        params['q'] += " in:name"
    response = requests.get(host, params=params, headers=headers)

    return response.json()

def print_results(results):
    import pydoc
    import colorama
    from colorama import Fore, Back, Style
    colorama.init()
    reset = Fore.RESET + Back.RESET + Style.RESET_ALL

    output = u""
    output += "Hubble discovered %d modules matching your query." % results['total_count']
    if results['total_count'] > 10:
        output += "\nThat's way too many, so here are the best 10: "
    for item in results['items']:
        output += "\n%s, by %s" % (Fore.YELLOW + Style.BRIGHT + item['name'] + reset, Style.DIM + item['owner']['login'] + reset)
        #output += '\n\tAuthor:\t%s' % item['owner']['login']
        output += '\n\tLanguage:\t%s' % item['language']
        output += '\n\tStars:\t%d\tForks:\t%d' % (item['watchers_count'], item['forks_count'])
        output += '\n\tURL:\t\t%s' % item['html_url']
        output += '\n\tDescription:\t%s\n' % item['description']
        #output += '\n\tForks:\t\t%d' % item['forks_count']
    pydoc.pipepager(output.encode('utf-8'), cmd='less -R')

if __name__ == "__main__":
    import argparse
    import git

    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="package to search for")
    parser.add_argument("-n", "--name-only", action="store_true", help="search the only the project name")
    parser.add_argument("-l", "--language", help="only search repos written in this language")
    parser.add_argument("-c", "--clone", help="clone down the best match to the chosen directory")
    args = parser.parse_args()
    results = find_repositories(args.query, args.language, args.name_only)
    print_results(results)
    if args.clone:
        import git
        g = git.repo.Git()
        item = results['items'][0]
        g.clone(item['html_url'], args.clone)
        print("Cloned %s from %s." % (item['name'], item['html_url']))
