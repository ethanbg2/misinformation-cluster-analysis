import requests
import json
import pandas as pd

class HoaxyApi:
    HOST = "api-hoaxy.p.rapidapi.com"
    URL = 'https://' + HOST

    def __init__(self, rapid_api_key):
        self.__headers = {
            'x-rapidapi-host': self.HOST, 
            'x-rapidapi-key': rapid_api_key
            }
    
    def get_networks_all_domains(self, domains, node_limit=1000, edge_limit=12500):
        all_networks = []
        for domain in domains:
            # get articles for domain
            response = self.search_by_domain(domain)
            articles = []
            try:
                articles = response['articles']
            except Exception as e:
                continue

            # get network for all articles
            ids = [a['id'] for a in articles]
            network = self.get_network(ids, node_limit=node_limit, edge_limit=edge_limit)
            try:
                network = pd.DataFrame(network['edges'])
                all_networks.append(network)
            except Exception as e:
                continue

        return pd.concat(all_networks)

    def search_by_domain(self, domain):
        q = {"query":f"domain:{domain}","use_lucene_syntax":"true","sort_by":"relevant"}
        return self.__get_response(q, "/articles")
    
    def search_by_title(self, title):
        q = {"query":f"title:{title}","use_lucene_syntax":"true","sort_by":"relevant"}
        return self.__get_response(q, "/articles")
    
    def general_search(self, query):
        q = {"query":query,"use_lucene_syntax":"false","sort_by":"relevant"}
        return self.__get_response(q, "/articles")
    
    def get_network(self, article_list, node_limit=1000, edge_limit=12500):
        q = {"ids":f"{article_list}","nodes_limit":str(node_limit),"edges_limit":str(edge_limit),"include_user_mentions":"true"}
        return self.__get_response(q, "/network")
    
    def __get_response(self, q, path):
        response = requests.request("GET", self.URL+path, headers=self.__headers, params=q)
        return json.loads(response.text)
        